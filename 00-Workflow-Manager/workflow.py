"""
AI Health OS - Workflow Manager MVP

这个文件是整个 AI Health OS 的主入口。
它不生成业务内容，也不开发新的 Agent，只负责调度已经完成的 Agent。

当前 MVP 只调度 Agent 1：健康选题发现 Agent。
未来接入 Agent 2、Agent 3 时，可以继续在 AGENT_REGISTRY 里增加配置。
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


# 仓库根目录。workflow.py 位于 00-Workflow-Manager 内，所以父目录就是项目根目录。
REPO_ROOT = Path(__file__).resolve().parents[1]

# 统一文件夹：以后所有工作流都从 Inputs 读，向 Outputs 和 Reports 写。
INPUTS_DIR = REPO_ROOT / "Inputs"
OUTPUTS_DIR = REPO_ROOT / "Outputs"
REPORTS_DIR = REPO_ROOT / "Reports"


@dataclass(frozen=True)
class AgentSpec:
    """描述一个 Agent 的入口和默认输入输出，方便未来继续接入 Agent 2、Agent 3。"""

    name: str
    script_path: Path
    default_input_path: Path
    default_output_path: Path
    default_report_path: Path
    description: str
    enabled_for_cli: bool = True


# Agent 注册表：Workflow Manager 只认识这里登记过的 Agent。
# 当前主流程仍然只自动调度 Agent 1。Agent 2 只登记名称、职责和默认交接路径，
# 保留人工确认步骤，不会被 run_workflow 自动触发，也不会开发 Agent 3。
AGENT_REGISTRY: Dict[str, AgentSpec] = {
    "agent1": AgentSpec(
        name="agent1",
        script_path=REPO_ROOT / "01-Viral-Finder" / "health_topic_finder.py",
        default_input_path=INPUTS_DIR / "health_topics.csv",
        default_output_path=OUTPUTS_DIR / "agent1_ranked_health_topics.json",
        default_report_path=REPORTS_DIR / "agent1_decision_report.md",
        description="健康选题发现 Agent：读取候选选题 CSV，输出 JSON 排序和 Markdown 决策报告。",
    ),
    "agent2": AgentSpec(
        name="agent2",
        script_path=REPO_ROOT / "00-Workflow-Manager" / "n8n" / "ai-health-os-agent2-compliance-rewriter-v0.1-dev.json",
        default_input_path=OUTPUTS_DIR / "agent1_ranked_health_topics.json",
        default_output_path=OUTPUTS_DIR / "agent2_compliance_results.json",
        default_report_path=REPORTS_DIR / "agent2_compliance_report.md",
        description="健康合规改写 Agent（v0.1 DEV）：接收人工确认后的 Agent 1 选题，识别健康声明风险并谨慎改写标题、Hook 和核心表述。",
        enabled_for_cli=False,
    ),
}


def ensure_workflow_directories() -> None:
    """确保统一 Inputs、Outputs、Reports 文件夹存在。"""
    for directory in [INPUTS_DIR, OUTPUTS_DIR, REPORTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def build_agent1_command(agent: AgentSpec, limit: int) -> List[str]:
    """生成调用 Agent 1 的命令；单独拆出来方便测试和未来扩展。"""
    return [
        sys.executable,
        str(agent.script_path),
        "--input",
        str(agent.default_input_path),
        "--output",
        str(agent.default_output_path),
        "--report",
        str(agent.default_report_path),
        "--limit",
        str(limit),
    ]


def run_agent(agent_name: str, limit: int) -> AgentSpec:
    """按名称运行一个已登记 Agent；当前 MVP 只支持 agent1。"""
    if agent_name not in AGENT_REGISTRY:
        available_agents = ", ".join(AGENT_REGISTRY)
        raise ValueError(f"未登记的 Agent：{agent_name}。当前可用：{available_agents}")

    agent = AGENT_REGISTRY[agent_name]
    if not agent.enabled_for_cli:
        raise ValueError(f"{agent.name} 已登记为预留 Agent，但尚未接入 Workflow Manager 自动调度；请先通过人工确认和独立 n8n 工作流运行。")
    if not agent.script_path.exists():
        raise FileNotFoundError(f"找不到 Agent 脚本：{agent.script_path}")
    if not agent.default_input_path.exists():
        raise FileNotFoundError(f"找不到 Agent 输入文件：{agent.default_input_path}")

    command = build_agent1_command(agent, limit)
    subprocess.run(command, check=True)
    return agent


def run_workflow(limit: int) -> List[AgentSpec]:
    """运行 AI Health OS 当前主流程；MVP 阶段只调用 Agent 1。"""
    ensure_workflow_directories()
    completed_agents = [run_agent("agent1", limit)]
    return completed_agents


def print_summary(completed_agents: List[AgentSpec]) -> None:
    """用中文打印本次工作流结果，方便非程序员确认文件在哪里。"""
    print("\nWorkflow Manager 执行完成。")
    for agent in completed_agents:
        print(f"- 已完成：{agent.name}｜{agent.description}")
        print(f"  JSON 输出：{agent.default_output_path}")
        print(f"  Markdown 报告：{agent.default_report_path}")
    print("\n下一步：请先查看 Reports 里的决策报告；确认前不要开发 Agent 2。")


def build_parser() -> argparse.ArgumentParser:
    """创建命令行参数；目前只暴露 Top N 数量，保持 MVP 简单。"""
    parser = argparse.ArgumentParser(description="AI Health OS Workflow Manager MVP")
    parser.add_argument("--limit", type=int, default=5, help="Agent 1 最多输出几个选题，默认 5 个")
    return parser


def main() -> None:
    """Workflow Manager 命令行入口。"""
    parser = build_parser()
    args = parser.parse_args()

    try:
        completed_agents = run_workflow(args.limit)
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

    print_summary(completed_agents)


if __name__ == "__main__":
    main()
