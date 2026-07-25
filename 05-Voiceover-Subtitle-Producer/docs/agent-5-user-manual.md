# Agent 5 中文用户使用手册

## 1. Agent 5 是什么？

Agent 5 的名字是：

```text
AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV
```

它是 AI Health OS 的第五个独立工作流，作用是把 Agent 4 已经通过 Visual QA 的视觉方案，变成可以交给配音工具和字幕工具使用的文本素材。

你可以把它理解成“配音字幕助理”：它不会真的生成音频，也不会调用 ElevenLabs，但会准备好英文配音稿、分句、字幕、SRT 文件内容和 TTS Prompt。

## 2. 你每天要准备什么？

你只需要准备 Agent 4 输出的完整 JSON。

Agent 5 默认只处理：

```text
ready_for_agent5 = true
```

如果没有符合条件的视觉方案，Agent 5 会返回 `insufficient_data`，不会编造配音或字幕。

## 3. 怎么在 n8n 里运行？

1. 打开 n8n。
2. 打开工作流：`AI Health OS - Agent 5 Voiceover & Subtitle Producer v0.1 DEV`。
3. 从第 1 个节点 `Agent5 输入` 开始测试。
4. 在表单字段 `agent4_json` 中粘贴 Agent 4 的完整 JSON。
5. 点击提交。
6. 依次测试第 2 到第 7 个节点。
7. 最后在第 7 个节点查看 Markdown 报告。

## 4. 输出里应该看什么？

你主要看 Markdown 报告：

```text
# AI Health OS — Agent 5 Voiceover & Subtitle Report
```

重点看：

- 哪些配音字幕包 `ready_for_agent6 = true`；
- 哪些字幕或配音文本需要人工复核；
- 每个视频的完整英文配音稿；
- 每个分句的开始时间、结束时间、配音文本、字幕文本和节奏；
- SRT 字幕内容；
- TTS Prompt。

## 5. Agent 5 输出 JSON 包含什么？

顶层字段包括：

- `workflow`
- `source_agent`
- `agent`
- `version`
- `status`
- `generated_at`
- `total_visual_plans`
- `voiceover_packages`
- `handoff`
- `disclaimer`
- `report_markdown`

每个 `voiceover_packages` 元素至少包含：

- `package_id`
- `source_script_id`
- `video_title`
- `language`
- `voice_style`
- `full_voiceover_script`
- `voiceover_segments`
- `subtitles`
- `srt`
- `voiceover_pacing`
- `tts_prompt`
- `qa_passed`
- `qa_score`
- `qa_issues`
- `ready_for_agent6`

## 6. 常见错误

### 错误：JSON 解析失败

说明你粘贴的 Agent 4 JSON 不完整，或者复制时多复制了其他文字。

处理方式：回到 Agent 4，把完整 JSON 重新复制到 Agent 5 表单里。

### 错误：insufficient_data

说明 Agent 4 JSON 里没有 `ready_for_agent5 = true` 的视觉方案。

你需要回到 Agent 4 报告，确认哪些视觉方案通过 Visual QA。

### 错误：Subtitle QA 未通过

说明配音稿或字幕中可能缺少必要内容、时间不合理、字幕太长，或重新出现了不适合健康短视频的高风险表达。

这种结果不能交给 Agent 6，需要人工检查。

## 7. 下一步如何接入 Agent 6？

当前不要开发 Agent 6。

未来 Agent 6 只应该接收：

```text
ready_for_agent6 = true
```

的配音字幕包，并继续由人工确认后再进入下一步。
