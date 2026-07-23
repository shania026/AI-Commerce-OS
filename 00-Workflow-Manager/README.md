# 00-Workflow-Manager：AI Health OS 工作流管理器 MVP

## 它负责什么？

Workflow Manager 是 AI Health OS 的主框架。

它不负责生成业务内容，也不负责写脚本、生成视频或发布内容。

它只负责：

1. 统一输入文件位置；
2. 调度已经完成的 Agent；
3. 把 Agent 输出统一保存到 Outputs；
4. 把给产品经理看的报告统一保存到 Reports；
5. 为后续 Agent 保留人工确认和交接入口。

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

## Agent 2 V1.0 发布说明

Agent 2 V1.0 已正式发布。

Agent 2 是独立 n8n 工作流，不会被 Workflow Manager 自动触发，仍然保留人工确认步骤。

导入文件：

```text
00-Workflow-Manager/n8n/ai-health-os-agent2-compliance-rewriter-v1.0.json
```

Agent 2 V1.0 负责：

- 接收 Agent 1 人工确认后的选题；
- 完成健康声明风险检查；
- 完成安全改写；
- 输出 JSON 和 Markdown 报告；
- 将可用选题交给 Agent 3。

Agent 2 V1.0 不负责：

- 写完整脚本；
- 生成视频；
- 发布内容；
- 开发 Agent 3。

## 注意

当前主流程仍然只自动运行 Agent 1。

请不要开发 Agent 5。

## Agent 4 v0.1 DEV 预留说明

Agent 4 Visual Director v0.1 DEV 已创建为独立 n8n 工作流，并已在 Workflow Manager 中登记接口。

导入文件：

```text
04-Video-Director/n8n/ai-health-os-agent4-visual-director-v0.1-dev.json
```

Agent 4 负责接收 Agent 3 已通过 QA 的脚本，生成镜头规划、视觉执行方案、AI 图片 Prompt、AI 视频 Prompt 和 Markdown Visual Report。

Agent 4 不会被 Workflow Manager 自动触发。必须先人工确认 Agent 3 的脚本，再单独运行 Agent 4 n8n 工作流。

当前不要开发 Agent 5。
