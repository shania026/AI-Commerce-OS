"""Agent 4 n8n 工作流的结构和核心行为测试。"""

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent4-visual-director-v0.1-dev.json"


class Agent4N8nWorkflowTest(unittest.TestCase):
    """确认 Agent 4 工作流独立、7 个节点，并能处理主要正常和异常案例。"""

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
            "2. 标准化 Agent 3 JSON",
            "3. 筛选可进入 Agent 4 的脚本",
            "4. Visual Director",
            "5. Visual QA",
            "6. JSON Visual Plan + Markdown Visual Report",
        ]
        payload = json.dumps(form_json, ensure_ascii=False)
        script_parts = [f"let items = [{{ json: {payload} }}];\n"]
        for node_name in sequence:
            script_parts.append("items = (function(){ const $input = { first(){ return items[0]; }, all(){ return items; } };\n")
            script_parts.append(self.code_nodes[node_name])
            script_parts.append("\n})();\n")
            script_parts.append("if (!Array.isArray(items) || !items[0] || !items[0].json) { throw new Error('Invalid n8n item output'); }\n")
        script_parts.append("console.log(JSON.stringify(items[0].json));\n")
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write("".join(script_parts))
            script_path = handle.name
        result = subprocess.run(["node", script_path], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def run_single_code_node(self, node_name, input_json):
        """单独运行某个 Code 节点，用于测试 Visual QA 修复能力。"""
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
        """工作流名称和节点数量必须符合 Agent 4 v0.1 DEV。"""
        self.assertEqual("AI Health OS - Agent 4 Visual Director v0.1 DEV", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertIn("1. Agent 4 输入表单", self.workflow["connections"])

    def test_code_nodes_have_valid_javascript(self):
        """所有 Code 节点 JavaScript 必须可解析。"""
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")

    def test_normal_script_generates_visual_plan(self):
        """正常脚本应生成完整镜头方案，并且 ready_for_agent5 = true。"""
        agent3_json = {
            "agent": "agent_3",
            "scripts": [
                {
                    "script_id": "script_1",
                    "video_title": "Why your evening tea choice matters",
                    "hook": "Your night tea might be the easiest wellness swap.",
                    "body": "Show the warm cup. Explain the evening routine. Keep it educational and calm.",
                    "cta": "Save this for your next cozy evening routine.",
                    "qa_passed": True,
                }
            ],
        }
        result = self.run_node_chain({"agent3_json": json.dumps(agent3_json)})

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_4", result["agent"])
        self.assertEqual("agent_5", result["handoff"]["next_agent"])
        self.assertEqual(1, len(result["visual_plans"]))
        plan = result["visual_plans"][0]
        self.assertTrue(plan["ready_for_agent5"])
        self.assertEqual("9:16", plan["aspect_ratio"])
        self.assertGreaterEqual(len(plan["scenes"]), 3)
        self.assertIn("image_prompt", plan["scenes"][0])
        self.assertIn("video_prompt", plan["scenes"][0])
        self.assertIn("# AI Health OS — Agent 4 Visual Director Report", result["report_markdown"])

    def test_no_ready_script_returns_insufficient_data(self):
        """没有可进入 Agent 4 的脚本时不能编造视觉方案。"""
        agent3_json = {"agent": "agent_3", "scripts": [{"video_title": "Not ready", "qa_passed": False}]}
        result = self.run_node_chain({"agent3_json": json.dumps(agent3_json)})

        self.assertEqual("insufficient_data", result["status"])
        self.assertEqual([], result["visual_plans"])

    def test_high_risk_medical_expression_blocks_agent5(self):
        """脚本含高风险医疗表达时，Visual QA 必须阻止进入 Agent 5。"""
        agent3_json = {
            "agent": "agent_3",
            "scripts": [
                {
                    "script_id": "risk_1",
                    "video_title": "Risky cure claim",
                    "hook": "This routine can cure diabetes.",
                    "body": "Show a before and after cure and tell people to replace medication.",
                    "cta": "Try it today.",
                    "qa_passed": True,
                }
            ],
        }
        result = self.run_node_chain({"agent3_json": json.dumps(agent3_json)})

        self.assertEqual("success", result["status"])
        self.assertFalse(result["visual_plans"][0]["ready_for_agent5"])
        self.assertGreater(result["handoff"]["failed_qa_count"], 0)
        self.assertTrue(result["visual_plans"][0]["qa_issues"])

    def test_missing_hook_or_cta_is_repaired_or_rejected(self):
        """缺少 Hook 或 CTA 时，QA 应给出问题或自动补充安全占位。"""
        agent3_json = {
            "agent": "agent_3",
            "scripts": [
                {"script_id": "missing_1", "video_title": "Gentle tea routine", "body": "Show the tea ritual.", "qa_passed": True}
            ],
        }
        result = self.run_node_chain({"agent3_json": json.dumps(agent3_json)})
        plan = result["visual_plans"][0]

        self.assertIn(plan["ready_for_agent5"], [True, False])
        self.assertGreaterEqual(len(plan["scenes"]), 3)
        self.assertTrue(plan["corrections_made"] or plan["qa_passed"])

    def test_abnormal_scene_duration_is_adjusted(self):
        """镜头总时长异常时，Visual QA 应自动调整预计时长。"""
        result = self.run_single_code_node(
            "5. Visual QA",
            {
                "status": "visual_planned",
                "draft_visual_plans": [
                    {
                        "script_id": "duration_1",
                        "video_title": "Duration mismatch",
                        "visual_style": "Natural Wellness",
                        "aspect_ratio": "9:16",
                        "estimated_duration_seconds": 45,
                        "scenes": [
                            {"scene_number": 1, "start_time": "0s", "end_time": "3s", "duration_seconds": 3, "script_section": "Hook", "narration_text": "Hook", "visual_description": "Safe visual", "image_prompt": "vertical 9:16 no medical claims", "video_prompt": "vertical 9:16 no medical claims", "on_screen_text": "Hook", "continuity_notes": "Same look"},
                            {"scene_number": 2, "start_time": "3s", "end_time": "8s", "duration_seconds": 5, "script_section": "Body", "narration_text": "Body", "visual_description": "Safe visual", "image_prompt": "vertical 9:16 no medical claims", "video_prompt": "vertical 9:16 no medical claims", "on_screen_text": "Body", "continuity_notes": "Same look"},
                            {"scene_number": 3, "start_time": "8s", "end_time": "12s", "duration_seconds": 4, "script_section": "CTA", "narration_text": "CTA", "visual_description": "Safe visual", "image_prompt": "vertical 9:16 no medical claims", "video_prompt": "vertical 9:16 no medical claims", "on_screen_text": "CTA", "continuity_notes": "Same look"},
                        ],
                    }
                ],
            },
        )

        plan = result["qa_visual_plans"][0]
        self.assertEqual(12, plan["estimated_duration_seconds"])
        self.assertTrue(any("镜头总时长" in item for item in plan["corrections_made"]))

    def test_invalid_json_returns_parse_error(self):
        """输入 JSON 格式错误时应返回 error 和 parse_error，工作流不崩溃。"""
        result = self.run_node_chain({"agent3_json": "{ bad json"})

        self.assertEqual("error", result["status"])
        self.assertIn("Agent 3 JSON 解析失败", result["parse_error"])
        self.assertEqual([], result["visual_plans"])


if __name__ == "__main__":
    unittest.main()
