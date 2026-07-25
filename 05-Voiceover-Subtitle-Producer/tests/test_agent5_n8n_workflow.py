"""Agent 5 n8n 工作流的结构和核心行为测试。"""

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent5-voiceover-subtitle-producer-v0.1-dev.json"


class Agent5N8nWorkflowTest(unittest.TestCase):
    """确认 Agent 5 工作流独立、7 个节点，并能处理主要正常和异常案例。"""

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
            "2. 标准化 Agent4 JSON",
            "3. 筛选 ready_for_agent5",
            "4. Voiceover Producer",
            "5. Subtitle QA",
            "6. JSON + Markdown",
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
        """单独运行某个 Code 节点，用于测试 Subtitle QA 修复能力。"""
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
        """工作流名称和节点数量必须符合 Agent 5 v0.1 DEV。"""
        self.assertEqual("AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertIn("1. Agent5 输入", self.workflow["connections"])

    def test_code_nodes_have_valid_javascript(self):
        """所有 Code 节点 JavaScript 必须可解析。"""
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")

    def test_normal_visual_plan_generates_voiceover_package(self):
        """正常 ready_for_agent5 视觉方案应生成完整配音字幕包。"""
        agent4_json = {
            "agent": "agent_4",
            "visual_plans": [
                {
                    "script_id": "script_1",
                    "video_title": "Why your evening tea choice matters",
                    "ready_for_agent5": True,
                    "scenes": [
                        {"scene_number": 1, "start_time": "0s", "end_time": "3s", "duration_seconds": 3, "narration_text": "Your night tea might be the easiest wellness swap."},
                        {"scene_number": 2, "start_time": "3s", "end_time": "8s", "duration_seconds": 5, "narration_text": "Show the warm cup and explain the calm evening routine."},
                        {"scene_number": 3, "start_time": "8s", "end_time": "12s", "duration_seconds": 4, "narration_text": "Save this for your next cozy evening routine."},
                    ],
                }
            ],
        }
        result = self.run_node_chain({"agent4_json": json.dumps(agent4_json)})

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_5", result["agent"])
        self.assertEqual("agent_6", result["handoff"]["next_agent"])
        self.assertEqual(1, len(result["voiceover_packages"]))
        package = result["voiceover_packages"][0]
        self.assertTrue(package["ready_for_agent6"])
        self.assertIn("-->", package["srt"])
        self.assertIn("tts_prompt", package)
        self.assertIn("# AI Health OS — Agent 5 Voiceover & Subtitle Report", result["report_markdown"])

    def test_no_ready_visual_plan_returns_insufficient_data(self):
        """没有 ready_for_agent5 的视觉方案时不能生成配音字幕。"""
        agent4_json = {"agent": "agent_4", "visual_plans": [{"video_title": "Not ready", "ready_for_agent5": False}]}
        result = self.run_node_chain({"agent4_json": json.dumps(agent4_json)})

        self.assertEqual("insufficient_data", result["status"])
        self.assertEqual([], result["voiceover_packages"])

    def test_invalid_json_returns_parse_error(self):
        """输入 JSON 格式错误时应返回 error 和 parse_error，工作流不崩溃。"""
        result = self.run_node_chain({"agent4_json": "{ bad json"})

        self.assertEqual("error", result["status"])
        self.assertIn("Agent 4 JSON 解析失败", result["parse_error"])
        self.assertEqual([], result["voiceover_packages"])

    def test_risky_voiceover_is_blocked_by_qa(self):
        """字幕或配音出现高风险医疗表达时应阻止进入 Agent 6。"""
        result = self.run_single_code_node(
            "5. Subtitle QA",
            {
                "status": "voiceover_drafted",
                "draft_voiceover_packages": [
                    {
                        "package_id": "risk_1",
                        "video_title": "Risky audio",
                        "voice_style": "warm",
                        "voiceover_segments": [
                            {"segment_number": 1, "start_time_seconds": 0, "end_time_seconds": 3, "duration_seconds": 3, "voiceover_text": "This can cure diabetes.", "subtitle_text": "This can cure diabetes.", "pacing": "fast"}
                        ],
                        "tts_prompt": "Read with guaranteed result energy.",
                    }
                ],
            },
        )

        package = result["qa_voiceover_packages"][0]
        self.assertFalse(package["ready_for_agent6"])
        self.assertTrue(package["qa_issues"])

    def test_missing_subtitle_and_bad_time_are_repaired(self):
        """缺字幕或时间不合理时，Subtitle QA 应自动修复。"""
        result = self.run_single_code_node(
            "5. Subtitle QA",
            {
                "status": "voiceover_drafted",
                "draft_voiceover_packages": [
                    {
                        "package_id": "repair_1",
                        "video_title": "Repair audio",
                        "voice_style": "warm",
                        "voiceover_segments": [
                            {"segment_number": 5, "start_time_seconds": 5, "end_time_seconds": 2, "duration_seconds": 4, "voiceover_text": "A calm wellness subtitle line.", "subtitle_text": "", "pacing": "natural"}
                        ],
                        "tts_prompt": "",
                    }
                ],
            },
        )

        package = result["qa_voiceover_packages"][0]
        self.assertIn("-->", package["srt"])
        self.assertTrue(package["corrections_made"])
        self.assertEqual(1, package["voiceover_segments"][0]["segment_number"])
        self.assertGreater(package["voiceover_segments"][0]["end_time_seconds"], package["voiceover_segments"][0]["start_time_seconds"])


if __name__ == "__main__":
    unittest.main()
