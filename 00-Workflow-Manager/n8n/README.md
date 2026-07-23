# n8n 可导入工作流：AI Health OS Daily Topic Finder Docker /files 版

这份文件是给 Docker 版 n8n 用户直接导入用的。

当前工作流不会开发 Agent 2，也不会调用 Agent 2。

## 1. 你要导入哪个文件？

请导入：

```text
00-Workflow-Manager/n8n/ai-health-os-daily-topic-workflow.json
```

导入后，n8n 里会出现一个工作流：

```text
AI Health OS - Daily Topic Finder Docker Files
```

## 2. 这次修复了什么？

你之前第 3 个节点报错：

```text
The file "/home/node/health_topics.csv" is not writable.
```

原因是 n8n Docker 容器里的 `/home/node` 不一定允许 Read/Write Files from Disk 节点直接写入。

新版 workflow 统一改成 Docker 中更适合挂载和写入的目录：

```text
/files
```

第 3、6、7 个文件节点统一使用：

```text
/files/health_topics.csv
/files/agent1_ranked_health_topics.json
/files/agent1_decision_report.md
```

## 3. Windows Docker Desktop 需要挂载哪个目录？

请在 Windows 上准备一个文件夹，例如：

```text
C:\AI-Health-OS-Files
```

然后把它挂载到 n8n 容器里的：

```text
/files
```

## 4. Docker Compose 示例

如果你用 `docker-compose.yml`，可以参考：

```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - C:/AI-Health-OS-Files:/files
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http

volumes:
  n8n_data:
```

Windows 路径建议用这种写法：

```text
C:/AI-Health-OS-Files:/files
```

不要写成：

```text
C:\AI-Health-OS-Files:/files
```

## 5. Docker Run 示例

如果你用 `docker run`，可以参考：

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -v C:/AI-Health-OS-Files:/files \
  n8nio/n8n:latest
