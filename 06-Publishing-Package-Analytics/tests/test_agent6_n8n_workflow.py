"""Agent 6 n8n 工作流的结构和核心行为测试。"""

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent6-publishing-package-analytics-v0.1-dev.json"


class Agent6N8nWorkflowTest(unittest.TestCase):
    """确认 Agent 6 工作流独立、7 个节点，并能处理主要正常和异常案例。"""

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
            "2. 标准化 Agent5 JSON",
            "3. 筛选 ready_for_agent6",
            "4. Publishing Package Builder",
            "5. Publishing QA",
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
        """单独运行某个 Code 节点，用于测试 Publishing QA 修复能力。"""
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
        """工作流名称和节点数量必须符合 Agent 6 v0.1 DEV。"""
        self.assertEqual("AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertIn("1. Agent6 输入", self.workflow["connections"])

    def test_code_nodes_have_valid_javascript(self):
        """所有 Code 节点 JavaScript 必须可解析。"""
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")

    def test_normal_ready_package_generates_publishing_package(self):
        """正常 ready_for_agent6 内容应生成完整发布素材包。"""
        agent5_json = {
            "agent": "agent_5",
            "voiceover_packages": [
                {
                    "package_id": "voice_1",
                    "video_title": "Why your evening tea choice matters",
                    "full_voiceover_script": "Your night tea might be the easiest wellness swap. Save this for your next cozy evening routine.",
                    "ready_for_agent6": True,
                }
            ],
        }
        result = self.run_node_chain({"agent5_json": json.dumps(agent5_json)})

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_6", result["agent"])
        self.assertEqual(1, len(result["publishing_packages"]))
        package = result["publishing_packages"][0]
        self.assertTrue(package["ready_for_manual_publish"])
        self.assertIn("tiktok_caption", package)
        self.assertIn("analytics_template", package)
        self.assertIn("ab_test_plan", package)
        self.assertIn("# AI Health OS — Agent 6 Publishing Package & Analytics Report", result["report_markdown"])

    def test_no_ready_package_returns_insufficient_data(self):
        """没有 ready_for_agent6 的内容时不能生成发布包。"""
        agent5_json = {"agent": "agent_5", "voiceover_packages": [{"video_title": "Not ready", "ready_for_agent6": False}]}
        result = self.run_node_chain({"agent5_json": json.dumps(agent5_json)})

        self.assertEqual("insufficient_data", result["status"])
        self.assertEqual([], result["publishing_packages"])

    def test_invalid_json_returns_parse_error(self):
        """输入 JSON 格式错误时应返回 error 和 parse_error，工作流不崩溃。"""
        result = self.run_node_chain({"agent5_json": "{ bad json"})

        self.assertEqual("error", result["status"])
        self.assertIn("Agent 5 JSON 解析失败", result["parse_error"])
        self.assertEqual([], result["publishing_packages"])

    def test_risky_caption_is_blocked_by_qa(self):
        """发布文案出现高风险健康表达时应阻止人工发布。"""
        result = self.run_single_code_node(
            "5. Publishing QA",
            {
                "status": "publishing_package_drafted",
                "draft_publishing_packages": [
                    {
                        "publishing_id": "risk_1",
                        "video_title": "Risky claim",
                        "cover_text": "Cure diabetes now",
                        "tiktok_caption": "This can cure diabetes fast.",
                        "instagram_caption": "Replace medication with this.",
                        "youtube_shorts_caption": "Guaranteed result.",
                        "cta": "Try it.",
                        "hashtags": ["#WellnessTok", "#Shorts", "#Health"],
                        "seo_keywords": ["wellness", "shorts", "routine"],
                        "publishing_checklist": ["Review"],
                        "analytics_template": {"views": 0},
                        "ab_test_plan": [{"test_name": "A", "variant_a": "a", "variant_b": "b", "success_metric": "views"}],
                    }
                ],
            },
        )

        package = result["qa_publishing_packages"][0]
        self.assertFalse(package["ready_for_manual_publish"])
        self.assertTrue(package["qa_issues"])

    def test_missing_fields_are_repaired(self):
        """缺少 Hashtags、SEO、Checklist、Analytics 或 A/B 计划时，Publishing QA 应自动修复。"""
        result = self.run_single_code_node(
            "5. Publishing QA",
            {
                "status": "publishing_package_drafted",
                "draft_publishing_packages": [
                    {
                        "publishing_id": "repair_1",
                        "video_title": "Repair publishing package",
                        "cover_text": "A very long cover text that should be shortened because mobile covers need short text",
                        "tiktok_caption": "Simple wellness education.",
                        "instagram_caption": "Simple wellness education.",
                        "youtube_shorts_caption": "Simple wellness education.",
                        "cta": "Save this.",
                    }
                ],
            },
        )

        package = result["qa_publishing_packages"][0]
        self.assertTrue(package["corrections_made"])
        self.assertGreaterEqual(len(package["hashtags"]), 3)
        self.assertIn("analytics_template", package)
        self.assertLessEqual(len(package["cover_text"]), 40)


if __name__ == "__main__":
    unittest.main()
