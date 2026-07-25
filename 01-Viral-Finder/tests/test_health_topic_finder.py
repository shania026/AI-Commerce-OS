"""Agent 1 的基础测试，确保 V1.1 商业评分和决策报告和风险识别不会明显跑偏。"""

import importlib.util
import unittest
from pathlib import Path


# 目录名里有连字符，不能直接 import，所以用文件路径加载脚本。
MODULE_PATH = Path(__file__).resolve().parents[1] / "health_topic_finder.py"
spec = importlib.util.spec_from_file_location("health_topic_finder", MODULE_PATH)
health_topic_finder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health_topic_finder)


TEST_CONFIG = {
    "score_weights": {
        "curiosity": 2,
        "pain": 2,
        "product_fit": 1,
        "visual_potential": 1,
        "repeatability": 1,
    },
    "risk_penalty_weight": 2,
    "recommendation_thresholds": {"A": 25, "B": 18},
    "risk_block_score": 5,
}


class HealthTopicFinderTest(unittest.TestCase):
    """检查健康选题发现 Agent 的关键 V1.1 行为。"""

    def test_high_risk_claim_is_not_recommended(self):
        """包含 cure 和 diabetes 的选题必须进入合规改写状态，并不推荐直接制作。"""
        topic = {
            "title": "This herb cures diabetes",
            "ingredient": "Devil's claw",
            "angle": "disease treatment claim",
            "target_audience": "People with diabetes",
            "curiosity": "5",
            "pain": "5",
            "product_fit": "3",
            "visual_potential": "3",
            "repeatability": "2",
            "suggested_hook": "This herb cures diabetes naturally.",
        }

        result = health_topic_finder.score_topic(topic, row_number=2, config=TEST_CONFIG)

        self.assertEqual(result["risk_score"], 5)
        self.assertEqual(result["status"], "needs_compliance_rewrite")
        self.assertEqual(result["recommendation_grade"], "C")
        self.assertEqual(result["is_recommended_for_production"], "No")
        self.assertIn("cures", result["risk_alerts"][0])

    def test_tea_does_not_match_inside_treatment(self):
        """tea 不能误命中 treatment，否则低风险识别会产生噪音。"""
        matches = health_topic_finder.find_keywords("disease treatment claim", ["tea"])

        self.assertEqual(matches, [])

    def test_scores_are_clamped_to_one_to_five(self):
        """误填 100 或 0 时，系统要自动拉回 1 到 5。"""
        self.assertEqual(health_topic_finder.to_score("100"), 5)
        self.assertEqual(health_topic_finder.to_score("0"), 1)
        self.assertEqual(health_topic_finder.to_score("not-a-number"), 3)

    def test_missing_required_fields_raise_clear_error(self):
        """CSV 缺表头时，要给出明确错误，方便非程序员修正。"""
        with self.assertRaises(ValueError) as context:
            health_topic_finder.validate_required_fields(["title"])

        self.assertIn("CSV 缺少必要字段", str(context.exception))

    def test_explainability_fields_are_present(self):
        """V1.1 必须继续输出推荐等级、推荐原因和评分解释。"""
        topic = {
            "title": "Why your evening tea choice matters",
            "ingredient": "Rooibos",
            "angle": "caffeine-free evening routine",
            "target_audience": "US adults who drink coffee late",
            "curiosity": "5",
            "pain": "4",
            "product_fit": "5",
            "visual_potential": "5",
            "repeatability": "5",
            "suggested_hook": "Your night tea might be the easiest wellness swap.",
        }

        result = health_topic_finder.score_topic(topic, row_number=2, config=TEST_CONFIG)

        self.assertEqual(result["recommendation_grade"], "A")
        self.assertEqual(result["is_recommended_for_production"], "Yes")
        self.assertIn("推荐优先制作", result["recommendation_reason"])
        self.assertIn("positive_points", result["score_explanation"])
        self.assertIn("negative_points", result["score_explanation"])

    def test_config_must_include_all_score_weights(self):
        """配置文件缺少权重时，要直接报错，避免悄悄算错商业分。"""
        broken_config = {"score_weights": {}, "recommendation_thresholds": {"A": 25, "B": 18}}

        with self.assertRaises(ValueError) as context:
            health_topic_finder.validate_config(broken_config)

        self.assertIn("评分配置缺少权重字段", str(context.exception))

    def test_decision_report_contains_pm_sections(self):
        """V1.1 必须生成产品经理能直接阅读的 Markdown 决策报告。"""
        topic = {
            "title": "Why your evening tea choice matters",
            "ingredient": "Rooibos",
            "angle": "caffeine-free evening routine",
            "target_audience": "US adults who drink coffee late",
            "curiosity": "5",
            "pain": "4",
            "product_fit": "5",
            "visual_potential": "5",
            "repeatability": "5",
            "suggested_hook": "Your night tea might be the easiest wellness swap.",
        }
        ranked_topics = [health_topic_finder.score_topic(topic, row_number=2, config=TEST_CONFIG)]

        report = health_topic_finder.build_decision_report(ranked_topics)

        self.assertIn("今日推荐 Top 5 选题", report)
        self.assertIn("综合评分", report)
        self.assertIn("推荐等级", report)
        self.assertIn("推荐制作", report)
        self.assertIn("推荐原因", report)
        self.assertIn("风险提醒", report)
        self.assertIn("立即制作", report)
        self.assertIn("不要开发 Agent 2", report)

    def test_default_report_path_keeps_json_interface(self):
        """不改变 JSON 输出参数，只在旁边生成同名 Markdown 报告路径。"""
        report_path = health_topic_finder.default_report_path(Path("ranked_health_topics.json"))

        self.assertEqual(report_path, Path("ranked_health_topics.md"))


if __name__ == "__main__":
    unittest.main()
