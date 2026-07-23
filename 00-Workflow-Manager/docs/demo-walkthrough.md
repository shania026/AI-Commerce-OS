# AI Health OS 完整 Demo：第一次使用 Workflow Manager

这份教程假设你是第一次使用 AI Health OS，不懂代码。

你只需要记住一句话：

> 把 CSV 放到 `Inputs/`，运行 Workflow Manager，然后去 `Reports/` 看报告。

当前 Demo 只会运行 Agent 1：健康选题发现 Agent。

不会生成脚本、视频或发布内容；如需合规改写，请在人工确认后使用已发布的 Agent 2 V1.0。

## 1. 我应该把 CSV 放到哪里？

请把你的健康选题 CSV 放到这个位置：

```text
Inputs/health_topics.csv
```

也就是说：

1. 打开项目文件夹；
2. 找到 `Inputs` 文件夹；
3. 把你的 CSV 文件命名为 `health_topics.csv`；
4. 放进去。

如果你还没有自己的 CSV，可以先使用系统已经准备好的示例：

```text
Inputs/health_topics.csv
```

## 2. 如果我要分析 Rooibos，该如何准备 CSV？

CSV 的第一行必须是表头，不要改字段名：

```csv
title,ingredient,angle,target_audience,curiosity,pain,product_fit,visual_potential,repeatability,suggested_hook
```

下面是 Rooibos 示例，你可以复制到 `Inputs/health_topics.csv`：

```csv
title,ingredient,angle,target_audience,curiosity,pain,product_fit,visual_potential,repeatability,suggested_hook
Why your evening tea choice matters,Rooibos,caffeine-free evening routine,US adults who drink coffee late,5,4,5,5,5,Your night tea might be the easiest wellness swap.
The red tea South Africans drink without caffeine,Rooibos,South African botanical story,US tea beginners,5,3,5,5,4,"This red tea has no caffeine, but it is not from China."
Rooibos vs late coffee,Rooibos,evening caffeine swap,US coffee drinkers,5,5,5,4,5,"Still drinking coffee at night? Try this caffeine-free swap."
A warm caffeine-free tea ritual,Rooibos,night routine,US adults building better sleep habits,4,4,5,4,5,"Your evening routine may need a gentler drink."
Rooibos for beginners,Rooibos,beginner tea education,US tea beginners,4,3,4,4,5,"This South African red tea is naturally caffeine-free."
```

字段里的 1 到 5 分可以这样理解：

- `curiosity`：用户看到会不会好奇；
- `pain`：这个问题是不是用户真的在意；
- `product_fit`：是否适合未来带货；
- `visual_potential`：是否容易拍出画面；
- `repeatability`：是否容易做成系列。

## 3. 我应该运行哪个命令？

在项目根目录运行：

```bash
python 00-Workflow-Manager/workflow.py --limit 5
```

普通用户可以这样理解这条命令：

- `python`：让电脑运行这个工具；
- `00-Workflow-Manager/workflow.py`：运行工作流管理器；
- `--limit 5`：最多输出 5 个推荐选题。

## 4. Workflow Manager 如何调用 Agent 1？

Workflow Manager 会自动做这些事：

1. 找到 `Inputs/health_topics.csv`；
2. 调用 Agent 1：`01-Viral-Finder/health_topic_finder.py`；
3. 把 CSV 交给 Agent 1；
4. 让 Agent 1 给选题打分；
5. 让 Agent 1 生成 JSON 结果；
6. 让 Agent 1 生成 Markdown 决策报告；
7. 把结果放到统一的 `Outputs/` 和 `Reports/` 文件夹。

你不需要手动打开 Agent 1，也不需要理解 Python 代码。

## 5. 输出的 JSON 在哪里？

机器可读 JSON 会在这里：

```text
Outputs/agent1_ranked_health_topics.json
```

JSON 是给系统和未来 Agent 用的。你可以打开看，但它不是最适合普通用户阅读的版本。

## 6. Markdown 决策报告在哪里？

产品经理决策报告会在这里：

```text
Reports/agent1_decision_report.md
```

这是你最应该看的文件。

它会告诉你：

- 今日推荐 Top 5 选题；
- 每个选题的综合评分；
- 推荐等级 A/B/C；
- 是否推荐制作 Yes/No；
- 推荐原因；
- 风险提醒；
- 建议优先级：立即制作、观察、暂缓。

## 7. 如何打开报告？

你有三种简单方式。

### 方式一：在编辑器里打开

如果你正在使用 VS Code、Cursor 或类似工具：

1. 打开左侧文件列表；
2. 找到 `Reports` 文件夹；
3. 点击 `agent1_decision_report.md`。

### 方式二：用电脑文件管理器打开

1. 打开项目文件夹；
2. 打开 `Reports` 文件夹；
3. 双击 `agent1_decision_report.md`。

### 方式三：用终端快速查看

如果你愿意复制命令，可以运行：

```bash
cat Reports/agent1_decision_report.md
```

## 8. Demo 成功时你会看到什么？

运行命令后，终端会显示类似：

```text
已生成 5 个优先选题：/workspace/AI-Commerce-OS/Outputs/agent1_ranked_health_topics.json
已生成产品经理决策报告：/workspace/AI-Commerce-OS/Reports/agent1_decision_report.md

Workflow Manager 执行完成。
- 已完成：agent1｜健康选题发现 Agent：读取候选选题 CSV，输出 JSON 排序和 Markdown 决策报告。
```

看到这些内容，就说明 Demo 跑通了。

## 9. Demo 后你应该做什么？

请先打开：

```text
Reports/agent1_decision_report.md
```

然后只判断三件事：

1. A 级选题是否值得今天马上制作；
2. B 级选题是否可以继续观察或优化；
3. C 级选题是否应该暂缓，尤其是有健康合规风险的内容。

确认这个 Demo 符合你的使用习惯后，才讨论下一步。

Agent 2 V1.0 已正式发布，但需要人工确认后单独运行；当前不要开发 Agent 3。
