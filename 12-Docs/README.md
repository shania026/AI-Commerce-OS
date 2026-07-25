# 12-Docs

Purpose: Maintain project documentation, operating procedures, architecture notes, and planning references.

This folder will contain documentation for AI-Commerce-OS as the project evolves. No implementation code is included yet.

## Planning Documents

- [AI Health OS Workflow Blueprint](ai-health-os-workflow-blueprint.md): strategy, compliance guardrails, Codex preparation checklist, and workflow modules for a US-facing herbal wellness short-video commerce account.

- [Agent 2 Health Compliance Rewriter V1.0](../02-Compliance-Rewriter/README.md): independent n8n workflow for health claim risk screening, safe rewriting, and JSON/Markdown compliance reports after Agent 1 human confirmation.
- [Agent 3 Script Writer V1.0](../03-Script-Writer/README.md): independent n8n workflow that turns Agent 2 approved topics into English TikTok/Reels/Shorts scripts with QA and JSON/Markdown script reports.
- [Agent 4 Visual Director v0.1 DEV](../04-Video-Director/README.md): independent n8n workflow that turns Agent 3 QA-passed scripts into vertical short-video visual plans, shot tables, image/video prompts, and Markdown visual reports.
- [Agent 5 Voiceover & Subtitle Producer v0.1 DEV](../05-Voiceover-Subtitle-Producer/README.md): independent n8n workflow that turns Agent 4 ready visual plans into English voiceover scripts, subtitles, SRT, pacing notes, TTS prompts, and Markdown reports.
- [Agent 6 Publishing Package & Analytics v0.1 DEV](../06-Publishing-Package-Analytics/README.md): independent n8n workflow that turns Agent 5 ready voiceover/subtitle packages into platform captions, titles, hashtags, SEO keywords, publishing checklists, analytics templates, and A/B test plans.
