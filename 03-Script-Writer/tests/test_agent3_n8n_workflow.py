"""Agent 3 n8n 工作流的结构和核心行为测试。"""

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent3-script-writer-v0.1-dev.json"


class Agent3N8nWorkflowTest(unittest.TestCase):
    """确认 Agent 3 工作流保持独立、7 个节点，并能处理核心案例。"""

    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW_PATH.read_text())
        cls.code_nodes = {
            node["name"]: node["parameters"]["jsCode"]
            for node in cls.workflow["nodes"]
            if node["type"] == "n8n-nodes-base.code"
        }

    def run_node_chain(self, form_json):
        """用 Node.js 模拟 n8n 的 Code 节点链路。"""
        sequence = [
            "2. 标准化 Agent 2 JSON",
            "3. 筛选可进入 Agent 3 的选题",
            "4. Script Writer",
            "5. Script QA",
            "6. JSON Script + Markdown Script Report",
        ]
        payload = json.dumps(form_json, ensure_ascii=False)
        script_parts = [f"let items = [{{ json: {payload} }}];\n"]
        for node_name in sequence:
            script_parts.append("items = (function(){ const $input = { first(){ return items[0]; }, all(){ return items; } };\n")
            script_parts.append(self.code_nodes[node_name])
            script_parts.append("\n})();\n")
            script_parts.append(
                "if (!Array.isArray(items) || !items[0] || !items[0].json) { throw new Error('Invalid n8n item output'); }\n"
            )
        script_parts.append("console.log(JSON.stringify(items[0].json));\n")
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write("".join(script_parts))
            script_path = handle.name
        result = subprocess.run(["node", script_path], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def run_single_code_node(self, node_name, input_json):
        """单独运行某个 Code 节点，用于测试 QA 重新生成。"""
        payload = json.dumps(input_json, ensure_ascii=False)
        script = textwrap.dedent(
            f"""
            let items = [{{ json: {payload} }}];
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
        """工作流名称和节点数量必须符合 Agent 3 v0.1 DEV。"""
        self.assertEqual("AI Health OS - Agent 3 Script Writer v0.1 DEV", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))

    def test_code_nodes_have_valid_javascript(self):
        """所有 Code 节点 JavaScript 必须可解析。"""
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")

    def test_normal_topic_generates_script(self):
        """正常 ready_for_agent3 选题应生成完整脚本。"""
        agent2_json = {
            "agent": "agent_2",
            "compliance_results": [
                {
                    "original_title": "Why your evening tea choice matters",
                    "compliant_title": "Why your evening tea choice matters",
                    "compliant_hook": "Your night tea might be the easiest wellness swap.",
                    "safe_core_claim": "May help support general wellness education.",
                    "ready_for_agent3": True,
                }
            ],
        }
        result = self.run_node_chain({"agent2_json": json.dumps(agent2_json)})

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_3", result["agent"])
        self.assertEqual("agent_4", result["handoff"]["next_agent"])
        self.assertEqual(1, len(result["scripts"]))
        self.assertIn("hook", result["scripts"][0])
        self.assertIn("body", result["scripts"][0])
        self.assertIn("cta", result["scripts"][0])
        self.assertIn("# Agent 3 Script Report", result["report_markdown"])

    def test_no_ready_topic_returns_insufficient_data(self):
        """没有 ready_for_agent3 的选题时不能生成脚本。"""
        agent2_json = {
            "agent": "agent_2",
            "compliance_results": [
                {"compliant_title": "Not ready topic", "ready_for_agent3": False}
            ],
        }
        result = self.run_node_chain({"agent2_json": json.dumps(agent2_json)})

        self.assertEqual("insufficient_data", result["status"])
        self.assertEqual([], result["scripts"])

    def test_qa_regenerates_hook_when_risky_phrase_appears(self):
        """Hook 出现 cure 等违规词时，QA 必须重新生成安全表达。"""
        result = self.run_single_code_node(
            "5. Script QA",
            {
                "status": "drafted",
                "draft_scripts": [
                    {
                        "video_title": "Risky script",
                        "video_goal": "Test QA",
                        "estimated_duration": "30–45 seconds",
                        "hook": "This herb can cure your problem fast.",
                        "body": "This is a general wellness body.",
                        "cta": "Save this for later and ask a professional.",
                        "hashtags": ["#WellnessTok"],
                    }
                ],
            },
        )

        fixed_script = result["qa_scripts"][0]
        self.assertTrue(fixed_script["qa"]["regenerated_due_to_risk"])
        self.assertIn("cure", fixed_script["qa"]["blocked_phrases_found"])
        self.assertNotIn("cure", fixed_script["hook"].lower())


if __name__ == "__main__":
    unittest.main()
