# 01-Viral-Finder：健康选题发现 Agent V1.1

## 这个 Agent 负责什么？

这是 AI Health OS 的第一个 V1.1 商业版 Agent。

它只负责一件事：**从一批健康短视频选题里，挑出最适合今天优先制作的选题，并额外生成产品经理决策报告。**

它不会：

- 写完整短视频脚本；
- 生成视频；
- 自动发布；
- 判断某个草本是否真的能治疗疾病；
- 替代医生或律师。

## 为什么先做这个 Agent？

因为健康号最重要的第一步不是拍视频，而是选题。

一个好的选题要同时满足：

1. 美国用户愿意点开；
2. 和草本/产品有关系；
3. 能拍成短视频画面；
4. 不容易触碰美国健康内容合规风险。

## 需要准备什么？

你只需要准备一个 CSV 表格。可以先复制 `examples/health_topics.csv`，然后改里面的内容。

每一行就是一个候选选题。

重要字段解释：

- `title`：选题标题；
- `ingredient`：相关草本、茶、食材或产品；
- `angle`：内容角度；
- `target_audience`：目标人群；
- `curiosity`：好奇心，1 分最低，5 分最高；
- `pain`：痛点强度，1 分最低，5 分最高；
- `product_fit`：和产品的匹配度；
- `visual_potential`：是否容易拍出画面；
- `repeatability`：是否适合做成系列；
- `suggested_hook`：建议的视频开头。

## 如何测试？

在项目根目录运行：

```bash
python 01-Viral-Finder/health_topic_finder.py \
  --input 01-Viral-Finder/examples/health_topics.csv \
  --output 01-Viral-Finder/examples/ranked_health_topics.json \
  --limit 5
```

运行成功后，你会看到两个新文件：

```text
01-Viral-Finder/examples/ranked_health_topics.json
01-Viral-Finder/examples/ranked_health_topics.md
```

打开 JSON 文件，你会看到每个选题的机器可读评分；打开 Markdown 文件，你会看到产品经理可读的 Decision Report。

JSON 文件里会包含：

- `row_number`：它来自 CSV 的第几行，方便你回去修改原始表格；
- `total_score`：总分，越高越适合优先做；
- `risk_score`：合规风险分，越高越危险；
- `status`：是否可以进入脚本阶段；
- `recommendation_grade`：推荐等级，A/B/C；
- `is_recommended_for_production`：是否推荐制作，Yes/No；
- `recommendation_reason`：最终推荐理由；
- `risk_alerts`：风险提醒；
- `score_details`：每个打分字段最终使用的分数；
- `score_explanation`：哪些字段加分、哪些字段扣分、为什么得到这个总分；
- `suggested_hook`：建议钩子。

## 这次审查后修正了什么？

我检查 Agent 1 后，发现并修正了这些 MVP 阶段就应该处理的问题：

1. **CSV 表头缺失时没有友好提示**：现在会明确告诉你缺哪个字段。
2. **分数可能被误填成 0、10 或 100**：现在所有分数都会自动限制在 1 到 5。
3. **关键词匹配太粗糙**：以前 `tea` 可能误命中 `treatment`，现在使用更安全的单词边界匹配。
4. **风险检查字段不够完整**：现在会同时检查标题、草本名、角度、目标人群和钩子。
5. **输出不方便回表格修改**：现在增加 `row_number`，你可以知道结果来自 CSV 第几行。
6. **未来不好测试**：现在增加了基础测试文件，防止以后改坏 Agent 1。

## 你应该怎么判断结果？

如果 `status` 是：

- `approved_for_script`：可以进入下一个 Agent，也就是脚本 Agent；
- `needs_compliance_rewrite`：这个选题有合规风险，不能直接写脚本，需要先改表达。

## V1.1 新增：Decision Report

Agent 1 现在会在保留 JSON 输出的同时，额外生成一份中文 Markdown 报告。

报告包括：

- 今日推荐 Top 5 选题；
- 每个选题的综合评分；
- 推荐等级 A/B/C；
- 推荐制作 Yes/No；
- 推荐原因；
- 风险提醒；
- 建议优先级：立即制作、观察、暂缓。

如果你想指定报告路径，可以加 `--report` 参数。

## 可配置评分权重

评分权重已经放到单独配置文件：

```text
01-Viral-Finder/config/scoring_weights.json
```

以后你想更重视带货、涨粉或合规保守度，只需要修改这个配置文件，不需要改 Python 代码。

## 完整用户手册

更详细的中文说明在：

```text
01-Viral-Finder/docs/agent-1-user-manual.md
```

## 下一步是什么？

请先测试这个 Agent。

如果你确认结果符合你的选题逻辑，我们再继续讨论下一个 Agent；在你确认之前，本项目不会继续开发 Agent 2。


## 如何运行基础测试？

如果你想检查 Agent 1 的代码是否正常，可以运行：

```bash
python -m unittest 01-Viral-Finder/tests/test_health_topic_finder.py
```

如果看到 `OK`，说明基础测试通过。
