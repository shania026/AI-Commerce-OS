"""Agent 2 V1.1 n8n 工作流兼容 Agent E ranked_topics 输出的测试。"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[2] / "00-Workflow-Manager" / "n8n" / "ai-health-os-agent2-compliance-rewriter-v1.1.json"
ORIGINAL_WORKFLOW_PATH = Path(__file__).resolve().parents[2] / "00-Workflow-Manager" / "n8n" / "ai-health-os-agent2-compliance-rewriter-v1.0.json"


REAL_AGENT_E_OUTPUT = [
    {
        "output_type": "json_ranking_result",
        "workflow_name": "AI Health OS - Agent 1 Memory MVP v2",
        "today_limit": 5,
        "today_focus": "Rooibos tea for the US Tiktok market",
        "ranked_topics": [
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
                "reason": "推荐制作",
                "risk_level": "Low",
                "risk_alert": "偏日常健康习惯，命中低风险方向：tea。",
                "focus_bonus": 5,
                "suggested_hook": "Rooibos Tea Before Bed",
            }
        ],
    }
]


class Agent2V11WorkflowTest(unittest.TestCase):
    """确认 Agent 2 V1.1 只修复接口兼容，不重建业务流程。"""

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
        """用 Node.js 模拟 n8n Code 节点。"""
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

    def test_v11_workflow_name_and_node_names_are_preserved(self):
        """复制版应改名 V1.1，但保留 7 个节点和原节点名称。"""
        self.assertEqual("AI Health OS - Agent 2 Health Compliance Rewriter V1.1", self.workflow["name"])
        self.assertEqual(7, len(self.workflow["nodes"]))
        self.assertEqual(
            [
                "1. Agent 2 输入表单",
                "2. 标准化 Agent 1 结果",
                "3. 筛选人工确认选题",
                "4. 健康声明风险检查",
                "5. 合规安全改写",
                "6. JSON 合规结果与 Markdown 报告",
                "7. 显示 Agent 2 报告",
            ],
            [node["name"] for node in self.workflow["nodes"]],
        )

    def test_original_v10_workflow_was_not_modified(self):
        """原 Agent 2 V1.0 工作流必须仍然存在且名称不变。"""
        self.assertEqual("AI Health OS - Agent 2 Health Compliance Rewriter V1.0", self.original_workflow["name"])
        self.assertIn("ai-health-os-agent2-compliance-rewriter-v1", self.original_workflow["nodes"][0]["parameters"]["options"]["path"])

    def test_node2_extracts_ranked_topics_from_agent_e_wrapper_array(self):
        """Node 2 必须从 [{ ranked_topics: [...] }] 中提取内部 topic list。"""
        result = self.run_code_sequence(
            {"agent1_json": json.dumps(REAL_AGENT_E_OUTPUT), "approved_topics": "Rooibos Tea Before Bed"},
            ["2. 标准化 Agent 1 结果"],
        )

        self.assertEqual("parsed", result["status"])
        self.assertEqual("agent_e", result["source_agent"])
        self.assertGreaterEqual(result["total_topics"], 1)
        self.assertEqual("Rooibos Tea Before Bed", result["topics"][0]["title"])
        self.assertEqual("Rooibos Tea Before Bed", result["topics"][0]["topic"])
        self.assertEqual(4, result["topics"][0]["row_number"])

    def test_node3_matches_manual_title_without_recommendation_grade(self):
        """Node 3 应按人工填写标题匹配，即使没有 recommendation_grade。"""
        result = self.run_code_sequence(
            {"agent1_json": json.dumps(REAL_AGENT_E_OUTPUT), "approved_topics": "Rooibos Tea Before Bed"},
            ["2. 标准化 Agent 1 结果", "3. 筛选人工确认选题"],
        )

        self.assertEqual("selected", result["status"])
        self.assertEqual(1, result["selected_count"])
        self.assertEqual("Rooibos Tea Before Bed", result["selected_topics"][0]["title"])

    def test_automatic_fallback_accepts_recommendation_yes_low_risk(self):
        """approved_topics 为空时，新 Agent E recommendation=Yes 且 risk_level=Low 应可自动入选。"""
        result = self.run_code_sequence(
            {"agent1_json": json.dumps(REAL_AGENT_E_OUTPUT), "approved_topics": ""},
            ["2. 标准化 Agent 1 结果", "3. 筛选人工确认选题"],
        )

        self.assertEqual("selected", result["status"])
        self.assertEqual(1, result["selected_count"])

    def test_end_to_end_nodes_2_to_6_do_not_return_insufficient_data(self):
        """Node 6 最终输出必须包含 Rooibos 选题且 handoff.next_agent 保持 agent_3。"""
        result = self.run_code_sequence(
            {"agent1_json": json.dumps(REAL_AGENT_E_OUTPUT), "approved_topics": "Rooibos Tea Before Bed"},
            [
                "2. 标准化 Agent 1 结果",
                "3. 筛选人工确认选题",
                "4. 健康声明风险检查",
                "5. 合规安全改写",
                "6. JSON 合规结果与 Markdown 报告",
            ],
        )

        self.assertNotEqual("insufficient_data", result["status"])
        self.assertEqual("success", result["status"])
        self.assertEqual("agent_e", result["source_agent"])
        self.assertGreaterEqual(result["total_topics"], 1)
        self.assertEqual("agent_3", result["handoff"]["next_agent"])
        self.assertTrue(any("Rooibos Tea Before Bed" in item.get("original_title", "") for item in result["compliance_results"]))

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
