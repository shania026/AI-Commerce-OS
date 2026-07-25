# Agent 4 输入输出规范

## 输入来源

Agent 4 接收 Agent 3 输出的 JSON。

n8n 表单字段：

```text
agent3_json
```

支持输入形式：

- JSON 字符串；
- JSON 对象；
- JSON 数组；
- 被 ```json 包裹的 JSON。

## 可识别脚本数组字段

Agent 4 会自动寻找以下数组：

- `scripts`
- `script_results`
- `approved_scripts`
- `results`
- `records`

## 进入 Agent 4 的条件

脚本满足以下任一条件即可：

- `ready_for_agent4 = true`
- `qa_passed = true`
- `status = approved`
- `ready_for_next_agent = true`

最多处理前 5 条。

## 输出状态

- `success`：成功生成视觉方案；
- `insufficient_data`：没有可处理脚本；
- `error`：输入 JSON 解析失败。

## 输出给 Agent 5 的条件

只有 `ready_for_agent5 = true` 的视觉方案可以交给 Agent 5。

当前只是预留交接，不开发 Agent 5。
