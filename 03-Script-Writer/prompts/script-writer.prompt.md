# Prompt：AI Health OS - Agent 3 Script Writer V1.0

Agent 3 V1.0 已正式发布。

Release Note：

- Version：V1.0
- Status：Stable
- Testing：Passed
- Ready for Agent 4

请维护或生成独立的 n8n 工作流：

```text
AI Health OS - Agent 3 Script Writer V1.0
```

## 边界

不要修改 Workflow Manager、Agent 1 或 Agent 2。

不要开发 Agent 4。

## Agent 3 职责

Agent 3 只负责：

- 接收 Agent 2 已审核通过的选题；
- 生成 TikTok / Reels / Shorts 英文视频脚本；
- 输出 Hook、Body、CTA；
- 输出视频标题、视频描述、建议标签、视频目标和预计时长；
- 输出 JSON 和 Markdown Script Report；
- 将脚本交给 Agent 4。

## Agent 3 不负责

Agent 3 不负责：

- 图片生成；
- 视频生成；
- 配音；
- 发布；
- 开发 Agent 4。

## 必须保留 7 个节点

1. Agent 3 输入表单
2. 标准化 Agent 2 JSON
3. 筛选可进入 Agent 3 的选题
4. Script Writer
5. Script QA
6. JSON Script + Markdown Script Report
7. 显示 Agent 3 报告

连接方式必须保持：

```text
1 → 2 → 3 → 4 → 5 → 6 → 7
```

## 输出要求

JSON 顶层必须包含：

- workflow
- agent
- version
- status
- scripts
- handoff

其中：

```text
handoff.next_agent = agent_4
```

Markdown 必须以以下标题开头：

```text
# Agent 3 Script Report
```

如果没有 `ready_for_agent3 = true` 的选题，必须返回 `status = insufficient_data`，不要生成脚本。
