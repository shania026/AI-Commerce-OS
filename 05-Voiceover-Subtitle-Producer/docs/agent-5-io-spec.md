# Agent 5 输入输出规范

## 输入来源

Agent 5 接收 Agent 4 输出的 JSON。

n8n 表单字段：

```text
agent4_json
```

支持输入形式：

- JSON 字符串；
- JSON 对象；
- JSON 数组；
- 被 ```json 包裹的 JSON。

## 可识别视觉方案数组字段

Agent 5 会自动寻找以下数组：

- `visual_plans`
- `plans`
- `results`
- `records`
- `approved_visual_plans`

## 进入 Agent 5 的条件

只处理：

```text
ready_for_agent5 = true
```

最多处理前 5 条。

## 输出状态

- `success`：成功生成配音字幕包；
- `insufficient_data`：没有可处理视觉方案；
- `error`：输入 JSON 解析失败。

## 输出给 Agent 6 的条件

只有 `ready_for_agent6 = true` 的配音字幕包可以交给 Agent 6。

当前只是预留交接，不开发 Agent 6。
