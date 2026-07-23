"""
AI Health OS - Agent 1: 健康选题发现 Agent V1.1

这个脚本的目标：
1. 读取一组健康短视频选题候选；
2. 根据配置文件里的商业权重打分；
3. 输出产品经理能看懂的推荐等级、推荐原因、风险提醒和 Markdown 决策报告。

V1.1 边界：
- 只做选题排序，不写脚本、不生成视频、不发布内容。
- 只使用 Python 标准库，不需要安装第三方包。
- 这是选题辅助工具，不是医疗、法律或平台合规意见。
"""

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


# 默认配置文件路径。产品经理以后只改这个 JSON 文件，不需要改 Python 代码。
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config" / "scoring_weights.json"

# CSV 必须包含的字段。先把输入格式固定住，后面其他 Agent 才容易复用。
REQUIRED_FIELDS = [
    "title",
    "ingredient",
    "angle",
    "target_audience",
    "curiosity",
    "pain",
    "product_fit",
    "visual_potential",
    "repeatability",
    "suggested_hook",
]

# 所有人工打分字段都限制在 1 到 5 分，避免有人误填 10 或 100 后把排序带偏。
SCORE_FIELDS = ["curiosity", "pain", "product_fit", "visual_potential", "repeatability"]
MIN_SCORE = 1
MAX_SCORE = 5
DEFAULT_SCORE = 3

# 这些词会让内容在美国市场更容易有合规风险。
# 不是说完全不能讨论，而是 V1.1 阶段先自动降权或拦截，避免账号早期踩线。
HIGH_RISK_WORDS = [
    "cure",
    "cures",
    "treat",
    "treats",
    "treatment",
    "prevent",
    "prevents",
    "prevention",
    "reverse",
    "reverses",
    "detox",
    "cleanse blood",
    "diabetes",
    "cancer",
    "hypertension",
    "fatty liver",
    "arthritis",
]

# 这些词更适合健康号做科普和生活方式内容。
# 它们通常偏「日常习惯」和「身体感受」，比疾病治疗更安全。
LOW_RISK_WELLNESS_WORDS = [
    "sleep",
    "energy",
    "hydration",
    "caffeine",
    "digestion",
    "bloating",
    "evening routine",
    "tea",
    "stress",
    "screen fatigue",
]

# 字段中文名用于解释分数，让 JSON 更适合产品经理阅读。
FIELD_LABELS = {
    "curiosity": "好奇心",
    "pain": "痛点强度",
    "product_fit": "产品匹配度",
    "visual_potential": "画面表现力",
    "repeatability": "系列化潜力",
}


def read_topics(input_path: Path) -> List[Dict[str, str]]:
    """读取 CSV 选题表，并检查表头是否符合 V1.1 约定。"""
    if not input_path.exists():
        raise FileNotFoundError(f"找不到输入文件：{input_path}")

    with input_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        validate_required_fields(reader.fieldnames or [])
        return list(reader)


