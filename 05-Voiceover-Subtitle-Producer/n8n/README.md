# Agent 5 n8n 工作流说明

## 导入文件

```text
05-Voiceover-Subtitle-Producer/n8n/ai-health-os-agent5-voiceover-subtitle-producer-v0.1-dev.json
```

导入后工作流名称是：

```text
AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV
```

## 架构说明

这是内存传递工作流，不写入本地磁盘，不调用 Python，不调用 ElevenLabs，不调用任何外部 TTS 服务。

7 个节点连接：

```text
1. Agent5 输入
→ 2. 标准化 Agent4 JSON
→ 3. 筛选 ready_for_agent5
→ 4. Voiceover Producer
→ 5. Subtitle QA
→ 6. JSON + Markdown
→ 7. 显示报告
```

## 普通用户如何测试

从第 1 个节点开始，粘贴 Agent 4 输出 JSON。然后逐节点点击测试，直到第 7 个节点显示 Markdown 报告。

## 注意

Agent 5 只生成文字层面的配音稿、字幕、SRT 和 TTS Prompt，不实际生成音频。当前不要开发 Agent 6。
