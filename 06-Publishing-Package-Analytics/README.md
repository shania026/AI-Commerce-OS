# AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV

Agent 6 是独立的发布素材包与数据分析模板工作流。

它接收 Agent 5 输出中 `ready_for_agent6 = true` 的内容，为每条视频生成 TikTok / Instagram / YouTube Shorts 发布文案、标题、封面文字、CTA、Hashtags、SEO Keywords、建议发布时间、发布检查清单、Analytics Template 和 A/B Test Plan。

## 当前状态

- Version：v0.1 DEV
- Status：Development
- 输入来源：Agent 5 Voiceover & Subtitle Producer v0.1 DEV 中 `ready_for_agent6 = true` 的内容
- 输出目标：人工发布或未来 Agent 7
- 是否自动接入主 Workflow Manager：否，当前只登记接口，保留人工确认步骤。

## Agent 6 负责什么？

Agent 6 只负责生成：

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
- JSON 和 Markdown 报告。

## Agent 6 不负责什么？

Agent 6 不负责：

- 自动发布；
- 自动上传；
- 自动购买广告；
- 自动回复评论；
- 开发 Agent 7。

## n8n 导入文件

```text
06-Publishing-Package-Analytics/n8n/ai-health-os-agent6-publishing-package-analytics-v0.1-dev.json
```

工作流名称：

```text
AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV
```

## 7 个节点

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | Agent6 输入 | 粘贴 Agent 5 JSON |
| 2 | 标准化 Agent5 JSON | 解析 JSON 字符串、数组、对象或 Markdown 代码块 |
| 3 | 筛选 ready_for_agent6 | 只保留 `ready_for_agent6 = true` 的内容 |
| 4 | Publishing Package Builder | 生成多平台 Caption、标题、CTA、Hashtags、SEO 和分析模板 |
| 5 | Publishing QA | 检查文案完整性、长度、风险词和发布包字段 |
| 6 | JSON + Markdown | 输出机器可读 JSON 和产品经理可读 Markdown 报告 |
| 7 | 显示报告 | 在 n8n 表单结束页动态显示报告 |

## 重要说明

Agent 6 只生成发布素材包和分析模板，不自动发布、不自动上传、不买广告、不自动回复评论。当前不要开发 Agent 7。
