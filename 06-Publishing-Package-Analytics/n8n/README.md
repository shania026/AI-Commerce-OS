# Agent 6 n8n 工作流说明

## 导入文件

```text
06-Publishing-Package-Analytics/n8n/ai-health-os-agent6-publishing-package-analytics-v0.1-dev.json
```

导入后工作流名称是：

```text
AI Health OS - Agent 6 Publishing Package & Analytics v0.1 DEV
```

## 架构说明

这是内存传递工作流，不写入本地磁盘，不调用 Python，不连接任何发布平台，不自动上传，不买广告，不自动回复评论。

7 个节点连接：

```text
1. Agent6 输入
→ 2. 标准化 Agent5 JSON
→ 3. 筛选 ready_for_agent6
→ 4. Publishing Package Builder
→ 5. Publishing QA
→ 6. JSON + Markdown
→ 7. 显示报告
```

## 普通用户如何测试

从第 1 个节点开始，粘贴 Agent 5 输出 JSON。然后逐节点点击测试，直到第 7 个节点显示 Markdown 报告。

## 注意

Agent 6 只生成发布素材包和分析模板，不自动发布。当前不要开发 Agent 7。
