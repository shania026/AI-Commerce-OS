# 00-Workflow-Manager：AI Health OS 工作流管理器 MVP

## 它负责什么？

Workflow Manager 是 AI Health OS 的主框架。

它不负责生成业务内容，也不负责写脚本、生成视频或发布内容。

它只负责：

1. 统一输入文件位置；
2. 调度已经完成的 Agent；
3. 把 Agent 输出统一保存到 Outputs；
4. 把给产品经理看的报告统一保存到 Reports；
5. 为以后接入 Agent 2、Agent 3 预留入口。

## 当前 MVP 做了什么？

当前只调度一个已经完成的 Agent：

```text
Agent 1：健康选题发现 Agent
```

Workflow Manager 会读取：

```text
Inputs/health_topics.csv
```

然后生成：

```text
Outputs/agent1_ranked_health_topics.json
Reports/agent1_decision_report.md
```

## 如何运行？

在项目根目录运行：

```bash
python 00-Workflow-Manager/workflow.py --limit 5
```

运行完成后，请优先打开：

```text
Reports/agent1_decision_report.md
```

这份 Markdown 报告是给产品经理看的，比 JSON 更容易阅读。

## 完整 Demo 教程

如果你是第一次使用，请先看这份普通用户教程：

```text
00-Workflow-Manager/docs/demo-walkthrough.md
```

## n8n 可导入工作流

如果你不想手动创建 n8n 节点，可以直接导入这个文件：

```text
00-Workflow-Manager/n8n/ai-health-os-daily-topic-workflow.json
```

导入和 Docker 路径说明请看：

```text
00-Workflow-Manager/n8n/README.md
```

这个导入版不使用 Execute Command 节点，避免部分 n8n Docker / n8n 2.x 环境显示 Unknown Node。

## 注意

请不要在这个阶段开发 Agent 2。

只有当你确认 Workflow Manager 能稳定调度 Agent 1 后，才讨论下一步是否接入 Agent 2。