def load_config(config_path: Path) -> Dict[str, object]:
    """读取评分配置文件，让商业权重可以不改代码直接调整。"""
    if not config_path.exists():
        raise FileNotFoundError(f"找不到评分配置文件：{config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    validate_config(config)
    return config


def validate_config(config: Dict[str, object]) -> None:
    """检查评分配置是否完整，避免配置写错后产生难懂结果。"""
    score_weights = config.get("score_weights", {})
    missing_weights = [field for field in SCORE_FIELDS if field not in score_weights]
    if missing_weights:
        raise ValueError(f"评分配置缺少权重字段：{', '.join(missing_weights)}")

    thresholds = config.get("recommendation_thresholds", {})
    if "A" not in thresholds or "B" not in thresholds:
        raise ValueError("评分配置缺少推荐等级阈值：A 或 B")


def validate_required_fields(fieldnames: Sequence[str]) -> None:
    """检查 CSV 是否缺少必要字段；缺字段时给出产品经理能看懂的错误。"""
    missing_fields = [field for field in REQUIRED_FIELDS if field not in fieldnames]
    if missing_fields:
        joined_fields = ", ".join(missing_fields)
        raise ValueError(f"CSV 缺少必要字段：{joined_fields}")


def normalize_text(text: str) -> str:
    """统一大小写和空格，方便后面做关键词识别。"""
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_keywords(text: str, words: Iterable[str]) -> List[str]:
    """查找命中的关键词，使用单词边界，避免 tea 误命中 treatment 这类情况。"""
    normalized_text = normalize_text(text)
    matched_words = []

    for word in words:
        normalized_word = normalize_text(word)
        # (?<!\w) 和 (?!\w) 表示关键词两边不能是字母、数字或下划线。
        # 这样可以匹配 tea，但不会把 treatment 里的 tea 当成低风险 tea。
        pattern = rf"(?<!\w){re.escape(normalized_word)}(?!\w)"
        if re.search(pattern, normalized_text):
            matched_words.append(word)

    return matched_words


def to_score(value: str, default: int = DEFAULT_SCORE) -> int:
    """把 CSV 里的分数字段转成 1 到 5 的整数。"""
    try:
        score = int(value)
    except (TypeError, ValueError):
        score = default

    # 把异常分数拉回 1 到 5，避免一个误填数字破坏整个排序。
    return max(MIN_SCORE, min(MAX_SCORE, score))


def to_number(value: object, default: int) -> int:
    """把配置文件里的数字转成整数；如果配置写错，就使用默认值。"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def combined_topic_text(topic: Dict[str, str]) -> str:
    """把需要检查风险的字段合并成一段文字。"""
    return " ".join(
        [
            topic.get("title", ""),
            topic.get("ingredient", ""),
            topic.get("angle", ""),
            topic.get("target_audience", ""),
            topic.get("suggested_hook", ""),
        ]
    )


def build_score_breakdown(field_scores: Dict[str, int], config: Dict[str, object], risk_score: int) -> Dict[str, object]:
    """生成加分、扣分和总分解释。"""
    score_weights = config["score_weights"]
    risk_penalty_weight = to_number(config.get("risk_penalty_weight"), 2)
    positive_points = []
    total_positive_score = 0

    for field in SCORE_FIELDS:
        score = field_scores[field]
        weight = to_number(score_weights.get(field), 1)
        contribution = score * weight
        total_positive_score += contribution
        positive_points.append(
            {
                "field": field,
                "label": FIELD_LABELS[field],
                "score": score,
                "weight": weight,
                "contribution": contribution,
                "explanation": f"{FIELD_LABELS[field]} {score} 分，权重 {weight}，贡献 {contribution} 分。",
            }
        )

    risk_penalty = risk_score * risk_penalty_weight
    total_score = total_positive_score - risk_penalty

    return {
        "positive_points": positive_points,
        "negative_points": [
            {
                "field": "risk_score",
                "label": "合规风险扣分",
                "score": risk_score,
                "weight": risk_penalty_weight,
                "contribution": -risk_penalty,
                "explanation": f"合规风险 {risk_score} 分，扣分权重 {risk_penalty_weight}，扣 {risk_penalty} 分。",
            }
        ],
        "total_positive_score": total_positive_score,
        "total_negative_score": -risk_penalty,
        "total_score": total_score,
        "score_formula": "总分 = 各字段分数 × 对应权重 - 合规风险分 × 风险扣分权重",
    }


def recommendation_grade(total_score: int, risk_score: int, config: Dict[str, object]) -> str:
    """把数字总分转换成产品经理更好理解的 A/B/C 推荐等级。"""
    risk_block_score = to_number(config.get("risk_block_score"), 5)
    thresholds = config["recommendation_thresholds"]
    a_threshold = to_number(thresholds.get("A"), 25)
    b_threshold = to_number(thresholds.get("B"), 18)

    if risk_score >= risk_block_score:
        return "C"
    if total_score >= a_threshold:
        return "A"
    if total_score >= b_threshold:
        return "B"
    return "C"


def build_recommendation_reason(title: str, grade: str, field_scores: Dict[str, int], risk_score: int) -> str:
    """生成一句最终推荐理由，方便产品经理快速判断是否制作。"""
    strong_fields = [FIELD_LABELS[field] for field, score in field_scores.items() if score >= 4]
    strong_text = "、".join(strong_fields) if strong_fields else "基础分"

    if grade == "A":
        return f"推荐优先制作《{title}》，因为它在{strong_text}上表现强，且风险可控。"
    if grade == "B":
        return f"可以作为备选制作《{title}》，它有一定潜力，但需要进一步优化钩子或商业角度。"
    if risk_score >= 5:
        return f"暂不推荐直接制作《{title}》，因为存在明显健康合规风险，应先人工改写。"
    return f"暂不优先制作《{title}》，因为综合商业价值不够突出。"


def score_topic(topic: Dict[str, str], row_number: int, config: Dict[str, object]) -> Dict[str, object]:
    """给单个选题打分，并输出可解释的商业推荐结果。"""
    text_for_risk_check = combined_topic_text(topic)
    high_risk_matches = find_keywords(text_for_risk_check, HIGH_RISK_WORDS)
    wellness_matches = find_keywords(text_for_risk_check, LOW_RISK_WELLNESS_WORDS)

    field_scores = {field: to_score(topic.get(field, "")) for field in SCORE_FIELDS}

    risk_score = 1
    risk_alerts = []

    if high_risk_matches:
        risk_score = 5
        risk_alerts.append(f"包含高风险健康词：{', '.join(high_risk_matches)}。发布前必须人工改写。")
    elif wellness_matches:
        risk_score = 2
        risk_alerts.append(f"偏日常健康习惯，命中低风险方向：{', '.join(wellness_matches)}。")
    else:
        risk_alerts.append("未发现明显高风险词，但仍需人工确认。")

    breakdown = build_score_breakdown(field_scores, config, risk_score)
    total_score = int(breakdown["total_score"])
    grade = recommendation_grade(total_score, risk_score, config)
    is_recommended = "Yes" if grade in ["A", "B"] else "No"
    title = topic.get("title", "").strip()
    recommendation_reason = build_recommendation_reason(title, grade, field_scores, risk_score)

    status = "approved_for_script"
    if risk_score >= to_number(config.get("risk_block_score"), 5):
        status = "needs_compliance_rewrite"

    return {
        "row_number": row_number,
        "title": title,
        "ingredient": topic.get("ingredient", "").strip(),
        "angle": topic.get("angle", "").strip(),
        "target_audience": topic.get("target_audience", "US wellness audience").strip(),
        "total_score": total_score,
        "recommendation_grade": grade,
        "is_recommended_for_production": is_recommended,
        "recommendation_reason": recommendation_reason,
        "risk_score": risk_score,
        "risk_alerts": risk_alerts,
        "status": status,
        "score_details": field_scores,
        "score_explanation": breakdown,
        "suggested_hook": topic.get("suggested_hook", "").strip(),
    }


def rank_topics(topics: List[Dict[str, str]], limit: int, config: Dict[str, object]) -> List[Dict[str, object]]:
    """给所有选题打分，并按总分从高到低排序；同分时保持原始顺序更好理解。"""
    safe_limit = max(1, limit)
    scored_topics = [score_topic(topic, index + 2, config) for index, topic in enumerate(topics)]
    return sorted(scored_topics, key=lambda item: (-int(item["total_score"]), int(item["row_number"])))[:safe_limit]


def suggested_priority(topic: Dict[str, object]) -> str:
    """把推荐等级和风险状态转换成产品经理每天排期用的优先级。"""
    if topic["recommendation_grade"] == "A" and topic["is_recommended_for_production"] == "Yes":
        return "立即制作"
    if topic["recommendation_grade"] == "B" and topic["is_recommended_for_production"] == "Yes":
        return "观察"
    return "暂缓"


def default_report_path(output_path: Path) -> Path:
    """如果用户没有指定报告路径，就在 JSON 输出旁边生成同名 Markdown 报告。"""
    return output_path.with_suffix(".md")


def markdown_escape(value: object) -> str:
    """简单处理 Markdown 表格里的竖线，避免表格格式被破坏。"""
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_decision_report(topics: List[Dict[str, object]]) -> str:
    """生成产品经理可直接阅读的中文 Decision Report。"""
    lines = [
        "# Agent 1 V1.1 Decision Report：今日健康选题决策报告",
        "",
        "## 使用说明",
        "",
        "这份报告只用于决定今天优先制作哪些健康短视频选题。",
        "Agent 1 仍然只负责选题排序和决策辅助，不负责写脚本、生成视频、发布内容，也不开发 Agent 2。",
        "",
        "## 今日推荐 Top 5 选题",
        "",
        "| 排名 | 选题 | 综合评分 | 推荐等级 | 推荐制作 | 建议优先级 |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]

    for index, topic in enumerate(topics[:5], start=1):
        lines.append(
            "| {rank} | {title} | {score} | {grade} | {recommended} | {priority} |".format(
                rank=index,
                title=markdown_escape(topic["title"]),
                score=topic["total_score"],
                grade=topic["recommendation_grade"],
                recommended=topic["is_recommended_for_production"],
                priority=suggested_priority(topic),
            )
        )

    lines.extend(["", "## 单条选题决策详情", ""])

    for index, topic in enumerate(topics[:5], start=1):
        risk_alerts = "；".join(str(alert) for alert in topic["risk_alerts"])
        lines.extend(
            [
                f"### {index}. {topic['title']}",
                "",
                f"- 综合评分：{topic['total_score']}",
                f"- 推荐等级：{topic['recommendation_grade']}",
                f"- 推荐制作：{topic['is_recommended_for_production']}",
                f"- 建议优先级：{suggested_priority(topic)}",
                f"- 推荐原因：{topic['recommendation_reason']}",
                f"- 风险提醒：{risk_alerts}",
                "",
            ]
        )

    lines.extend(
        [
            "## 决策建议",
            "",
            "- `立即制作`：适合作为今天优先生产的内容。",
            "- `观察`：可以作为备选，建议先优化钩子、画面或商业角度。",
            "- `暂缓`：暂时不要直接制作，尤其是涉及高风险健康表达时。",
            "",
            "## 下一步",
            "",
            "请先人工确认这份报告。确认前不要开发 Agent 2。",
        ]
    )

    return "\n".join(lines) + "\n"


def save_decision_report(report_path: Path, topics: List[Dict[str, object]]) -> None:
    """保存 Markdown 决策报告，给产品经理直接阅读。"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_decision_report(topics), encoding="utf-8")


def save_json(output_path: Path, data: List[Dict[str, object]]) -> None:
    """把结果保存成 JSON 文件，方便产品经理查看。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def build_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器，单独拆出来方便未来测试和扩展。"""
    parser = argparse.ArgumentParser(description="AI Health OS 健康选题发现 Agent V1.1")
    parser.add_argument("--input", required=True, help="输入 CSV 文件路径")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    parser.add_argument("--limit", type=int, default=5, help="最多输出几个选题，默认 5 个")
    parser.add_argument("--report", help="Markdown 决策报告输出路径；不填时默认生成在 JSON 输出旁边")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="评分配置 JSON 文件路径；默认使用 01-Viral-Finder/config/scoring_weights.json",
    )
    return parser


def main() -> None:
    """命令行入口：读取输入 CSV 和评分配置，输出排序后的 JSON。"""
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config(Path(args.config))
        topics = read_topics(Path(args.input))
        output_path = Path(args.output)
        report_path = Path(args.report) if args.report else default_report_path(output_path)
        ranked_topics = rank_topics(topics, args.limit, config)
        save_json(output_path, ranked_topics)
        save_decision_report(report_path, ranked_topics)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        # 这里捕获的是用户输入类错误，不是隐藏程序错误。
        # 产品经理看到中文错误后，可以直接检查 CSV、配置文件路径或 JSON 格式。
        parser.error(str(error))

    print(f"已生成 {len(ranked_topics)} 个优先选题：{args.output}")
    print(f"已生成产品经理决策报告：{report_path}")


if __name__ == "__main__":
    main()
