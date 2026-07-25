# AI Health OS：MVP 工作流蓝图（产品经理版）

## 1. 这份文档给谁看？

这份文档不是给程序员看的，而是给产品经理看的。

你不需要懂代码，也不需要一次把整个 AI Health OS 做完。我们会按照 MVP（最小可运行产品）的方式，一次只做一个 Agent。

每完成一个 Agent，都必须做到：

1. 说明它负责什么；
2. 创建它需要的文件；
3. 写好可复制给 AI 的 Prompt；
4. 写好带中文注释的代码；
5. 用中文教你如何测试；
6. 等你确认以后，再继续下一个 Agent。

## 2. 项目目标

AI Health OS 的目标是帮助你做一个面向美国市场的健康短视频账号。

内容方向包括：

- 健康冷知识；
- 日常生活里容易忽略的小健康问题；
- 中国中医草本概念；
- 南非草本植物；
- 美国用户听得懂、愿意看、愿意保存和转发的短视频；
- 最后通过合规方式实现带货、联盟货、茶饮产品、草本产品或内容电商转化。

## 3. MVP 原则：不要一次开发整个系统

错误做法：一次开发完整 AI Health OS，包括选题、脚本、视频、配音、发布、数据分析和带货。

正确做法：先做最小闭环。

第一阶段只做：

```text
候选选题表格
  -> Agent 1：健康选题发现
  -> 输出今天优先做的 2-5 个选题
  -> 你人工确认
```

确认 Agent 1 好用以后，再做 Agent 2。

## 4. 推荐 Agent 开发顺序

### Agent 1：健康选题发现 Agent（现在先做这个）

负责：从一批候选选题里，筛选最适合今天制作的健康短视频选题。

它会看：

- 用户是否会好奇；
- 痛点是否明显；
- 是否适合美国市场；
- 是否容易带到产品；
- 是否容易拍成画面；
- 是否存在健康合规风险。

### Agent 2：健康合规改写 Agent（等你确认后再做）

负责：把高风险健康表达改成更安全的美国市场表达。

例如：

- 不说“治疗糖尿病”；
- 改成“支持日常健康习惯”或“传统上用于某类日常调理场景”；
- 对疾病、药物、孕妇、慢性病等内容提示人工确认。

### Agent 3：短视频脚本 Agent

负责：把确认过的选题写成 20-45 秒英文短视频脚本。

### Agent 4：画面导演 Agent

负责：把脚本拆成镜头、画面、字幕位置和素材需求。

### Agent 5：AI 视频/图片 Prompt Agent

负责：给 Runway、Pika、Canva 或其他 AI 工具生成画面 Prompt。

### Agent 6：配音和字幕 Agent

负责：生成英文旁白、字幕和短视频屏幕文字。

### Agent 7：发布文案 Agent

负责：生成标题、描述、话题标签、联盟披露和产品链接备注。

### Agent 8：数据复盘 Agent

负责：根据播放、完播、收藏、评论和点击数据，告诉你明天应该继续做什么选题。

## 5. 美国市场健康内容合规底线

健康内容属于高风险内容。为了保护账号和商业化路径，所有 Agent 都必须遵守这些底线。

### 可以做的表达

- “may support”：可能支持；
- “traditionally used”：传统上用于；
- “daily wellness routine”：日常健康习惯；
- “caffeine-free tea swap”：无咖啡因茶饮替换；
- “supports healthy digestion”：支持健康消化；
- “helps maintain hydration”：帮助维持水分摄入。

### 不要做的表达

- 不说治疗、治愈、预防、逆转疾病；
- 不说“7 天见效”；
- 不说“清血”“排毒治病”“根治”；
- 不针对糖尿病、高血压、癌症、脂肪肝等疾病做产品承诺；
- 不替代医生建议。

### 需要记住的官方参考

- FDA 对膳食补充剂结构/功能声称的说明：<https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/structurefunction-claims>
- FDA 对健康声称和结构/功能声称区别的说明：<https://www.fda.gov/food/dietary-supplements-guidance-documents-regulatory-information/dietary-supplement-labeling-guide-chapter-vi-claims>
- FTC 对健康产品广告证据要求的说明：<https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance>
- TikTok 医疗健康广告政策需要定期复查：<https://ads.tiktok.com/help/article/tiktok-ads-policy-healthcare-pharmaceuticals>

## 6. 当前 MVP：Agent 1 文件清单

本次只创建 Agent 1，不开发后面的 Agent。

Agent 1 文件包括：

- `01-Viral-Finder/README.md`：中文说明文档；
- `01-Viral-Finder/health_topic_finder.py`：带中文注释的 Python 代码；
- `01-Viral-Finder/prompts/health-topic-finder.prompt.md`：给 Codex 或 AI 使用的 Prompt；
- `01-Viral-Finder/examples/health_topics.csv`：测试用的候选选题表格。

## 7. Agent 1 怎么测试？

你只需要在项目根目录运行这一条命令：

```bash
python 01-Viral-Finder/health_topic_finder.py \
  --input 01-Viral-Finder/examples/health_topics.csv \
  --output 01-Viral-Finder/examples/ranked_health_topics.json \
  --limit 5
```

如果成功，会生成：

```text
01-Viral-Finder/examples/ranked_health_topics.json
```

你可以打开这个文件，看系统推荐哪些选题先做。

## 8. 你确认 Agent 1 时，只需要看什么？

你不用看代码。

你只需要看输出结果是否符合你的商业直觉：

1. 推荐的选题是不是美国用户可能感兴趣？
2. 是否优先推荐了 rooibos、茶饮、日常健康习惯这类低风险内容？
3. 是否把“治疗糖尿病”等高风险选题标记出来？
4. 输出的 2-5 个选题是否值得进入脚本阶段？

如果你觉得 OK，我们再继续 Agent 2：健康合规改写 Agent。
