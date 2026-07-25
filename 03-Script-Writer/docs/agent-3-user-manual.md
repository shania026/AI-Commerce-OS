# Agent 3 Script Writer V1.0 用户使用手册

Agent 3 V1.0 已正式发布。

Release Note：

- Version：V1.0
- Status：Stable
- Testing：Passed
- Ready for Agent 4

这份手册写给普通用户和产品经理，不假设你会编程。

## 1. Agent 3 是什么？

Agent 3 是英文短视频脚本生成 Agent。

它会把 Agent 2 已经审核通过的健康选题，改写成适合 TikTok / Reels / Shorts 的英文短视频脚本。

## 2. Agent 3 负责什么？

Agent 3 只负责：

- 接收 Agent 2 已审核通过的选题；
- 生成 TikTok / Reels / Shorts 英文视频脚本；
- 输出 Hook、Body、CTA；
- 输出视频标题、视频描述、建议标签、视频目标和预计时长；
- 输出 JSON 和 Markdown Script Report；
- 将脚本交给 Agent 4。

## 3. Agent 3 不负责什么？

Agent 3 不负责：

- 图片生成；
- 视频生成；
- 配音；
- 发布；
- 开发 Agent 4。

## 4. 我每天怎么用？

### 第一步：先完成 Agent 1 和 Agent 2

你需要先用 Agent 1 选题，再用 Agent 2 做健康声明风险检查和安全改写。

### 第二步：复制 Agent 2 JSON

你只需要复制 Agent 2 输出的 JSON。

### 第三步：打开 Agent 3 n8n 工作流

工作流名称是：

```text
AI Health OS - Agent 3 Script Writer V1.0
```

### 第四步：填写表单

表单里只有一个必填字段：

```text
agent2_json
```

把 Agent 2 JSON 粘贴进去，然后提交。

### 第五步：查看报告

Agent 3 会输出 Markdown Script Report。

你重点看：

- 生成了几个脚本；
- 每个脚本的视频标题；
- Hook 是否适合前三秒；
- Body 是否自然；
- CTA 是否完整；
- Hashtags 是否可用；
- Script QA 是否通过。

## 5. 如果没有脚本生成怎么办？

如果报告显示：

```text
status = insufficient_data
```

说明 Agent 2 JSON 中没有 `ready_for_agent3 = true` 的选题。

这时不要让 Agent 3 编造内容。请回到 Agent 2，确认至少一个选题已经通过并可进入 Agent 3。

## 6. 导入哪个文件？

请导入：

```text
03-Script-Writer/n8n/ai-health-os-agent3-script-writer-v1.0.json
```

## 7. 重要说明

Agent 3 只负责脚本写作，不负责健康声明审核、医疗合规判断、图片、视频、配音或发布。

请不要开发 Agent 4。
