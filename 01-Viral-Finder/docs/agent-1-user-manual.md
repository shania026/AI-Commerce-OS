# Agent 1 用户使用手册：健康选题发现 Agent V1.1

## 1. 这个 Agent 的作用

Agent 1 是 AI Health OS 的第一个 V1.1 商业版本 Agent。

它只负责一件事：**帮助你从一批候选健康短视频选题里，选出今天最值得制作的内容。**

它会根据以下因素给选题打分：

- 好奇心：用户刷到后是否想停下来；
- 痛点强度：用户是否觉得这个问题和自己有关；
- 产品匹配度：是否方便未来带货或做联盟转化；
- 画面表现力：是否容易拍成短视频；
- 系列化潜力：是否可以持续做同类内容；
- 合规风险：是否出现治疗、治愈、疾病承诺等高风险表达。

它不会做这些事：

- 不写完整视频脚本；
- 不生成视频；
- 不自动发布；
- 不做医疗判断；
- 不开发 Agent 2。

## 2. 输入格式

输入是一个 CSV 表格。

测试文件在：

```text
01-Viral-Finder/examples/health_topics.csv
```

每一行代表一个候选选题。

必须包含这些字段：

| 字段 | 你要填写什么 |
| --- | --- |
| `title` | 选题标题 |
| `ingredient` | 相关草本、茶、食材或产品 |
| `angle` | 内容角度 |
| `target_audience` | 目标人群 |
| `curiosity` | 好奇心分数，1 到 5 |
| `pain` | 痛点强度，1 到 5 |
| `product_fit` | 产品匹配度，1 到 5 |
| `visual_potential` | 画面表现力，1 到 5 |
| `repeatability` | 系列化潜力，1 到 5 |
| `suggested_hook` | 建议的视频开头 |

如果你误填了 0、10 或 100，系统会自动把分数拉回 1 到 5。

## 3. 输出格式

输出包括两个文件：一个 JSON 文件和一个 Markdown 决策报告。

默认测试命令会生成：

```text
01-Viral-Finder/examples/ranked_health_topics.json
01-Viral-Finder/examples/ranked_health_topics.md
```

JSON 里你重点看这些字段：

| 字段 | 含义 |
| --- | --- |
| `row_number` | 这个结果来自 CSV 第几行 |
| `total_score` | 总分，越高越优先 |
| `recommendation_grade` | 推荐等级：A/B/C |
| `is_recommended_for_production` | 是否推荐制作：Yes/No |
| `recommendation_reason` | 最终推荐原因 |
| `risk_score` | 合规风险分，越高越危险 |
| `risk_alerts` | 风险提醒 |
| `score_details` | 每个字段最终使用的 1 到 5 分 |
| `score_explanation` | 为什么得到这个总分 |

## 4. Markdown 决策报告怎么看？

Markdown 报告是给产品经理看的，不是给程序看的。

报告包括：

- 今日推荐 Top 5 选题；
- 每个选题的综合评分；
- 推荐等级 A/B/C；
- 推荐制作 Yes/No；
- 推荐原因；
- 风险提醒；
- 建议优先级。

建议优先级分三种：

- `立即制作`：今天可以优先进入生产；
- `观察`：可以作为备选，先优化钩子或画面；
- `暂缓`：暂时不要直接制作。

## 5. 推荐等级怎么理解？

### A 级

优先制作。

通常说明这个选题好奇心强、痛点明确、适合产品、容易拍，也没有明显高风险疾病表达。

### B 级

可以作为备选。

通常说明这个选题有潜力，但可能钩子、画面或商业价值还可以继续优化。

### C 级

暂不推荐直接制作。

常见原因：

- 分数不够高；
- 商业价值不明显；
- 出现治疗、治愈、预防疾病等高风险表达。

## 6. 如何测试

在项目根目录运行：

```bash
python 01-Viral-Finder/health_topic_finder.py \
  --input 01-Viral-Finder/examples/health_topics.csv \
  --output 01-Viral-Finder/examples/ranked_health_topics.json \
  --limit 5
```

如果成功，你会看到类似提示：

```text
已生成 5 个优先选题：01-Viral-Finder/examples/ranked_health_topics.json
```

然后打开输出文件：

```text
01-Viral-Finder/examples/ranked_health_topics.json
01-Viral-Finder/examples/ranked_health_topics.md
```

你不需要看代码，只需要看：

1. A 级选题是否真的值得今天做；
2. B 级选题是否可以作为备选；
3. C 级选题是否确实有风险或价值不足；
4. 风险提醒是否能帮你避开违规表达。

## 7. 如何运行基础测试

如果你想确认程序本身没坏，可以运行：

```bash
python -m unittest 01-Viral-Finder/tests/test_health_topic_finder.py
```

如果看到 `OK`，说明基础测试通过。

## 8. 常见错误

### 错误 1：找不到输入文件

原因：CSV 路径写错了。

解决：确认 `--input` 后面的文件路径存在。

### 错误 2：CSV 缺少必要字段

原因：表头少了字段，比如少了 `curiosity` 或 `suggested_hook`。

解决：复制 `examples/health_topics.csv` 的第一行表头，不要随便改字段名。

### 错误 3：JSON 配置文件格式错误

原因：配置文件里少了逗号、多了逗号，或引号不完整。

解决：恢复默认配置文件，或者用 JSON 校验工具检查。

### 错误 4：输出结果和你的商业直觉不同

原因：评分权重可能不符合你的阶段目标。

解决：修改评分权重配置文件。

## 9. 如何修改评分权重

评分权重文件在：

```text
01-Viral-Finder/config/scoring_weights.json
```

默认配置是：

```json
{
  "score_weights": {
    "curiosity": 2,
    "pain": 2,
    "product_fit": 1,
    "visual_potential": 1,
    "repeatability": 1
  },
  "risk_penalty_weight": 2,
  "recommendation_thresholds": {
    "A": 25,
    "B": 18
  },
  "risk_block_score": 5
}
```

### 如果你更重视带货

把 `product_fit` 调高，例如从 `1` 改成 `2` 或 `3`。

### 如果你更重视涨粉

把 `curiosity` 和 `visual_potential` 调高。

### 如果你更保守，怕违规

把 `risk_penalty_weight` 调高，例如从 `2` 改成 `3`。

### 如果你想更严格地筛 A 级选题

把 `recommendation_thresholds` 里的 `A` 调高。

## 10. 下一步如何接入 Agent 2

现在不要开发 Agent 2。

等你确认 Agent 1 的输出符合你的选题逻辑后，Agent 2 应该只接收 Agent 1 输出里：

- `recommendation_grade` 是 `A` 或 `B`；
- `is_recommended_for_production` 是 `Yes`；
- `status` 是 `approved_for_script` 或需要人工确认后进入改写的选题。

Agent 2 的职责应该是：**健康合规改写**。

它不应该重新做选题排序，因为选题排序已经是 Agent 1 的职责。
