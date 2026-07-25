# Agent 6 测试说明

## 自动测试命令

在项目根目录运行：

```bash
python -m unittest 06-Publishing-Package-Analytics/tests/test_agent6_n8n_workflow.py
```

## 测试覆盖

测试至少覆盖：

1. 正常 `ready_for_agent6 = true` 的内容可以生成完整发布包；
2. 没有 `ready_for_agent6 = true` 的内容时返回 `insufficient_data`；
3. 输入 JSON 格式错误时返回清晰 `parse_error`，工作流不崩溃；
4. 发布文案中出现高风险健康表达时，Publishing QA 阻止进入人工发布；
5. 缺少 Hashtags、SEO、Checklist、Analytics Template 或 A/B Test Plan 时，Publishing QA 自动修复或标记问题；
6. Markdown 报告必须包含 TikTok、Instagram、YouTube Shorts、Analytics Template 和 A/B Test Plan。

## n8n 手动测试顺序

1. 先测试第 1 个节点：`Agent6 输入`；
2. 再测试第 2 个节点：`标准化 Agent5 JSON`；
3. 然后依次测试第 3 到第 7 个节点；
4. 最后看第 7 个节点是否显示 Markdown 报告。
