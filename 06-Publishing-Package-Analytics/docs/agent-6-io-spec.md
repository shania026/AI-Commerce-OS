# Agent 6 输入输出规范

## 输入来源

Agent 6 接收 Agent 5 输出的 JSON。

n8n 表单字段：

```text
agent5_json
```

支持输入形式：

- JSON 字符串；
- JSON 对象；
- JSON 数组；
- 被 ```json 包裹的 JSON。

## 可识别内容数组字段

Agent 6 会自动寻找以下数组：

- `voiceover_packages`
- `publishing_inputs`
- `packages`
- `results`
- `records`

## 进入 Agent 6 的条件

只处理：

```text
ready_for_agent6 = true
```

最多处理前 5 条。

## 输出状态

- `success`：成功生成发布素材包；
- `insufficient_data`：没有可处理内容；
- `error`：输入 JSON 解析失败。

## 输出用途

Agent 6 输出只用于人工发布前准备，不会自动发布、上传、买广告或回复评论。

当前不开发 Agent 7。
