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

    def test_v11_workflow_name_and_nodes_are_preserved(self):
        """复制版应改名 V1.1，但保留 7 个节点和节点名称。"""
        self.assertEqual("AI Health OS - Agent 4 Visual Director V1.1", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertEqual(
            [
                "1. Agent 4 输入表单",
                "2. 标准化 Agent 3 JSON",
                "3. 筛选可进入 Agent 4 的脚本",
                "4. Visual Director",
                "5. Visual QA",
                "6. JSON Visual Plan + Markdown Visual Report",
                "7. 显示 Agent 4 报告",
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
