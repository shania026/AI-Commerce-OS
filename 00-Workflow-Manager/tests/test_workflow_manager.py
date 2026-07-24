"""Workflow Manager MVP 的基础测试。"""

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "workflow.py"
spec = importlib.util.spec_from_file_location("workflow_manager", MODULE_PATH)
workflow_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow_manager)


class WorkflowManagerTest(unittest.TestCase):
    """确认工作流管理器自动调度 Agent 1，并预留 Agent 2/3/4/5/6 人工交接点。"""

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
        self.assertIn("V1.0", agent.description)
        self.assertIn("ai-health-os-agent2-compliance-rewriter-v1.0.json", str(agent.script_path))
        self.assertIn("agent2_compliance_results.json", str(agent.default_output_path))

        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent2", limit=5)


    def test_agent2_n8n_workflow_is_v1_release(self):
        """Agent 2 V1.0 n8n 工作流应保持 7 个节点。"""
        workflow_path = Path(workflow_manager.AGENT_REGISTRY["agent2"].script_path)
        workflow = json.loads(workflow_path.read_text())

        self.assertEqual("AI Health OS - Agent 2 Health Compliance Rewriter V1.0", workflow["name"])
        self.assertEqual(7, len(workflow["nodes"]))
        self.assertIn("1. Agent 2 输入表单", workflow["connections"])



    def test_agent2_v11_is_registered_but_original_agent2_remains(self):
        """Agent 2 V1.1 作为 Agent E 兼容复制版登记，原 V1.0 仍保留。"""
        original = workflow_manager.AGENT_REGISTRY["agent2"]
        compatible = workflow_manager.AGENT_REGISTRY["agent2_v11"]

        self.assertIn("ai-health-os-agent2-compliance-rewriter-v1.0.json", str(original.script_path))
        self.assertFalse(compatible.enabled_for_cli)
        self.assertIn("Agent E", compatible.description)
        self.assertIn("ai-health-os-agent2-compliance-rewriter-v1.1.json", str(compatible.script_path))

        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent2_v11", limit=5)

    def test_agent2_v11_n8n_workflow_is_compatible_copy(self):
        """Agent 2 V1.1 复制版应保持 7 个节点。"""
        workflow_path = Path(workflow_manager.AGENT_REGISTRY["agent2_v11"].script_path)
        workflow = json.loads(workflow_path.read_text())

        self.assertEqual("AI Health OS - Agent 2 Health Compliance Rewriter V1.1", workflow["name"])
        self.assertEqual(7, len(workflow["nodes"]))
        self.assertIn("1. Agent 2 输入表单", workflow["connections"])

    def test_agent3_v11_is_registered_but_original_agent3_remains(self):
        """Agent 3 V1.1 作为 Agent 2 V1.1 兼容复制版登记，原 V1.0 仍保留。"""
        original = workflow_manager.AGENT_REGISTRY["agent3"]
        compatible = workflow_manager.AGENT_REGISTRY["agent3_v11"]

        self.assertIn("ai-health-os-agent3-script-writer-v1.0.json", str(original.script_path))
        self.assertFalse(compatible.enabled_for_cli)
        self.assertIn("Agent 2 V1.1", compatible.description)
        self.assertIn("ai-health-os-agent3-script-writer-v1.1.json", str(compatible.script_path))

        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent3_v11", limit=5)

    def test_agent3_v11_n8n_workflow_is_compatible_copy(self):
        """Agent 3 V1.1 复制版应保持 7 个节点。"""
        workflow_path = Path(workflow_manager.AGENT_REGISTRY["agent3_v11"].script_path)
        workflow = json.loads(workflow_path.read_text())

        self.assertEqual("AI Health OS - Agent 3 Script Writer V1.1", workflow["name"])
        self.assertEqual(7, len(workflow["nodes"]))
        self.assertIn("1. Agent 3 输入表单", workflow["connections"])


    def test_agent4_is_registered_but_not_auto_runnable(self):
        """Agent 4 v0.1 DEV 只登记交接信息，不能被 Workflow Manager 自动调度。"""
        agent = workflow_manager.AGENT_REGISTRY["agent4"]

        self.assertFalse(agent.enabled_for_cli)
        self.assertIn("视觉导演", agent.description)
        self.assertIn("v0.1 DEV", agent.description)
        self.assertIn("ai-health-os-agent4-visual-director-v0.1-dev.json", str(agent.script_path))
        self.assertIn("agent4_visual_plan_results.json", str(agent.default_output_path))
        self.assertIn("agent4_visual_director_report.md", str(agent.default_report_path))

        with self.assertRaises(ValueError):
    def test_agent4_n8n_workflow_is_dev_release(self):
        """Agent 4 v0.1 DEV n8n 工作流应保持 7 个节点。"""
        workflow_path = Path(workflow_manager.AGENT_REGISTRY["agent4"].script_path)
        workflow = json.loads(workflow_path.read_text())

        self.assertEqual("AI Health OS - Agent 4 Visual Director v0.1 DEV", workflow["name"])
        self.assertEqual(7, len(workflow["nodes"]))
        self.assertIn("1. Agent 4 输入表单", workflow["connections"])


    def test_agent5_is_registered_but_not_auto_runnable(self):
        """Agent 5 v0.1 DEV 只登记交接信息，不能被 Workflow Manager 自动调度。"""
        agent = workflow_manager.AGENT_REGISTRY["agent5"]

        self.assertFalse(agent.enabled_for_cli)
        self.assertIn("配音字幕", agent.description)
        self.assertIn("v0.1 DEV", agent.description)
        self.assertIn("ai-health-os-agent5-voiceover-subtitle-producer-v0.1-dev.json", str(agent.script_path))
        self.assertIn("agent5_voiceover_subtitle_results.json", str(agent.default_output_path))
        self.assertIn("agent5_voiceover_subtitle_report.md", str(agent.default_report_path))

        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent5", limit=5)

    def test_agent5_n8n_workflow_is_dev_release(self):
        """Agent 5 v0.1 DEV n8n 工作流应保持 7 个节点。"""
        workflow_path = Path(workflow_manager.AGENT_REGISTRY["agent5"].script_path)
        workflow = json.loads(workflow_path.read_text())

        self.assertEqual("AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV", workflow["name"])
        self.assertEqual(7, len(workflow["nodes"]))
        self.assertIn("1. Agent5 输入", workflow["connections"])


    def test_agent6_is_registered_but_not_auto_runnable(self):
        """Agent 6 v0.1 DEV 只登记交接信息，不能被 Workflow Manager 自动调度。"""
        agent = workflow_manager.AGENT_REGISTRY["agent6"]

        self.assertFalse(agent.enabled_for_cli)
        self.assertIn("发布素材包", agent.description)
        self.assertIn("v0.1 DEV", agent.description)
        self.assertIn("ai-health-os-agent6-publishing-package-analytics-v0.1-dev.json", str(agent.script_path))
        self.assertIn("agent6_publishing_package_results.json", str(agent.default_output_path))
        self.assertIn("agent6_publishing_package_report.md", str(agent.default_report_path))

        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent6", limit=5)

    def test_agent6_n8n_workflow_is_dev_release(self):
        """Agent 6 v0.1 DEV n8n 工作流应保持 7 个节点。"""
        workflow_path = Path(workflow_manager.AGENT_REGISTRY["agent6"].script_path)
        workflow = json.loads(workflow_path.read_text())

        self.assertEqual("AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV", workflow["name"])
        self.assertEqual(7, len(workflow["nodes"]))
        self.assertIn("1. Agent6 输入", workflow["connections"])

    def test_unknown_agent_is_rejected(self):
        """没有登记的 Agent 不能被调度，避免误以为 Agent 7 已经存在。"""
        with self.assertRaises(ValueError):
            workflow_manager.run_agent("agent7", limit=5)

            workflow_manager.run_agent("agent3", limit=5)


if __name__ == "__main__":
    unittest.main()
