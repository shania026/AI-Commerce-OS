# Agent 6 中文用户使用手册

## 1. Agent 6 是什么？

Agent 6 的名字是：

```text
AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV
```

它是 AI Health OS 的第六个独立工作流，作用是把 Agent 5 已经通过 QA 的配音字幕包，变成可以人工发布前使用的多平台发布素材包。

你可以把它理解成“发布助理”：它不会替你发布视频，也不会上传文件，但会准备好 TikTok、Instagram Reels 和 YouTube Shorts 可以参考的 Caption、标题、封面文字、CTA、Hashtags、SEO Keywords、发布时间建议、发布检查清单、数据分析模板和 A/B 测试计划。

## 2. 你每天要准备什么？

你只需要准备 Agent 5 输出的完整 JSON。

Agent 6 默认只处理：

```text
ready_for_agent6 = true
```

如果没有符合条件的内容，Agent 6 会返回 `insufficient_data`，不会编造发布包。

## 3. 怎么在 n8n 里运行？

1. 打开 n8n。
2. 打开工作流：`AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV`。
3. 从第 1 个节点 `Agent6 输入` 开始测试。
4. 在表单字段 `agent5_json` 中粘贴 Agent 5 的完整 JSON。
5. 点击提交。
6. 依次测试第 2 到第 7 个节点。
7. 最后在第 7 个节点查看 Markdown 报告。

## 4. 输出里应该看什么？

你主要看 Markdown 报告：

```text
# AI Health OS — Agent 6 Publishing Package & Analytics Report
```

重点看：

- TikTok Caption；
- Instagram Caption；
- YouTube Shorts Caption；
- Video Title；
- Cover Text；
- CTA；
- Hashtags；
- SEO Keywords；
- Suggested Posting Time；
- Publishing Checklist；
- Analytics Template；
- A/B Test Plan；
- 哪些发布包 `ready_for_manual_publish = true`。

## 5. Agent 6 输出 JSON 包含什么？

顶层字段包括：

- `workflow`
- `source_agent`
- `agent`
- `version`
- `status`
- `generated_at`
- `total_voiceover_packages`
- `publishing_packages`
- `handoff`
- `disclaimer`
- `report_markdown`

每个 `publishing_packages` 元素至少包含：

- `publishing_id`
- `source_package_id`
- `video_title`
- `cover_text`
- `tiktok_caption`
- `instagram_caption`
- `youtube_shorts_caption`
- `cta`
- `hashtags`
- `seo_keywords`
- `suggested_posting_time`
- `publishing_checklist`
- `analytics_template`
- `ab_test_plan`
- `qa_passed`
- `qa_score`
- `qa_issues`
- `ready_for_manual_publish`

## 6. 常见错误

### 错误：JSON 解析失败

说明你粘贴的 Agent 5 JSON 不完整，或者复制时多复制了其他文字。

处理方式：回到 Agent 5，把完整 JSON 重新复制到 Agent 6 表单里。

### 错误：insufficient_data

说明 Agent 5 JSON 里没有 `ready_for_agent6 = true` 的内容。

你需要回到 Agent 5 报告，确认哪些配音字幕包通过 QA。

### 错误：Publishing QA 未通过

说明发布包可能缺少 Caption、Hashtags、SEO、CTA、分析模板，或者重新出现高风险健康表达。

这种结果不能直接用于发布，需要人工检查。

## 7. 下一步

当前不要开发 Agent 7。

Agent 6 的输出只用于人工发布前准备。最终是否发布、什么时候发布、发布到哪个平台，都需要人工确认。
