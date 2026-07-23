# n8n Workflow：AI Health OS - Agent 3 Script Writer v0.1 DEV

导入文件：

```text
03-Script-Writer/n8n/ai-health-os-agent3-script-writer-v0.1-dev.json
```

导入后 workflow 名称：

```text
AI Health OS - Agent 3 Script Writer v0.1 DEV
```

这个工作流是独立工作流，不会修改 Workflow Manager、Agent 1 或 Agent 2。

它只处理 Agent 2 JSON 中 `ready_for_agent3 = true` 的选题。

如果没有符合条件的选题，会返回：

```text
status = insufficient_data
```

请不要开发 Agent 4。
