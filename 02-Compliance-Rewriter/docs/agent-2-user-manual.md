# Agent 2 V1.0 用户使用手册

Agent 2 V1.0 已正式发布。

这份手册写给普通用户和产品经理，不假设你会编程。

## 1. Agent 2 是什么？

Agent 2 是 AI Health OS 的健康合规改写 Agent。

它的作用是：把 Agent 1 已经筛选出来、并且由你人工确认的健康选题，进行一次风险检查和安全改写。

## 2. Agent 2 V1.0 负责什么？

Agent 2 V1.0 负责：

- 接收 Agent 1 人工确认后的选题；
- 完成健康声明风险检查；
- 完成安全改写；
- 输出 JSON 和 Markdown 报告；
- 将可用选题交给未来 Agent 3。

## 3. Agent 2 V1.0 不负责什么？

Agent 2 V1.0 不负责：

- 写完整脚本；
- 生成视频；
- 发布内容；
- 提供医疗或法律意见；
- 保证内容一定符合所有法规或平台规则；
- 开发 Agent 3。

## 4. 我每天怎么用？

### 第一步：先运行 Agent 1

你先用 Agent 1 得到健康选题排名结果。

### 第二步：人工确认 2–5 个选题

你从 Agent 1 的结果里选出今天想继续处理的 2–5 个选题。

### 第三步：打开 Agent 2 V1.0 n8n 工作流

工作流名称是：

```text
AI Health OS - Agent 2 Health Compliance Rewriter V1.0
```

### 第四步：填写表单

表单里有两个字段：

1. `agent1_json`：把 Agent 1 的 JSON 结果粘贴进去。
2. `approved_topics`：填写你人工确认的选题编号或名称。

如果你不填写 `approved_topics`，Agent 2 会默认选择 Agent 1 中 A/B 且 Yes 的前 5 个选题。

### 第五步：查看报告

提交后，n8n 会显示中文 Markdown 合规改写报告。

你重点看：

- 哪些选题可以进入未来 Agent 3；
- 哪些选题需要人工复核；
- 哪些选题被拦截；
- 标题和 Hook 被改成了什么；
- 哪些高风险表达被修改或移除。

## 5. 导入哪个文件？

请导入：

```text
00-Workflow-Manager/n8n/ai-health-os-agent2-compliance-rewriter-v1.0.json
```

## 6. 重要说明

本工具仅用于内容风险筛查和谨慎改写，不构成医疗、法律或平台合规意见。最终发布前仍需人工审核。
