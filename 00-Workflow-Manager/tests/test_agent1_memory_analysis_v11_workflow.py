"""Agent 1 Memory Analysis V1.1 n8n 子工作流结构与 Code 节点测试。"""

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "n8n" / "ai-health-os-agent1-memory-analysis-v1.1.json"


class Agent1MemoryAnalysisV11WorkflowTest(unittest.TestCase):
    """确认 Agent 1 V1.1 可被 Execute Workflow 调用，并保留 Agent 2 所需输出。"""

    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW_PATH.read_text())
        cls.code_nodes = {
            node["name"]: node["parameters"]["jsCode"]
            for node in cls.workflow["nodes"]
            if node["type"] == "n8n-nodes-base.code"
        }

    def run_code_node(self, node_name, items):
        script = textwrap.dedent(
            f"""
            let items = {json.dumps(items, ensure_ascii=False)};
            items = (function(){{ const $input = {{ first(){{ return items[0]; }}, all(){{ return items; }} }};
            {self.code_nodes[node_name]}
            }})();
            if (!Array.isArray(items) || !items[0] || !items[0].json) {{ throw new Error('Invalid n8n item output'); }}
            console.log(JSON.stringify(items));
            """
        )
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write(script)
            script_path = handle.name
        result = subprocess.run(["node", script_path], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_workflow_is_callable_subworkflow_without_form_trigger(self):
        self.assertEqual("AI Health OS - Agent 1 Memory Analysis V1.1", self.workflow["name"])
        self.assertEqual("When Executed by Another Workflow", self.workflow["nodes"][0]["name"])
        self.assertEqual("n8n-nodes-base.executeWorkflowTrigger", self.workflow["nodes"][0]["type"])
        self.assertNotIn("n8n-nodes-base.formTrigger", {node["type"] for node in self.workflow["nodes"]})

    def test_code_nodes_have_valid_javascript(self):
        for node_name, code in self.code_nodes.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
                handle.write(code)
                script_path = handle.name
            result = subprocess.run(["node", "--check", script_path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"{node_name}: {result.stderr}")

    def test_rooibos_input_generates_agent2_compatible_json(self):
        items = [{"json": {
            "topic": "Rooibos Tea Before Bed",
            "product_name": "FYNELA Rooibos Tea",
            "target_audience": "US wellness audience",
            "today_limit": 5,
            "today_focus": "Rooibos tea for the US TikTok market",
            "additional_requirements": "Educational content only. Avoid medical claims.",
        }}]
        for node_name in [
            "2. 标准化上传 CSV",
            "3. CSV 转 JSON",
            "4. Agent 1 内存分析",
            "5. JSON 排名结果",
            "6. Markdown 决策报告",
        ]:
            items = self.run_code_node(node_name, items)

        output = items[0]["json"]
        self.assertTrue(output["success"])
        self.assertEqual("agent1", output["agent"])
        self.assertEqual("success", output["status"])
        self.assertEqual("json_ranking_result", output["output_type"])
        self.assertEqual("AI Health OS - Agent 1 Memory Analysis V1.1", output["workflow_name"])
        self.assertGreaterEqual(len(output["ranked_topics"]), 1)
        self.assertEqual("Rooibos Tea Before Bed", output["ranked_topics"][0]["title"])
        self.assertEqual("agent_2", output["handoff"]["next_agent"])
        self.assertGreaterEqual(output["handoff"]["ready_count"], 1)
        self.assertIn("markdown_report", output)


if __name__ == "__main__":
    unittest.main()
