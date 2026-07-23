# Agent 4 测试说明

## 自动测试命令

在项目根目录运行：

```bash
python -m unittest 04-Video-Director/tests/test_agent4_n8n_workflow.py
```

## 测试覆盖

测试至少覆盖：

1. 正常脚本可以生成完整镜头方案，并且 `ready_for_agent5 = true`；
2. 没有可进入 Agent 4 的脚本时返回 `insufficient_data`；
3. 脚本或视觉方案中出现高风险医疗表达时，Visual QA 阻止进入 Agent 5；
4. 缺少 Hook 或 CTA 时，Visual QA 给出问题并自动补充安全占位；
5. 镜头时间总和异常时，Visual QA 自动调整预计时长；
6. 输入 JSON 格式错误时返回清晰 `parse_error`，工作流不崩溃。

## n8n 手动测试顺序

1. 先测试第 1 个节点：`Agent 4 输入表单`；
2. 再测试第 2 个节点：`标准化 Agent 3 JSON`；
3. 然后依次测试第 3 到第 7 个节点；
4. 最后看第 7 个节点是否显示 Markdown Visual Report。
