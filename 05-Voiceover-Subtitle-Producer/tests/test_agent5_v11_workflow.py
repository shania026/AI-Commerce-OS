"""Agent 5 V1.1 n8n 工作流兼容 Agent 4 V1.1 真实输出的测试。"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent5-voiceover-subtitle-producer-v1.1.json"
ORIGINAL_WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent5-voiceover-subtitle-producer-v0.1-dev.json"


REAL_AGENT4_ROOIBOS_OUTPUT = [
    {
        "workflow": "AI Health OS",
        "source_agent": "agent_3",
        "agent": "agent_4",
        "version": "1.1",
        "status": "success",
        "total_scripts": 1,
        "visual_plans": [
            {
                "script_id": "agent3_script_1",
                "video_title": "Rooibos Tea Before Bed | Simple wellness story",
                "visual_style": "Cozy Evening Ritual",
                "color_style": "warm amber, cream, soft brown",
                "lighting": "soft warm evening practical lighting",
                "music_style": "calm modern wellness background music",
                "aspect_ratio": "9:16",
                "estimated_duration_seconds": 12,
                "scene_count": 3,
                "ready_for_agent5": True,
                "qa_passed": True,
                "qa_score": 100,
                "scenes": [
                    {
                        "scene_number": 1,
                        "start_time": "0s",
                        "end_time": "3s",
                        "duration_seconds": 3,
                        "script_section": "Hook",
                        "narration_text": "A calm Rooibos tea moment before bed.",
                        "visual_description": "Warm Rooibos tea on a bedside table.",
                        "on_screen_text": "A calmer evening ritual",
                        "image_prompt": "Vertical 9:16 Rooibos tea, cozy evening lighting, no medical claims.",
                        "video_prompt": "Vertical 9:16 video, Rooibos tea steam, no medical claims.",
                    },
                    {
                        "scene_number": 2,
                        "start_time": "3s",
                        "end_time": "8s",
                        "duration_seconds": 5,
                        "script_section": "Body",
                        "narration_text": "Show the warm cup and explain the calm evening routine.",
                        "visual_description": "Hands pour caffeine-free Rooibos tea.",
                        "on_screen_text": "General wellness only",
                        "image_prompt": "Vertical 9:16 hands pouring Rooibos tea.",
                        "video_prompt": "Vertical 9:16 tea ritual.",
                    },
                    {
                        "scene_number": 3,
                        "start_time": "8s",
                        "end_time": "12s",
                        "duration_seconds": 4,
                        "script_section": "CTA",
                        "narration_text": "Save this for your next cozy evening routine.",
                        "visual_description": "Creator writes a simple evening tea note.",
                        "on_screen_text": "Save this idea",
                        "image_prompt": "Vertical 9:16 creator and tea.",
                        "video_prompt": "Vertical 9:16 creator writing.",
                    },
                ],
            }
        ],
        "handoff": {"next_agent": "agent_5", "ready_count": 1},
    }
]


class Agent5V11WorkflowTest(unittest.TestCase):
    """确认 Agent 5 V1.1 只增强 Agent 4 V1.1 输出兼容。"""

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
        self.assertEqual("AI Health OS - Agent 5 Voiceover & Subtitle Producer V1.1", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertEqual(
            [
                "1. Agent5 输入",
                "2. 标准化 Agent4 JSON",
                "3. 筛选 ready_for_agent5",
                "4. Voiceover Producer",
                "5. Subtitle QA",
                "6. JSON + Markdown",
                "7. 显示报告",
            ],
            [node["name"] for node in self.workflow["nodes"]],
        )

    def test_original_v01_workflow_was_not_modified(self):
        """原 Agent 5 v0.1 DEV 工作流必须仍然存在且名称不变。"""
        self.assertEqual("AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV", self.original_workflow["name"])

    def test_node2_reads_visual_plans_from_agent4_wrapper_array(self):
        """Node 2 必须从外层数组中读取 visual_plans[]。"""
        result = self.run_code_sequence(
            {"agent4_json": json.dumps(REAL_AGENT4_ROOIBOS_OUTPUT)},
            ["2. 标准化 Agent4 JSON"],
        )

        self.assertEqual("parsed", result["status"])
        self.assertEqual("agent_4", result["source_agent"])
        self.assertEqual(1, result["total_visual_plans"])
        self.assertEqual("Rooibos Tea Before Bed | Simple wellness story", result["visual_plans"][0]["video_title"])
        self.assertTrue(result["visual_plans"][0]["ready_for_agent5"])

    def test_end_to_end_generates_voiceover_package_from_real_agent4_output(self):
        """真实 Agent 4 Rooibos JSON 应生成配音、字幕和 SRT 并交给 Agent 6。"""
        result = self.run_code_sequence(
            {"agent4_json": json.dumps(REAL_AGENT4_ROOIBOS_OUTPUT)},
            [
                "2. 标准化 Agent4 JSON",
                "3. 筛选 ready_for_agent5",
                "4. Voiceover Producer",
                "5. Subtitle QA",
                "6. JSON + Markdown",
            ],
        )

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_4", result["source_agent"])
        self.assertEqual("agent_5", result["agent"])
        self.assertEqual("1.1", result["version"])
        self.assertGreaterEqual(len(result["voiceover_packages"]), 1)
        self.assertEqual("agent_6", result["handoff"]["next_agent"])
        self.assertGreaterEqual(result["handoff"]["ready_count"], 1)
        package = result["voiceover_packages"][0]
        self.assertTrue(package["ready_for_agent6"])
        self.assertIn("voiceover_script", package)
        self.assertIn("narration_segments", package)
        self.assertIn("subtitle_segments", package)
        self.assertIn("-->", package["srt"])
        self.assertIn("tts_prompt", package)
        self.assertIn("pacing_notes", package)
        self.assertIn("subtitle_qa", package)

    def test_ready_for_agent5_truthy_values_are_supported(self):
        """Node 3 应支持 true、字符串 true/Yes/yes 和数字 1。"""
        for value in [True, "true", "Yes", "yes", 1]:
            sample = json.loads(json.dumps(REAL_AGENT4_ROOIBOS_OUTPUT))
            sample[0]["visual_plans"][0]["ready_for_agent5"] = value
            result = self.run_code_sequence(
                {"agent4_json": json.dumps(sample)},
                ["2. 标准化 Agent4 JSON", "3. 筛选 ready_for_agent5"],
            )
            self.assertEqual("ready_for_voiceover", result["status"])
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
