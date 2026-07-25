# Agent 5 测试说明

## 自动测试命令

在项目根目录运行：

```bash
python -m unittest 05-Voiceover-Subtitle-Producer/tests/test_agent5_n8n_workflow.py
```

## 测试覆盖

测试至少覆盖：

1. 正常 `ready_for_agent5 = true` 的视觉方案可以生成完整配音字幕包，并且 `ready_for_agent6 = true`；
2. 没有 `ready_for_agent5 = true` 的视觉方案时返回 `insufficient_data`；
3. 输入 JSON 格式错误时返回清晰 `parse_error`，工作流不崩溃；
4. 字幕或配音文本中出现高风险医疗表达时，Subtitle QA 阻止进入 Agent 6；
5. 缺少字幕、TTS Prompt 或时间不合理时，Subtitle QA 自动修复或标记问题；
6. SRT 必须包含合法时间箭头 `-->`。

## n8n 手动测试顺序

1. 先测试第 1 个节点：`Agent5 输入`；
2. 再测试第 2 个节点：`标准化 Agent4 JSON`；
3. 然后依次测试第 3 到第 7 个节点；
4. 最后看第 7 个节点是否显示 Markdown 报告。
