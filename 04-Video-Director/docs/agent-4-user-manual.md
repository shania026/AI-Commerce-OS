# Agent 4 中文用户使用手册

## 1. Agent 4 是什么？

Agent 4 的名字是：

```text
AI Health OS - Agent 4 Visual Director v0.1 DEV
```

它是 AI Health OS 的第四个独立工作流，作用是把 Agent 3 已经生成好的英文短视频脚本，变成可以交给图片/视频制作工具使用的视觉执行方案。

你可以把它理解成“视频导演助理”：它不会拍视频，也不会生成图片，但会告诉你每个镜头应该拍什么、画面怎么设计、屏幕文字写什么、AI 图片/视频 Prompt 怎么写。

## 2. 你每天要准备什么？

你只需要准备 Agent 3 输出的完整 JSON。

Agent 4 默认只处理以下脚本：

- `ready_for_agent4 = true`
- 或 `qa_passed = true`
- 或 `status = approved`
- 或 `ready_for_next_agent = true`

如果没有符合条件的脚本，Agent 4 会返回 `insufficient_data`，不会编造视觉方案。

## 3. 怎么在 n8n 里运行？

1. 打开 n8n。
2. 打开工作流：`AI Health OS - Agent 4 Visual Director v0.1 DEV`。
3. 从第 1 个节点 `Agent 4 输入表单` 开始测试。
4. 在表单字段 `agent3_json` 中粘贴 Agent 3 的完整 JSON。
5. 点击提交。
6. 依次测试第 2 到第 7 个节点。
7. 最后在第 7 个节点查看 Markdown Visual Report。

## 4. 输出里应该看什么？

你主要看 Markdown 报告：

```text
# AI Health OS — Agent 4 Visual Director Report
```

重点看：

- 哪些视觉方案 `ready_for_agent5 = true`；
- 哪些方案需要人工复核；
- 哪些方案没有通过 Visual QA；
- 每个镜头的时间、旁白、画面、屏幕文字、Image Prompt、Video Prompt 和注意事项。

## 5. Agent 4 输出 JSON 包含什么？

顶层字段包括：

- `workflow`
- `source_agent`
- `agent`
- `version`
- `status`
- `generated_at`
- `total_scripts`
- `visual_plans`
- `handoff`
- `disclaimer`
- `report_markdown`

每个 `visual_plans` 元素至少包含：

- `script_id`
- `video_title`
- `visual_style`
- `aspect_ratio`
- `estimated_duration_seconds`
- `scenes`
- `qa_passed`
- `qa_score`
- `qa_issues`
- `ready_for_agent5`

## 6. 常见错误

### 错误：JSON 解析失败

说明你粘贴的 Agent 3 JSON 不完整，或者复制时多复制了其他文字。

处理方式：回到 Agent 3，把完整 JSON 重新复制到 Agent 4 表单里。

### 错误：insufficient_data

说明 Agent 3 JSON 里没有可进入 Agent 4 的脚本。

你需要确认脚本是否有：

- `ready_for_agent4 = true`
- 或 `qa_passed = true`
- 或 `status = approved`
- 或 `ready_for_next_agent = true`

### 错误：Visual QA 未通过

说明视觉方案可能缺少关键字段，或者出现了不安全医疗画面表达，例如“治愈疾病”“替代药物”“保证结果”。

这种方案不能交给 Agent 5，需要人工检查。

## 7. 下一步如何接入 Agent 5？

当前不要开发 Agent 5。

未来 Agent 5 只应该接收：

```text
ready_for_agent5 = true
```

的视觉方案，并继续由人工确认后再进入下一步。

## 重要说明

本工具仅生成视觉策划、镜头设计和生成式媒体 Prompt，不实际生成图片或视频，也不构成医疗、法律或平台合规意见。最终制作和发布前仍需人工审核。
