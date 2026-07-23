# AI Health OS - Agent 4 Visual Director v0.1 DEV

Agent 4 是独立的视觉导演工作流。

它接收 Agent 3 已生成并通过 QA 的短视频脚本，为每条脚本生成适合 TikTok / Reels / Shorts 的视觉执行方案，包括镜头规划、画面描述、AI 图片 Prompt、AI 视频 Prompt、屏幕文字、B-roll 建议和镜头节奏。

## 当前状态

- Version：v0.1 DEV
- Status：Development
- 输入来源：Agent 3 Script Writer V1.0
- 输出目标：Agent 5
- 是否自动接入主 Workflow Manager：否，当前只登记接口，保留人工确认步骤。

## Agent 4 负责什么？

Agent 4 只负责：

- 接收 Agent 3 已通过 QA 的短视频脚本；
- 生成 9:16 竖屏短视频镜头规划；
- 生成每个镜头的画面描述、屏幕文字和 B-roll 建议；
- 生成英文 image_prompt 和 video_prompt；
- 做 Visual QA，判断视觉方案是否可以交给 Agent 5；
- 输出机器可读 JSON 和产品经理可读 Markdown Visual Report。

## Agent 4 不负责什么？

Agent 4 不负责：

- 改写完整视频脚本；
- 健康声明合规判断；
- 实际生成图片或视频；
- 配音；
- 字幕时间轴；
- 发布内容；
- 开发 Agent 5。

## n8n 导入文件

请导入这个文件：

```text
04-Video-Director/n8n/ai-health-os-agent4-visual-director-v0.1-dev.json
```

工作流名称：

```text
AI Health OS - Agent 4 Visual Director v0.1 DEV
```

## 7 个节点

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | Agent 4 输入表单 | 粘贴 Agent 3 JSON 结果 |
| 2 | 标准化 Agent 3 JSON | 解析 JSON 字符串、对象、数组或 Markdown 代码块 |
| 3 | 筛选可进入 Agent 4 的脚本 | 只保留 ready_for_agent4 / qa_passed / approved / ready_for_next_agent 的脚本 |
| 4 | Visual Director | 生成镜头规划、画面描述、Prompt、屏幕文字和 B-roll |
| 5 | Visual QA | 检查视觉方案完整性、安全性和镜头节奏 |
| 6 | JSON Visual Plan + Markdown Visual Report | 输出 JSON 和 Markdown 视觉报告 |
| 7 | 显示 Agent 4 报告 | 在 n8n 表单结束页动态显示报告 |

## 重要说明

Agent 4 只生成视觉策划和生成式媒体 Prompt，不实际生成图片或视频，也不构成医疗、法律或平台合规意见。最终制作和发布前仍需人工审核。

当前不要开发 Agent 5。