```

## 6. 这个 workflow 包含哪些节点？

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | 上传健康选题 CSV | 表单上传 CSV |
| 2 | 标准化上传文件 | 只整理 n8n 数据字段，不操作文件系统 |
| 3 | 保存上传 CSV 文件 | 用官方节点保存到 `/files/health_topics.csv` |
| 4 | 提取 CSV 文本 | 用官方节点把 CSV 文件转成文本/JSON |
| 5 | 评分并生成报告数据 | Code 节点只做数据处理，不使用 `fs` |
| 6 | 保存 JSON 排序结果 | 用官方节点保存到 `/files/agent1_ranked_health_topics.json` |
| 7 | 保存 Markdown 决策报告 | 用官方节点保存到 `/files/agent1_decision_report.md` |

## 7. 为什么不再使用 Code 节点操作文件？

经过测试，n8n Code 节点不允许使用：

```text
require('node:fs')
require('fs')
import fs
```

所以新版 workflow 严格遵守：

1. Code 节点不操作文件系统。
2. Code 节点不创建目录。
3. Code 节点不读取或写入本地文件。
4. 文件保存全部交给 n8n 官方 `Read/Write Files from Disk` 节点。
5. CSV 文本提取交给 n8n 官方 `Extract From File` 节点。
6. Code 节点只负责 CSV 数据评分、生成 JSON 内容和 Markdown 内容。

## 8. 导入后每天怎么用？

1. 确认 Windows 文件夹 `C:\AI-Health-OS-Files` 已经挂载到 Docker 容器的 `/files`。
2. 打开 n8n。
3. 导入 `ai-health-os-daily-topic-workflow.json`。
4. 打开工作流 `AI Health OS - Daily Topic Finder Docker Files`。
5. 打开第 1 个表单节点生成的表单地址。
6. 上传当天的 `health_topics.csv`。
7. `today_limit` 填 `5`，或者留空使用默认值。
8. 点击提交。
9. 看第 5 个节点的 `decision_report_markdown` 字段，或者到 Windows 文件夹 `C:\AI-Health-OS-Files` 里查看 Markdown 文件。

## 9. CSV 表头必须是什么？

第一行必须是：

```csv
title,ingredient,angle,target_audience,curiosity,pain,product_fit,visual_potential,repeatability,suggested_hook
```

如果字段名写错，workflow 会提示缺少哪个字段。

---

# 备用新版：Agent 1 Memory MVP（不使用任何磁盘写入）

如果 Docker 的 `/files` 挂载已经确认可写，但 n8n 的文件节点仍然报写入权限错误，请改用内存传递版 workflow。

导入文件：

```text
00-Workflow-Manager/n8n/ai-health-os-agent1-memory-mvp.json
```

导入后 workflow 名称：

```text
AI Health OS - Agent 1 Memory MVP
```

这个版本的特点：

1. 不使用 `Read/Write Files from Disk` 节点。
2. 不写入 `/files`。
3. 不写入 `/home/node`。
4. 不写入 Windows 本地路径。
5. 不使用 `node:fs`、`fs`、`require()` 或任何文件系统模块。
6. CSV 在 n8n 节点之间以内存方式传递。
7. 使用官方 `Extract From File` 节点把 CSV 转成 JSON。
8. 最后用官方 `Form Ending` 节点把 Markdown 报告和 JSON 排名结果直接显示给用户。

节点顺序：

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | 上传 CSV 表单 | 上传 `health_topics_csv`，填写 `today_limit` 和 `today_focus` |
| 2 | 标准化上传文件 | 把上传的二进制字段统一命名为 `data` |
| 3 | CSV 转 JSON | 官方节点把 CSV 转成 JSON 行数据 |
| 4 | Agent 1 内存分析 | 只做数据评分和风险判断，不操作文件系统 |
| 5 | JSON 排名结果 | 最终 JSON 输出分支 |
| 6 | Markdown 决策报告 | 最终 Markdown 输出分支 |
| 7 | 显示结果给用户 | 在表单结束页直接显示报告和 JSON |

建议从第 1 个节点重新测试。

---

# 最新新版：Agent 1 Memory MVP v2（只要求 title）

如果你的 CSV 只有 `title` 一列，请导入 v2 版本。

导入文件：

```text
00-Workflow-Manager/n8n/ai-health-os-agent1-memory-mvp-v2.json
```

导入后 workflow 名称：

```text
AI Health OS - Agent 1 Memory MVP v2
```

v2 的变化：

1. 只要求 `title` 是必填字段。
2. `ingredient`、`angle`、`target_audience`、`curiosity`、`pain`、`product_fit`、`visual_potential`、`repeatability`、`suggested_hook` 全部变成可选。
3. 如果可选字段缺失，系统会根据 `title` 自动补默认值。
4. 不会因为缺少可选字段而停止工作流。
5. 继续使用内存传递架构，不写入本地文件。
6. 继续不使用 `node:fs`、`fs`、`require()` 或任何文件系统模块。

最简 CSV 示例：

```csv
title
Why your evening tea choice matters
The red tea South Africans drink without caffeine
Screen fatigue and your tea routine
```

建议仍然从第 1 个节点重新测试：

```text
1. 上传 CSV 表单
```

---

# Agent 2：Health Compliance Rewriter V1.0

Agent 2 V1.0 已正式发布。

这是独立的 Agent 2 n8n 工作流，不会修改 Agent 1，也不会自动触发或开发 Agent 3。

导入文件：

```text
00-Workflow-Manager/n8n/ai-health-os-agent2-compliance-rewriter-v1.0.json
```

导入后 workflow 名称：

```text
AI Health OS - Agent 2 Health Compliance Rewriter V1.0
```

## Agent 2 V1.0 职责

Agent 2 V1.0 负责：

1. 接收 Agent 1 人工确认后的选题；
2. 完成健康声明风险检查；
3. 完成安全改写；
4. 输出 JSON 和 Markdown 报告；
5. 将可用选题交给未来 Agent 3。

Agent 2 V1.0 不负责：

- 不写完整脚本；
- 不生成视频；
- 不发布内容；
- 不提供医疗或法律意见；
- 不保证内容一定符合所有法规或平台规则；
- 不开发 Agent 3。

## Agent 2 V1.0 的 7 个节点

| 节点 | 名称 | 作用 |
| --- | --- | --- |
| 1 | Agent 2 输入表单 | 粘贴 Agent 1 JSON，填写人工确认选题 |
| 2 | 标准化 Agent 1 结果 | 安全解析 JSON 字符串、对象、数组或代码块 |
| 3 | 筛选人工确认选题 | 只保留人工确认或默认 A/B 且 Yes 的前 5 个选题 |
| 4 | 健康声明风险检查 | 识别医疗声明、风险词和绝对化表达 |
| 5 | 合规安全改写 | 把高风险表达改成更谨慎的健康教育表达 |
| 6 | JSON 合规结果与 Markdown 报告 | 同时生成机器可读 JSON 和中文报告 |
| 7 | 显示 Agent 2 报告 | 用 Form Ending 动态显示报告 |

## 使用方式

1. 先运行 Agent 1，得到 JSON 排名结果；
2. 人工选择 2–5 个想继续处理的选题；
3. 打开 Agent 2 V1.0 表单；
4. 把 Agent 1 JSON 粘贴到 `agent1_json`；
5. 在 `approved_topics` 中填写选题编号或名称；
6. 提交后查看中文 Markdown 合规改写报告。

重要说明：本工具仅用于内容风险筛查和谨慎改写，不构成医疗、法律或平台合规意见。最终发布前仍需人工审核。

## Agent 4 Visual Director v0.1 DEV

Agent 4 已作为独立 n8n 工作流创建：

```text
04-Video-Director/n8n/ai-health-os-agent4-visual-director-v0.1-dev.json
```

它使用 n8n 官方 Form Trigger、Code 和 Form Ending 节点，不写磁盘，不调用本地 Python，不依赖外部图片或视频 API。

使用顺序：

1. 导入工作流 `AI Health OS - Agent 4 Visual Director v0.1 DEV`；
2. 在第 1 个节点粘贴 Agent 3 输出 JSON；
3. 逐节点测试到第 7 个节点；
4. 查看 Markdown Visual Report；
5. 只把 `ready_for_agent5 = true` 的视觉方案交给未来 Agent 5。

当前不要开发 Agent 5。
