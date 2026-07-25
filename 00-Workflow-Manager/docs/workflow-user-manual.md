# Workflow 使用手册（普通用户版）

## 1. Workflow Manager 是什么？

Workflow Manager 是 AI Health OS 的总调度器。

你可以把它理解成“项目经理”：

- 它不亲自写内容；
- 它不生成视频；
- 它不发布 TikTok；
- 它只负责按顺序调用已经完成的 Agent。

当前 MVP 只调用 Agent 1。

## 2. 你需要准备什么？

你只需要准备一个健康选题 CSV 文件：

```text
Inputs/health_topics.csv
```

如果你不知道怎么写，可以先参考这个文件：

```text
01-Viral-Finder/examples/health_topics.csv
```

## 3. 如何运行整个流程？

在项目根目录运行：

```bash
python 00-Workflow-Manager/workflow.py --limit 5
```

这条命令的意思是：

- 调用 Workflow Manager；
- 让它运行 Agent 1；
- 最多输出 5 个推荐选题。

## 4. 运行后看哪里？

运行完成后，你会得到两个核心文件。

机器可读结果：

```text
Outputs/agent1_ranked_health_topics.json
```

产品经理决策报告：

```text
Reports/agent1_decision_report.md
```

如果你不是程序员，请优先打开 Markdown 报告。

## 5. 如何判断是否成功？

成功时，终端会显示类似：

```text
Workflow Manager 执行完成。
- 已完成：agent1｜健康选题发现 Agent：读取候选选题 CSV，输出 JSON 排序和 Markdown 决策报告。
```

并且你能在 `Reports/` 里看到决策报告。

## 6. 常见错误

### 错误 1：找不到 Inputs/health_topics.csv

说明你还没有准备输入文件。

解决方法：

1. 打开 `Inputs/` 文件夹；
2. 新建或复制一个 `health_topics.csv`；
3. 再运行 Workflow Manager。

### 错误 2：CSV 字段不对

说明你的 CSV 表头缺字段或字段名写错。

解决方法：复制 `01-Viral-Finder/examples/health_topics.csv` 的第一行表头。

### 错误 3：我看到 JSON，但看不懂

这是正常的。JSON 是给系统和后续 Agent 用的。

你应该优先看：

```text
Reports/agent1_decision_report.md
```

## 7. 下一步如何使用 Agent 2？

Agent 2 V1.0 已正式发布。

但请注意：Workflow Manager 当前主流程仍然只自动运行 Agent 1。Agent 2 是独立 n8n 工作流，必须在你人工确认选题后单独运行。

Agent 2 V1.0 负责：

- 接收 Agent 1 人工确认后的选题；
- 完成健康声明风险检查；
- 完成安全改写；
- 输出 JSON 和 Markdown 报告；
- 将可用选题交给 Agent 3。

Agent 2 V1.0 不负责：

- 写完整脚本；
- 生成视频；
- 发布内容；
- 开发 Agent 3。

导入文件：

```text
00-Workflow-Manager/n8n/ai-health-os-agent2-compliance-rewriter-v1.0.json
```

普通用户操作顺序：

1. 先运行 Agent 1；
2. 打开 Agent 1 的 Markdown 决策报告；
3. 人工确认 2–5 个选题；
4. 打开 Agent 2 V1.0 n8n 表单；
5. 粘贴 Agent 1 JSON；
6. 填写人工确认的选题名称或编号；
7. 查看 Agent 2 输出的中文合规改写报告。

当前阶段请不要开发 Agent 5。

## 8. 下一步如何使用 Agent 4？

Agent 4 Visual Director v0.1 DEV 已创建为独立 n8n 工作流。

但请注意：Workflow Manager 当前主流程仍然只自动运行 Agent 1。Agent 4 只是登记了接口，不会自动接在 Agent 3 后面运行。

Agent 4 负责：

