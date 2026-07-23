# Workflow 使用手册（普通用户版）

## 1. Workflow Manager 是什么？

Workflow Manager 是 AI Health OS 的总调度器。

你可以把它理解成“项目经理”：

- 它不亲自写内容；
- 它不生成视频；
- 它不发布 TikTok；
- 它只负责按顺序调用已经完成的 Agent。

当前 MVP 只调用 Agent 1。

## 2. 你需要准备什么？

你只需要准备一个健康选题 CSV 文件：

```text
Inputs/health_topics.csv
```

如果你不知道怎么写，可以先参考这个文件：

```text
01-Viral-Finder/examples/health_topics.csv
```

## 3. 如何运行整个流程？

在项目根目录运行：

```bash
python 00-Workflow-Manager/workflow.py --limit 5
```

这条命令的意思是：

- 调用 Workflow Manager；
- 让它运行 Agent 1；
- 最多输出 5 个推荐选题。

## 4. 运行后看哪里？

运行完成后，你会得到两个核心文件。

机器可读结果：

```text
Outputs/agent1_ranked_health_topics.json
```

产品经理决策报告：

```text
Reports/agent1_decision_report.md
```

如果你不是程序员，请优先打开 Markdown 报告。

## 5. 如何判断是否成功？

成功时，终端会显示类似：

```text
Workflow Manager 执行完成。
- 已完成：agent1｜健康选题发现 Agent：读取候选选题 CSV，输出 JSON 排序和 Markdown 决策报告。
```

并且你能在 `Reports/` 里看到决策报告。

## 6. 常见错误

### 错误 1：找不到 Inputs/health_topics.csv

说明你还没有准备输入文件。

解决方法：

1. 打开 `Inputs/` 文件夹；
2. 新建或复制一个 `health_topics.csv`；
3. 再运行 Workflow Manager。

### 错误 2：CSV 字段不对

说明你的 CSV 表头缺字段或字段名写错。

解决方法：复制 `01-Viral-Finder/examples/health_topics.csv` 的第一行表头。

### 错误 3：我看到 JSON，但看不懂

这是正常的。JSON 是给系统和后续 Agent 用的。

你应该优先看：

```text
Reports/agent1_decision_report.md
```

## 7. 下一步如何接入 Agent 2？

现在不要开发 Agent 2。

Workflow Manager 已经预留了 Agent 注册表。以后接入 Agent 2 时，只需要：

1. 先确认 Agent 2 已经单独开发完成；
2. 再把 Agent 2 登记到 `workflow.py`；
3. 让 Workflow Manager 在 Agent 1 后面调用 Agent 2。

但这一步必须等你确认后再做。
