# Agent 4 n8n 工作流说明

## 导入文件

```text
04-Video-Director/n8n/ai-health-os-agent4-visual-director-v0.1-dev.json
```

导入后工作流名称是：

```text
AI Health OS - Agent 4 Visual Director v0.1 DEV
```

## 架构说明

这是内存传递工作流，不写入本地磁盘，不调用 Python，不调用外部图片或视频 API。

7 个节点连接：

```text
1. Agent 4 输入表单
→ 2. 标准化 Agent 3 JSON
→ 3. 筛选可进入 Agent 4 的脚本
→ 4. Visual Director
→ 5. Visual QA
→ 6. JSON Visual Plan + Markdown Visual Report
→ 7. 显示 Agent 4 报告
```

## 普通用户如何测试

从第 1 个节点开始，粘贴 Agent 3 输出 JSON。然后逐节点点击测试，直到第 7 个节点显示 Markdown 报告。

## 注意

Agent 4 只生成视觉策划和 Prompt，不实际生成图片或视频。当前不要开发 Agent 5。

## Agent 4 V1.1（Agent 3 V1.1 兼容复制版）

原始 Agent 4 v0.1 DEV 工作流保留不变。为兼容上游 `AI Health OS - Agent 3 Script Writer V1.1` 的真实输出，新增复制版：

```text
04-Video-Director/n8n/ai-health-os-agent4-visual-director-v1.1.json
```

V1.1 只增强前端输入解析与筛选兼容：能够从外层数组、对象、JSON 字符串或 Markdown fenced JSON 中读取 `scripts[]`，并在 Agent 3 顶层 `handoff.next_agent = agent_4` 且 `ready_count > 0` 时处理脚本。视觉设计、Visual QA、Markdown Visual Report 和 `handoff.next_agent = agent_5` 结构保持不变，同时新增 `visual_projects` 作为 `visual_plans` 的兼容别名。