- 接收 Agent 3 已通过 QA 的短视频脚本；
- 生成 TikTok / Reels / Shorts 竖屏镜头规划；
- 生成 AI 图片 Prompt 和 AI 视频 Prompt；
- 输出 JSON Visual Plan 和 Markdown Visual Report；
- 将可用视觉方案交给未来 Agent 5。

Agent 4 不负责：

- 实际生成图片或视频；
- 配音；
- 发布内容；
- 开发 Agent 5。

导入文件：

```text
04-Video-Director/n8n/ai-health-os-agent4-visual-director-v0.1-dev.json
```

普通用户操作顺序：

1. 先运行 Agent 3；
2. 人工确认 Agent 3 生成的脚本；
3. 打开 Agent 4 n8n 表单；
4. 粘贴 Agent 3 JSON；
5. 查看 Agent 4 输出的 Markdown Visual Report；
6. 只把 `ready_for_agent5 = true` 的视觉方案交给未来 Agent 5。

当前阶段请不要开发 Agent 5。

## 9. 下一步如何使用 Agent 5？

Agent 5 Voiceover & Subtitle Producer v0.1 DEV 已创建为独立 n8n 工作流。

但请注意：Workflow Manager 当前主流程仍然只自动运行 Agent 1。Agent 5 只是登记了接口，不会自动接在 Agent 4 后面运行。

Agent 5 负责：

- 接收 Agent 4 中 `ready_for_agent5 = true` 的视觉方案；
- 生成英文配音稿；
- 生成分句配音；
- 生成字幕和 SRT；
- 生成配音节奏和 TTS Prompt；
- 输出 JSON 和 Markdown 报告；
- 将合格配音字幕包交给未来 Agent 6。

Agent 5 不负责：

- 实际生成音频；
- 调用 ElevenLabs；
- 发布视频；
- 修改 Agent 4；
- 开发 Agent 6。

导入文件：

```text
05-Voiceover-Subtitle-Producer/n8n/ai-health-os-agent5-voiceover-subtitle-producer-v0.1-dev.json
```

普通用户操作顺序：

1. 先运行 Agent 4；
2. 人工确认 Agent 4 生成的视觉方案；
3. 打开 Agent 5 n8n 表单；
4. 粘贴 Agent 4 JSON；
5. 查看 Agent 5 输出的 Markdown 报告；
6. 只把 `ready_for_agent6 = true` 的配音字幕包交给未来 Agent 6。

当前阶段请不要开发 Agent 6。

## 10. 下一步如何使用 Agent 6？

Agent 6 Publishing Package & Analytics v0.1 DEV 已创建为独立 n8n 工作流。

但请注意：Workflow Manager 当前主流程仍然只自动运行 Agent 1。Agent 6 只是登记了接口，不会自动接在 Agent 5 后面运行。

Agent 6 负责：

- 接收 Agent 5 中 `ready_for_agent6 = true` 的内容；
- 生成 TikTok / Instagram / YouTube Shorts Caption；
- 生成 Video Title、Cover Text、CTA、Hashtags 和 SEO Keywords；
- 生成 Suggested Posting Time、Publishing Checklist、Analytics Template 和 A/B Test Plan；
- 输出 JSON 和 Markdown 报告。

Agent 6 不负责：

- 自动发布；
- 自动上传；
- 自动购买广告；
- 自动回复评论；
- 开发 Agent 7。

导入文件：

```text
06-Publishing-Package-Analytics/n8n/ai-health-os-agent6-publishing-package-analytics-v0.1-dev.json
```

普通用户操作顺序：

1. 先运行 Agent 5；
2. 人工确认 Agent 5 生成的配音字幕包；
3. 打开 Agent 6 n8n 表单；
4. 粘贴 Agent 5 JSON；
5. 查看 Agent 6 输出的 Markdown 报告；
6. 人工确认后再决定是否手动发布。

当前阶段请不要开发 Agent 7。
