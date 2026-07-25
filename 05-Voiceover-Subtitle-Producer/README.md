# AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV

Agent 5 是独立的配音与字幕生产工作流。

它接收 Agent 4 输出中 `ready_for_agent5 = true` 的视觉方案，为每条视频生成英文配音稿、分句配音、字幕、SRT、配音节奏和 TTS Prompt。

## 当前状态

- Version：v0.1 DEV
- Status：Development
- 输入来源：Agent 4 Visual Director V1.0 / v0.1 DEV 输出中 `ready_for_agent5 = true` 的视觉方案
- 输出目标：Agent 6
- 是否自动接入主 Workflow Manager：否，当前只登记接口，保留人工确认步骤。

## Agent 5 负责什么？

Agent 5 只负责：

- 接收 Agent 4 可进入下一步的视觉方案；
- 生成英文完整配音稿；
- 生成分句配音；
- 生成字幕文本；
- 生成 SRT 字幕；
- 生成配音节奏和 delivery notes；
- 生成 TTS Prompt；
- 输出 JSON 和 Markdown 报告；
- 将合格结果交给 Agent 6。

## Agent 5 不负责什么？

Agent 5 不负责：

- 实际生成音频；
- 调用 ElevenLabs；
- 发布视频；
- 修改 Agent 4；
- 开发 Agent 6。

## n8n 导入文件

```text
05-Voiceover-Subtitle-Producer/n8n/ai-health-os-agent5-voiceover-subtitle-producer-v0.1-dev.json
```

工作流名称：

```text
AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV
```

## 7 个节点

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | Agent5 输入 | 粘贴 Agent 4 JSON |
| 2 | 标准化 Agent4 JSON | 解析 JSON 字符串、数组、对象或 Markdown 代码块 |
| 3 | 筛选 ready_for_agent5 | 只保留 `ready_for_agent5 = true` 的视觉方案 |
| 4 | Voiceover Producer | 生成英文配音稿、分句配音、字幕、SRT 和 TTS Prompt |
| 5 | Subtitle QA | 检查字幕、SRT、时间、风险词和完整性 |
| 6 | JSON + Markdown | 输出机器可读 JSON 和产品经理可读 Markdown 报告 |
| 7 | 显示报告 | 在 n8n 表单结束页动态显示报告 |

## 重要说明

Agent 5 只生成文字层面的配音稿、字幕和 TTS Prompt，不实际生成音频，不调用 ElevenLabs 或任何外部 TTS 服务。当前不要开发 Agent 6。
