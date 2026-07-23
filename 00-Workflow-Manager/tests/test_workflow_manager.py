"""Workflow Manager MVP 的基础测试。"""

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "workflow.py"
spec = importlib.util.spec_from_file_location("workflow_manager", MODULE_PATH)
workflow_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow_manager)


class WorkflowManagerTest(unittest.TestCase):
    """确认工作流管理器自动调度 Agent 1，并预留 Agent 2 人工交接点。"""

    def test_agent1_is_registered(self):
        """当前 MVP 必须登记 Agent 1。"""
        self.assertIn("agent1", workflow_manager.AGENT_REGISTRY)

    def test_agent1_command_calls_existing_agent(self):
        """Workflow Manager 应该调用 Agent 1，而不是重新实现 Agent 1。"""
        agent = workflow_manager.AGENT_REGISTRY["agent1"]
        command = workflow_manager.build_agent1_command(agent, limit=5)

        self.assertIn("01-Viral-Finder/health_topic_finder.py", "/".join(command))
        self.assertIn("--report", command)
        self.assertIn("--output", command)

    def test_agent2_is_registered_but_not_auto_runnable(self):
        """Agent 2 只登记交接信息，不能被 Workflow Manager 自动调度。"""
        agent = workflow_manager.AGENT_REGISTRY["agent2"]

        self.assertFalse(agent.enabled_for_cli)
        self.assertIn("健康合规改写", agent.description)
        self.assertIn("agent2_compliance_results.json", str(agent.default_output_path))

        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent2", limit=5)

    def test_unknown_agent_is_rejected(self):
        """没有登记的 Agent 不能被调度，避免误以为 Agent 3 已经存在。"""
        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent3", limit=5)


if __name__ == "__main__":
    unittest.main()
