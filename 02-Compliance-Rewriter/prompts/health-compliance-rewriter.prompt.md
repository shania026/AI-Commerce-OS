# Prompt：Agent 2 Health Compliance Rewriter V1.0

Agent 2 V1.0 已正式发布。

请维护或生成独立的 n8n 工作流：

```text
AI Health OS - Agent 2 Health Compliance Rewriter V1.0
```

## 边界

不要修改 Agent 1。不要开发 Agent 3。

## Agent 2 V1.0 职责

Agent 2 V1.0 负责：

- 接收 Agent 1 人工确认后的选题；
- 完成健康声明风险检查；
- 完成安全改写；
- 输出 JSON 和 Markdown 报告；
- 将可用选题交给未来 Agent 3。

## Agent 2 V1.0 不负责

Agent 2 V1.0 不负责：

- 写完整脚本；
- 生成视频；
- 发布内容；
- 提供医疗或法律意见；
- 保证内容一定符合所有法规或平台规则；
- 开发 Agent 3。

## 工作流要求

必须保留 7 个节点：

1. Agent 2 输入表单
2. 标准化 Agent 1 结果
3. 筛选人工确认选题
4. 健康声明风险检查
5. 合规安全改写
6. JSON 合规结果与 Markdown 报告
7. 显示 Agent 2 报告

连接方式必须保持：

```text
1 → 2 → 3 → 4 → 5 → 6 → 7
```

不要改变输入输出格式，不要删除人工确认步骤，不要自动触发 Agent 3。
