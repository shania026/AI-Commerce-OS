# AI Health OS - Agent 2 Health Compliance Rewriter V1.0

Agent 2 V1.0 已正式发布。

Agent 2 是 AI Health OS 的第二个 Agent。它接收 Agent 1 已经输出、并且经过人工确认的健康选题，完成健康声明风险检查和安全改写，然后输出机器可读 JSON 和产品经理可读的中文 Markdown 报告。

当前版本只提供独立 n8n 工作流，不会修改 Agent 1，也不会开发 Agent 3。

## 导入文件

```text
00-Workflow-Manager/n8n/ai-health-os-agent2-compliance-rewriter-v1.0.json
```

导入 n8n 后 workflow 名称：

```text
AI Health OS - Agent 2 Health Compliance Rewriter V1.0
```

## Agent 2 V1.0 职责

- 接收 Agent 1 人工确认后的选题；
- 完成健康声明风险检查；
- 完成安全改写；
- 输出 JSON 和 Markdown 报告；
- 将可用选题交给未来 Agent 3。

## Agent 2 V1.0 不负责

- 不写完整脚本；
- 不生成视频；
- 不发布内容；
- 不提供医疗或法律意见；
- 不保证内容一定符合所有法规或平台规则；
- 不开发 Agent 3。

## 输入

Agent 2 V1.0 的 n8n 表单包含两个字段：

1. `agent1_json`：必填，用来粘贴 Agent 1 输出的 JSON。
2. `approved_topics`：可选，用来填写人工确认的选题名称或编号。

## 输出

Agent 2 V1.0 输出：

1. 机器可读 JSON 合规结果；
2. 中文 Markdown 合规改写报告。

## 重要说明

本工具仅用于内容风险筛查和谨慎改写，不构成医疗、法律或平台合规意见。最终发布前仍需人工审核。
