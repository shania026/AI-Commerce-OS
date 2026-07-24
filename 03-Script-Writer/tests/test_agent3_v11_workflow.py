"""Agent 3 V1.1 n8n 工作流兼容 Agent 2 V1.1 真实输出的测试。"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent3-script-writer-v1.1.json"
ORIGINAL_WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent3-script-writer-v1.0.json"


REAL_AGENT2_V11_OUTPUT = [
    {
        "workflow": "AI Health OS",
        "source_agent": "agent_1",
        "agent": "agent_2",
        "version": "1.1",
        "status": "success",
        "total_topics": 1,
        "approved_topics": [
            {
                "ranking": 1,
                "row_number": 4,
                "topic": "Rooibos Tea Before Bed",
                "title": "Rooibos Tea Before Bed",
                "ingredient": "Rooibos",
                "angle": "general wellness curiosity",
                "target_audience": "US wellness audience",
                "score": 24,
                "recommendation": "Yes",
                "risk_level": "Low",
                "suggested_hook": "Rooibos Tea Before Bed",
            }
        ],
        "compliance_results": [
            {
                "original_title": "Rooibos Tea Before Bed",
                "compliant_title": "Rooibos Tea Before Bed",
                "original_hook": "Rooibos Tea Before Bed",
                "compliant_hook": "Rooibos Tea Before Bed",
                "safe_core_claim": "may help support general wellness education. Do not present this as medical advice, treatment, dosage guidance, or a guaranteed result.",
                "removed_or_changed_phrases": [],
                "rewrite_explanation": "未发现明显高风险表达，保留原有吸引力，同时提醒发布前人工审核。",
                "final_risk_level": "low",
                "ready_for_agent3": True,
                "review_required": False,
            }
        ],
        "handoff": {
            "next_agent": "agent_3",
            "ready_count": 1,
            "blocked_count": 0,
            "manual_review_count": 0,
        },
    }
]


class Agent3V11WorkflowTest(unittest.TestCase):
    """确认 Agent 3 V1.1 只修复 Agent 2 V1.1 输出兼容。"""

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
        """复制版应改名 V1.1，但保留 6 个可调用节点和节点名称。"""
        self.assertEqual("AI Health OS - Agent 3 Script Writer V1.1", self.workflow["name"])
        self.assertEqual(6, len(self.workflow["nodes"]))
        self.assertEqual(
            [
                "When Executed by Another Workflow",
                "2. 标准化 Agent 2 JSON",
                "3. 筛选可进入 Agent 3 的选题",
                "4. Script Writer",
                "5. Script QA",
                "6. JSON Script + Markdown Script Report",
            ],
            [node["name"] for node in self.workflow["nodes"]],
        )

    def test_original_v10_workflow_was_not_modified(self):
        """原 Agent 3 V1.0 工作流必须仍然存在且名称不变。"""
        self.assertEqual("AI Health OS - Agent 3 Script Writer V1.0", self.original_workflow["name"])

    def test_node2_extracts_and_merges_agent2_v11_compliance_results(self):
        """Node 2 必须从外层数组中读取 compliance_results 并合并 approved_topics。"""
        result = self.run_code_sequence(
            {"agent2_json": json.dumps(REAL_AGENT2_V11_OUTPUT)},
            ["2. 标准化 Agent 2 JSON"],
        )

        self.assertEqual("parsed", result["status"])
        self.assertEqual("agent_2", result["source_agent"])
        self.assertEqual(1, result["total_topics"])
        topic = result["topics"][0]
        self.assertEqual("Rooibos Tea Before Bed", topic["title"])
        self.assertEqual("Rooibos", topic["ingredient"])
        self.assertEqual("general wellness curiosity", topic["angle"])
        self.assertEqual("US wellness audience", topic["target_audience"])
        self.assertTrue(topic["ready_for_agent3"])

    def test_node3_accepts_ready_for_agent3_truthy_values(self):
        """Node 3 应支持 true、字符串 true/Yes/yes 和数字 1。"""
        for value in [True, "true", "Yes", "yes", 1]:
            sample = json.loads(json.dumps(REAL_AGENT2_V11_OUTPUT))
            sample[0]["compliance_results"][0]["ready_for_agent3"] = value
            result = self.run_code_sequence(
                {"agent2_json": json.dumps(sample)},
                ["2. 标准化 Agent 2 JSON", "3. 筛选可进入 Agent 3 的选题"],
            )
            self.assertEqual("ready_for_script", result["status"])
            self.assertEqual(1, result["selected_count"])

    def test_end_to_end_generates_script_from_real_agent2_v11_output(self):
        """真实 Agent 2 V1.1 输出应生成脚本并交给 Agent 4。"""
        result = self.run_code_sequence(
            {"agent2_json": json.dumps(REAL_AGENT2_V11_OUTPUT)},
            [
                "2. 标准化 Agent 2 JSON",
                "3. 筛选可进入 Agent 3 的选题",
                "4. Script Writer",
                "5. Script QA",
                "6. JSON Script + Markdown Script Report",
            ],
        )

        self.assertEqual("success", result["status"])
        self.assertEqual("agent_2", result["source_agent"])
        self.assertEqual("agent_3", result["agent"])
        self.assertEqual("1.1", result["version"])
        self.assertGreaterEqual(len(result["scripts"]), 1)
        self.assertEqual("agent_4", result["handoff"]["next_agent"])
        self.assertGreaterEqual(result["handoff"]["ready_count"], 1)
        self.assertIn("Rooibos Tea Before Bed", result["scripts"][0]["video_title"])

    def test_no_ready_topic_returns_insufficient_data(self):
        """确实没有 ready_for_agent3=true 时才返回 insufficient_data。"""
        sample = json.loads(json.dumps(REAL_AGENT2_V11_OUTPUT))
        sample[0]["compliance_results"][0]["ready_for_agent3"] = False
        result = self.run_code_sequence(
            {"agent2_json": json.dumps(sample)},
            [
                "2. 标准化 Agent 2 JSON",
                "3. 筛选可进入 Agent 3 的选题",
                "4. Script Writer",
                "5. Script QA",
                "6. JSON Script + Markdown Script Report",
            ],
        )

        self.assertEqual("insufficient_data", result["status"])
        self.assertEqual([], result["scripts"])

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
