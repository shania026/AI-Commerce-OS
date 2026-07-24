"""AI Health OS Master Orchestrator n8n 工作流结构测试。"""

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-master-orchestrator-agent-1-6-v1.0.json"


class MasterOrchestratorWorkflowTest(unittest.TestCase):
    """确认总控工作流只调用现有 Agent 1-6，并保留串行和错误处理结构。"""

    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW_PATH.read_text())
        cls.code_nodes = {
            node["name"]: node["parameters"]["jsCode"]
            for node in cls.workflow["nodes"]
            if node["type"] == "n8n-nodes-base.code"
        }

    def run_code_node(self, node_name, payload):
        script = textwrap.dedent(
            f"""
            let items = [{{ json: {json.dumps(payload, ensure_ascii=False)} }}];
            items = (function(){{ const $input = {{ first(){{ return items[0]; }}, all(){{ return items; }} }};
            {self.code_nodes[node_name]}
            }})();
            if (!Array.isArray(items) || !items[0] || !items[0].json) {{ throw new Error('Invalid n8n item output'); }}
            console.log(JSON.stringify(items[0].json));
            """
        )
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write(script)
            script_path = handle.name
        result = subprocess.run(["node", script_path], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_workflow_name_and_node_count(self):
        self.assertEqual("AI Health OS - Master Orchestrator Agent 1-6 V1.0", self.workflow["name"])
        self.assertEqual(28, len(self.workflow["nodes"]))

    def test_execute_workflow_nodes_call_existing_agents_in_order(self):
        expected = [
            "AI Health OS Agent 1 Memory Analysis V1.0",
            "AI Health OS - Agent 2 Health Compliance Rewriter V1.1",
            "AI Health OS - Agent 3 Script Writer V1.1",
            "AI Health OS - Agent 4 Visual Director V1.1",
            "AI Health OS - Agent 5 Voiceover & Subtitle Producer V1.1",
            "AI Health OS - Agent 6 Publishing Package & Analytics V1.1",
        ]
        actual = [
            node["parameters"]["workflowId"]["value"]
            for node in self.workflow["nodes"]
            if node["type"] == "n8n-nodes-base.executeWorkflow"
        ]
        self.assertEqual(expected, actual)

    def test_success_checks_and_unified_error_report_exist(self):
        node_names = [node["name"] for node in self.workflow["nodes"]]
        for agent_number in range(1, 7):
            self.assertIn(f"Agent {agent_number} Success Check", node_names)
        self.assertIn("Unified Error Report", node_names)
        self.assertIn("AI Health OS Final Report", node_names)

    def test_code_nodes_have_valid_javascript(self):
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")


    def test_execute_workflow_nodes_continue_to_error_report_on_failure(self):
        """Execute Workflow 子流程失败时不能让 Form 直接提交失败，应进入统一 Error Report。"""
        execute_nodes = [node for node in self.workflow["nodes"] if node["type"] == "n8n-nodes-base.executeWorkflow"]
        self.assertEqual(6, len(execute_nodes))
        for node in execute_nodes:
            self.assertEqual("database", node["parameters"].get("source"), msg=node["name"])
            self.assertTrue(node.get("continueOnFail"), msg=node["name"])
            self.assertTrue(node.get("alwaysOutputData"), msg=node["name"])
            self.assertEqual("continueRegularOutput", node.get("onError"), msg=node["name"])

    def test_normalize_execute_workflow_error_routes_to_failed_status(self):
        """Execute Workflow 报错对象应被标准化成 failed，而不是让工作流启动即终止。"""
        result = self.run_code_node("Normalize Agent 1 Output", {"error": {"message": "Workflow could not be started"}})

        self.assertFalse(result["success"])
        self.assertEqual("agent_1", result["failed_agent"])
        self.assertIn("Workflow could not be started", result["error_message"])

    def test_prepare_agent_inputs_pass_full_previous_json(self):
        agent2_input = self.run_code_node(
            "Prepare Agent 2 Input",
            {"topic": "Rooibos Tea Before Bed", "agent_1_output": {"status": "success", "ranked_topics": [{"title": "Rooibos Tea Before Bed"}]}},
        )
        self.assertIn("agent1_json", agent2_input)
        self.assertIn("ranked_topics", agent2_input["agent1_json"])

        agent6_input = self.run_code_node(
            "Prepare Agent 6 Input",
            {"agent_5_output": {"status": "success", "voiceover_packages": [{"ready_for_agent6": True}]}},
        )
        self.assertIn("agent5_json", agent6_input)
        self.assertIn("voiceover_packages", agent6_input["agent5_json"])

    def test_final_report_uses_agent6_publishing_packages(self):
        payload = {
            "master_run_id": "master_rooibos_test",
            "started_at": "2026-07-24T00:00:00.000Z",
            "topic": "Rooibos Tea Before Bed",
            "product_name": "Rooibos",
            "target_platform": "TikTok",
            "agent_1_status": "success",
            "agent_2_status": "success",
            "agent_3_status": "success",
            "agent_4_status": "success",
            "agent_5_status": "success",
            "agent_6_status": "success",
            "agent_4_output": {"handoff": {"ready_count": 1}},
            "agent_5_output": {"handoff": {"ready_count": 1}},
            "agent_6_output": {
                "handoff": {"ready_count": 1},
                "publishing_packages": [
                    {
                        "video_title": "Rooibos Tea Before Bed | Simple wellness story",
                        "cover_text": "Rooibos Before Bed",
                        "cta": "Save this.",
                        "tiktok_caption": "A calm Rooibos tea moment before bed.",
                        "instagram_caption": "A calm Rooibos tea moment before bed.",
                        "youtube_shorts_caption": "Rooibos Tea Before Bed.",
                        "hashtags": ["#WellnessTok", "#Rooibos", "#Shorts"],
                        "seo_keywords": ["rooibos", "tea routine"],
                        "suggested_posting_time": {"primary": "7:00 PM", "secondary": "12:00 PM"},
                        "publishing_checklist": ["Human review before posting."],
                        "analytics_template": {"views": 0},
                        "ab_test_plan": [{"test_name": "Caption", "variant_a": "A", "variant_b": "B", "success_metric": "views"}],
                        "qa_passed": True,
                        "qa_score": 100,
                        "qa_issues": [],
                        "ready_for_manual_publish": True,
                    }
                ],
            },
        }
        result = self.run_code_node("Build Final Master Report", payload)

        self.assertEqual("success", result["status"])
        self.assertTrue(result["ready_for_manual_publish"])
        self.assertEqual(1, len(result["final_publishing_packages"]))
        self.assertIn("# AI Health OS Master Orchestrator Report", result["report_markdown"])


if __name__ == "__main__":
    unittest.main()
