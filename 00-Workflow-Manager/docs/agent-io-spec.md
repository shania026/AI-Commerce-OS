# Agent 输入输出规范（MVP）

## 1. 为什么需要统一规范？

AI Health OS 以后会有多个 Agent。如果每个 Agent 的输入和输出位置都不一样，普通用户很难使用，也不方便排查问题。

所以从 Workflow Manager 开始，统一约定：

- 所有用户准备的输入文件放在 `Inputs/`；
- 所有机器可读结果放在 `Outputs/`；
- 所有产品经理可读报告放在 `Reports/`；
- 所有工作流调度代码放在 `00-Workflow-Manager/`。

## 2. 统一目录结构

```text
Inputs/
  health_topics.csv
Outputs/
  agent1_ranked_health_topics.json
Reports/
  agent1_decision_report.md
00-Workflow-Manager/
  workflow.py
  README.md
  docs/
    agent-io-spec.md
    workflow-user-manual.md
```

## 3. Agent 1 输入规范

Agent 1 输入文件：

```text
Inputs/health_topics.csv
```

必须包含字段：

| 字段 | 含义 |
| --- | --- |
| `title` | 选题标题 |
| `ingredient` | 相关草本、茶、食材或产品 |
| `angle` | 内容角度 |
| `target_audience` | 目标人群 |
| `curiosity` | 好奇心分数，1 到 5 |
| `pain` | 痛点强度，1 到 5 |
| `product_fit` | 产品匹配度，1 到 5 |
| `visual_potential` | 画面表现力，1 到 5 |
| `repeatability` | 系列化潜力，1 到 5 |
| `suggested_hook` | 建议开头钩子 |

## 4. Agent 1 输出规范

机器可读 JSON：

```text
Outputs/agent1_ranked_health_topics.json
```

产品经理可读 Markdown：

```text
Reports/agent1_decision_report.md
```

## 5. 未来 Agent 接入规范

未来每个 Agent 都应该登记到 `workflow.py` 的 `AGENT_REGISTRY`。

每个 Agent 至少需要说明：

- Agent 名称；
- 脚本路径；
- 默认输入路径；
- 默认输出路径；
- 默认报告路径；
- 它负责什么。

注意：这只是预留接口，不代表现在要开发 Agent 2。
