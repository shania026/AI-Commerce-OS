"""Agent 4 V1.1 n8n 工作流兼容 Agent 3 V1.1 真实输出的测试。"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent4-visual-director-v1.1.json"
ORIGINAL_WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent4-visual-director-v0.1-dev.json"


REAL_AGENT3_V11_OUTPUT = [
    {
        "workflow": "AI Health OS",
        "source_agent": "agent_2",
        "agent": "agent_3",
        "version": "1.1",
        "status": "success",
        "scripts": [
            {
                "script_id": "agent3_script_1",
                "source_title": "Rooibos Tea Before Bed",
                "video_title": "Rooibos Tea Before Bed | Simple wellness story",
                "video_description": "A short educational wellness video about Rooibos Tea Before Bed. Not medical advice.",
                "video_goal": "Turn an approved compliance-safe topic into a 30–45 second educational short video script.",
                "estimated_duration": "30–45 seconds",
                "hook": "If you've seen this wellness idea online, here is the safer way to understand it: Rooibos Tea Before Bed",
                "body": "Here is the idea: Rooibos Tea Before Bed. Instead of making big health promises, frame it as general wellness education. May help support general wellness education. For short-form content, keep the message simple: explain the habit, show the routine, and avoid disease or medication claims.",
                "cta": "Save this if you want more simple wellness ideas, and always check with a qualified professional for personal health questions.",
                "hashtags": ["#WellnessTok", "#HealthyHabits", "#TeaTok", "#Rooibos"],
                "source_risk_level": "low",
                "qa": {
                    "passed": True,
                    "blocked_phrases_found": [],
                    "regenerated_due_to_risk": False,
                },
            }
        ],
        "handoff": {"next_agent": "agent_4", "ready_count": 1},
    }
]


class Agent4V11WorkflowTest(unittest.TestCase):
    """确认 Agent 4 V1.1 只增强 Agent 3 V1.1 输出兼容。"""

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


    def run_single_code_node(self, node_name, input_json):
        """单独运行某个 Code 节点，用于验证 Visual QA 细节。"""
        payload = json.dumps(input_json, ensure_ascii=False)
        script_parts = [f"let items = [{{ json: {payload} }}];\n"]
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
        """复制版应改名 V1.1，但保留 6 个可调用节点和节点名称。"""
        self.assertEqual("AI Health OS - Agent 4 Visual Director V1.1", self.workflow["name"])
        self.assertEqual(6, len(self.workflow["nodes"]))
        self.assertEqual(
            [
                "When Executed by Another Workflow",
                "2. 标准化 Agent 3 JSON",
                "3. 筛选可进入 Agent 4 的脚本",
                "4. Visual Director",
                "5. Visual QA",
                "6. JSON Visual Plan + Markdown Visual Report",
            ],
            [node["name"] for node in self.workflow["nodes"]],
        )

    def test_original_v01_workflow_was_not_modified(self):
        """原 Agent 4 v0.1 DEV 工作流必须仍然存在且名称不变。"""
        self.assertEqual("AI Health OS - Agent 4 Visual Director v0.1 DEV", self.original_workflow["name"])

    def test_node2_reads_scripts_from_agent3_v11_wrapper_array(self):
        """Node 2 必须从外层数组中读取 scripts[]。"""
        result = self.run_code_sequence(
            {"agent3_json": json.dumps(REAL_AGENT3_V11_OUTPUT)},
            ["2. 标准化 Agent 3 JSON"],
        )

        self.assertEqual("parsed", result["status"])
        self.assertEqual("agent_3", result["source_agent"])
        self.assertEqual(1, result["total_scripts"])
        self.assertEqual("Rooibos Tea Before Bed | Simple wellness story", result["scripts"][0]["video_title"])
        self.assertEqual("agent_4", result["source_handoff"]["next_agent"])

    def test_end_to_end_generates_visual_project_from_real_agent3_v11_output(self):
        """真实 Agent 3 V1.1 输出应生成视觉方案并交给 Agent 5。"""
        result = self.run_code_sequence(
            {"agent3_json": json.dumps(REAL_AGENT3_V11_OUTPUT)},
            [
                "2. 标准化 Agent 3 JSON",
                "3. 筛选可进入 Agent 4 的脚本",
                "4. Visual Director",
                "5. Visual QA",
                "6. JSON Visual Plan + Markdown Visual Report",
            ],
        )

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_3", result["source_agent"])
        self.assertEqual("agent_4", result["agent"])
        self.assertEqual("1.1", result["version"])
        self.assertGreaterEqual(len(result["visual_projects"]), 1)
        self.assertEqual("agent_5", result["handoff"]["next_agent"])
        self.assertGreaterEqual(result["handoff"]["ready_count"], 1)
        project = result["visual_projects"][0]
        self.assertIn("storyboard", project)
        self.assertIn("scene_list", project)
        self.assertIn("shot_list", project)
        self.assertIn("color_style", project)
        self.assertIn("lighting", project)
        self.assertIn("music_style", project)
        scene = project["scenes"][0]
        self.assertIn("duration", scene)
        self.assertIn("camera", scene)
        self.assertIn("subtitle", scene)
        self.assertIn("voice_reference", scene)
        self.assertIn("image_prompt", scene)
        self.assertIn("video_prompt", scene)


    def test_visual_qa_does_not_flag_negative_safety_context(self):
        """否定/禁止语境中的风险词不应被误判为违规。"""
        result = self.run_single_code_node(
            "5. Visual QA",
            {
                "status": "visual_planned",
                "draft_visual_plans": [
                    {
                        "script_id": "safe_negation_1",
                        "video_title": "Safe Rooibos visual",
                        "visual_style": "Cozy Evening Ritual",
                        "aspect_ratio": "9:16",
                        "estimated_duration_seconds": 12,
                        "storyboard": [
                            "Show a warm Rooibos tea cup. Do not present this as a guaranteed result.",
                            "Avoid medical claims and never imply a cure.",
                        ],
                        "scenes": [
                            {
                                "scene_number": 1,
                                "start_time": "0s",
                                "end_time": "3s",
                                "duration_seconds": 3,
                                "script_section": "Hook",
                                "narration_text": "A calm Rooibos tea moment before bed.",
                                "visual_description": "Warm Rooibos tea on a bedside table. Do not present this as a guaranteed result.",
                                "shot_type": "macro close-up",
                                "camera_movement": "slow push-in",
                                "subject": "Rooibos tea cup",
                                "setting": "cozy evening bedroom",
                                "props": ["tea cup"],
                                "on_screen_text": "A calmer evening ritual",
                                "b_roll_suggestion": "steam rising from tea",
                                "image_prompt": "Vertical 9:16 composition, Rooibos tea, cozy evening lighting, no medical claims, no logos, no watermark.",
                                "video_prompt": "Vertical 9:16 video, Rooibos tea steam, avoid medical claims, no FDA badges, no doctor endorsement.",
                                "transition": "soft cut",
                                "continuity_notes": "Keep warm lighting consistent.",
                                "safety_notes": "Must not present this as treatment. Never imply a cure. No FDA badges.",
                            },
                            {
                                "scene_number": 2,
                                "start_time": "3s",
                                "end_time": "8s",
                                "duration_seconds": 5,
                                "script_section": "Body",
                                "narration_text": "Frame it as general wellness education.",
                                "visual_description": "Hands pour caffeine-free Rooibos tea without medical promises.",
                                "shot_type": "close-up",
                                "camera_movement": "slow tilt",
                                "subject": "hands pouring tea",
                                "setting": "cozy kitchen",
                                "props": ["tea pot"],
                                "on_screen_text": "General wellness only",
                                "b_roll_suggestion": "tea pour",
                                "image_prompt": "Vertical 9:16 composition, hands pouring Rooibos tea, without medical promises, no logos, no watermark.",
                                "video_prompt": "Vertical 9:16 video, tea ritual, must not present this as treatment, no medical claims.",
                                "transition": "match cut",
                                "continuity_notes": "Same cup and warm tone.",
                                "safety_notes": "Avoid saying FDA approved or doctor approved.",
                            },
                            {
                                "scene_number": 3,
                                "start_time": "8s",
                                "end_time": "12s",
                                "duration_seconds": 4,
                                "script_section": "CTA",
                                "narration_text": "Save this for a cozy evening idea.",
                                "visual_description": "Creator saves a note about a tea ritual.",
                                "shot_type": "medium lifestyle shot",
                                "camera_movement": "gentle hold",
                                "subject": "creator with notebook",
                                "setting": "evening desk",
                                "props": ["notebook", "tea cup"],
                                "on_screen_text": "Save this idea",
                                "b_roll_suggestion": "notebook and tea",
                                "image_prompt": "Vertical 9:16 composition, creator and tea, cozy lighting, no medical claims.",
                                "video_prompt": "Vertical 9:16 video, creator writing, no medical claims, no watermark.",
                                "transition": "soft fade",
                                "continuity_notes": "Same warm palette.",
                                "safety_notes": "Do not claim this can cure disease.",
                            },
                        ],
                    }
                ],
            },
        )

        plan = result["qa_visual_plans"][0]
        self.assertTrue(plan["qa_passed"])
        self.assertTrue(plan["ready_for_agent5"])
        self.assertFalse(any("guaranteed result" in issue for issue in plan["qa_issues"]))

    def test_invalid_json_returns_parse_error(self):
        """输入 JSON 格式错误时应返回 error 和 parse_error，工作流不崩溃。"""
        result = self.run_code_sequence(
            {"agent3_json": "{ bad json"},
            [
                "2. 标准化 Agent 3 JSON",
                "3. 筛选可进入 Agent 4 的脚本",
                "4. Visual Director",
                "5. Visual QA",
                "6. JSON Visual Plan + Markdown Visual Report",
            ],
        )

        self.assertEqual("error", result["status"])
        self.assertIn("Agent 3 JSON 解析失败", result["parse_error"])
        self.assertEqual([], result["visual_projects"])

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
