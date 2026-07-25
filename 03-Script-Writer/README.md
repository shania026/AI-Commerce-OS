# AI Health OS - Agent 3 Script Writer V1.0

Agent 3 是独立的英文短视频脚本生成工作流。

它接收 Agent 2 已审核通过、并标记为 `ready_for_agent3 = true` 的健康选题，然后生成适合 TikTok / Reels / Shorts 的英文短视频脚本。

Agent 3 V1.0 已正式发布。

Release Note：

- Version：V1.0
- Status：Stable
- Testing：Passed
- Ready for Agent 4

工作流名称：

```text
AI Health OS - Agent 3 Script Writer V1.0
```

## 导入文件

```text
03-Script-Writer/n8n/ai-health-os-agent3-script-writer-v1.0.json
```

## Agent 3 负责什么？

Agent 3 只负责：

- 接收 Agent 2 已审核通过的选题；
- 生成 TikTok / Reels / Shorts 英文视频脚本；
- 输出 Hook、Body、CTA；
- 输出视频标题、视频描述、建议标签、视频目标和预计时长；
- 输出 JSON 和 Markdown Script Report；
- 将脚本交给 Agent 4。

## Agent 3 不负责什么？

Agent 3 不负责：

- 图片生成；
- 视频生成；
- 配音；
- 发布；
- 开发 Agent 4。

## 7 个节点

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | Agent 3 输入表单 | 粘贴 Agent 2 JSON |
| 2 | 标准化 Agent 2 JSON | 解析 JSON 字符串、数组、对象或代码块 |
| 3 | 筛选可进入 Agent 3 的选题 | 只保留 `ready_for_agent3 = true` 的选题 |
| 4 | Script Writer | 生成英文 Hook、Body、CTA 和视频元数据 |
| 5 | Script QA | 检查 Hook、CTA 和高风险词，必要时重新生成安全表达 |
| 6 | JSON Script + Markdown Script Report | 输出机器可读 JSON 和中文/英文混合 Markdown 报告 |
| 7 | 显示 Agent 3 报告 | 用 Form Ending 显示结果 |

## 重要说明

Agent 3 不重新进行健康声明审核。它依赖 Agent 2 的合规筛查结果，并且不能重新加入 Agent 2 删除掉的高风险医疗声明。

请不要开发 Agent 4。
