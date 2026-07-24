"""Agent 6 V1.1 n8n 工作流兼容 Agent 5 V1.1 真实输出的测试。"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent6-publishing-package-analytics-v1.1.json"
ORIGINAL_WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent6-publishing-package-analytics-v0.1-dev.json"


REAL_AGENT5_ROOIBOS_OUTPUT = [
    {
        "workflow": "AI Health OS",
        "source_agent": "agent_4",
        "agent": "agent_5",
        "version": "1.1",
        "status": "success",
        "generated_at": "2026-07-24T00:00:00.000Z",
        "total_visual_plans": 1,
        "voiceover_packages": [
            {
                "package_id": "agent5_voice_1",
                "source_visual_plan_id": "agent3_script_1",
                "video_title": "Rooibos Tea Before Bed | Simple wellness story",
                "voiceover_script": "A calm Rooibos tea moment before bed. Do not present this as medical advice, treatment, dosage guidance, or a guaranteed result. Save this for your next cozy evening routine.",
                "full_voiceover_script": "A calm Rooibos tea moment before bed. Do not present this as medical advice, treatment, dosage guidance, or a guaranteed result. Save this for your next cozy evening routine.",
                "narration_segments": [
                    {
                        "segment_number": 1,
                        "start_time_seconds": 0,
                        "end_time_seconds": 3,
                        "duration_seconds": 3,
                        "voiceover_text": "A calm Rooibos tea moment before bed.",
                        "subtitle_text": "A calm Rooibos tea moment before bed.",
                    },
                    {
                        "segment_number": 2,
                        "start_time_seconds": 3,
                        "end_time_seconds": 8,
                        "duration_seconds": 5,
                        "voiceover_text": "Do not present this as medical advice, treatment, dosage guidance, or a guaranteed result.",
                        "subtitle_text": "Do not present this as medical advice or a guaranteed result.",
                    },
                    {
                        "segment_number": 3,
                        "start_time_seconds": 8,
                        "end_time_seconds": 12,
                        "duration_seconds": 4,
                        "voiceover_text": "Save this for your next cozy evening routine.",
                        "subtitle_text": "Save this for your next cozy evening routine.",
                    },
                ],
                "subtitle_segments": [
                    {"index": 1, "start": 0, "end": 3, "text": "A calm Rooibos tea moment before bed."},
                    {"index": 2, "start": 3, "end": 8, "text": "Do not present this as medical advice or a guaranteed result."},
                    {"index": 3, "start": 8, "end": 12, "text": "Save this for your next cozy evening routine."},
                ],
                "srt": "1\n00:00:00,000 --> 00:00:03,000\nA calm Rooibos tea moment before bed.\n\n2\n00:00:03,000 --> 00:00:08,000\nDo not present this as medical advice or a guaranteed result.\n\n3\n00:00:08,000 --> 00:00:12,000\nSave this for your next cozy evening routine.",
                "tts_prompt": "Read in natural American English, warm calm wellness tone. No medical claims.",
                "pacing_notes": "Keep a calm 30–45 second short-form pacing style.",
                "subtitle_qa": {"passed": True, "qa_score": 100, "issues": [], "corrections_made": []},
                "qa_passed": True,
                "qa_score": 100,
                "qa_issues": [],
                "ready_for_agent6": True,
            }
        ],
        "handoff": {"next_agent": "agent_6", "ready_count": 1, "failed_qa_count": 0, "manual_review_count": 0},
    }
]


class Agent6V11WorkflowTest(unittest.TestCase):
    """确认 Agent 6 V1.1 只增强 Agent 5 V1.1 输出兼容。"""

    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW_PATH.read_text())
        cls.original_workflow = json.loads(ORIGINAL_WORKFLOW_PATH.read_text())
        cls.code_nodes = {
            node["name"]: node["parameters"]["jsCode"]
            for node in cls.workflow["nodes"]
            if node["type"] == "n8n-nodes-base.code"
        }

    def run_code_sequence(self, form_json, sequence):
        """用 Node.js 模拟 n8n Code 节点链路。"""
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

    def test_v11_workflow_name_and_nodes_are_preserved(self):
        """复制版应改名 V1.1，但保留 7 个节点和节点名称。"""
        self.assertEqual("AI Health OS - Agent 6 Publishing Package & Analytics V1.1", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertEqual(
            [
                "1. Agent6 输入",
                "2. 标准化 Agent5 JSON",
                "3. 筛选 ready_for_agent6",
                "4. Publishing Package Builder",
                "5. Publishing QA",
                "6. JSON + Markdown",
                "7. 显示报告",
            ],
            [node["name"] for node in self.workflow["nodes"]],
        )

    def test_original_v01_workflow_was_not_modified(self):
        """原 Agent 6 v0.1 DEV 工作流必须仍然存在且名称不变。"""
        self.assertEqual("AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV", self.original_workflow["name"])

    def test_node2_reads_voiceover_packages_from_agent5_wrapper_array(self):
        """Node 2 必须从外层数组中读取 voiceover_packages[]。"""
        result = self.run_code_sequence(
            {"agent5_json": json.dumps(REAL_AGENT5_ROOIBOS_OUTPUT)},
            ["2. 标准化 Agent5 JSON"],
        )

        self.assertEqual("parsed", result["status"])
        self.assertEqual("agent_5", result["source_agent"])
        self.assertEqual(1, result["total_voiceover_packages"])
        self.assertEqual("Rooibos Tea Before Bed | Simple wellness story", result["voiceover_packages"][0]["video_title"])
        self.assertTrue(result["voiceover_packages"][0]["ready_for_agent6"])

    def test_end_to_end_generates_publishing_package_from_real_agent5_output(self):
        """真实 Agent 5 Rooibos JSON 应生成发布包、Caption、Hashtags 和 Analytics。"""
        result = self.run_code_sequence(
            {"agent5_json": json.dumps(REAL_AGENT5_ROOIBOS_OUTPUT)},
            [
                "2. 标准化 Agent5 JSON",
                "3. 筛选 ready_for_agent6",
                "4. Publishing Package Builder",
                "5. Publishing QA",
                "6. JSON + Markdown",
            ],
        )

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_5", result["source_agent"])
        self.assertEqual("agent_6", result["agent"])
        self.assertEqual("1.1", result["version"])
        self.assertGreaterEqual(result["total_voiceover_packages"], 1)
        self.assertGreaterEqual(len(result["publishing_packages"]), 1)
        self.assertGreaterEqual(result["handoff"]["ready_count"], 1)
        package = result["publishing_packages"][0]
        self.assertTrue(package["ready_for_manual_publish"])
        self.assertIn("tiktok_caption", package)
        self.assertIn("instagram_caption", package)
        self.assertIn("youtube_shorts_caption", package)
        self.assertGreaterEqual(len(package["hashtags"]), 3)
        self.assertIn("analytics_template", package)
        self.assertIn("ab_test_plan", package)
        self.assertIn("# AI Health OS — Agent 6 Publishing Package & Analytics Report", result["report_markdown"])

    def test_markdown_fenced_json_input_is_supported(self):
        """Node 2 应支持 Markdown fenced JSON。"""
        fenced = "```json\n" + json.dumps(REAL_AGENT5_ROOIBOS_OUTPUT, ensure_ascii=False) + "\n```"
        result = self.run_code_sequence({"agent5_json": fenced}, ["2. 标准化 Agent5 JSON"])

        self.assertEqual("parsed", result["status"])
        self.assertEqual(1, result["total_voiceover_packages"])

    def test_ready_for_agent6_truthy_values_are_supported(self):
        """Node 3 应支持 true、字符串 true/Yes/yes 和数字 1。"""
        for value in [True, "true", "Yes", "yes", 1]:
            sample = json.loads(json.dumps(REAL_AGENT5_ROOIBOS_OUTPUT))
            sample[0]["voiceover_packages"][0]["ready_for_agent6"] = value
            result = self.run_code_sequence(
                {"agent5_json": json.dumps(sample)},
                ["2. 标准化 Agent5 JSON", "3. 筛选 ready_for_agent6"],
            )
            self.assertEqual("ready_for_publishing_package", result["status"])
            self.assertEqual(1, result["selected_count"])

    def test_code_nodes_have_valid_javascript(self):
        """所有 Code 节点 JavaScript 必须可解析。"""
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")


if __name__ == "__main__":
    unittest.main()
