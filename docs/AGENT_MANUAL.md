# AI Health OS Agent Manual

This manual documents the stable V1 Agent workflows.

## Agent 1

- **Workflow name:** `AI Health OS - Agent 1 Memory Analysis V1.1`
- **Purpose:** Rank health/wellness topic opportunities from Master input or CSV-style topic memory.
- **Expected input:** Master topic brief, `health_topics_csv`, topic, product name, audience, platform, duration, language, tone, and requirements.
- **Main processing stages:** Normalize uploaded CSV, parse CSV, memory analysis, score/rank topics, generate JSON ranking, generate Markdown decision report.
- **Expected output:** Ranked topic JSON with `ranked_topics`, `today_focus`, `today_limit`, `markdown_report`, and compatibility status fields.
- **Required compatibility fields:** `success`, `agent`, `status`, `ranked_topics`, `handoff.ready_count`.
- **Handoff target:** Agent 2 via `agent1_json`.
- **Common failure modes:** Missing topic data, malformed CSV, empty ranked topics, missing success compatibility fields.
- **Manual test method:** Execute the Agent directly with `When Executed by Another Workflow` test data or run it through the Master input form.

## Agent 2

- **Workflow name:** `AI Health OS - Agent 2 Health Compliance Rewriter V1.1`
- **Purpose:** Check and rewrite Agent 1 topic output for safer health-compliance framing.
- **Expected input:** Full Agent 1 output as `agent1_json`.
- **Main processing stages:** Normalize Agent 1 JSON, select topics, rewrite unsafe phrasing, apply compliance QA, produce handoff JSON/Markdown.
- **Expected output:** Compliance-safe results and items ready for Agent 3.
- **Required compatibility fields:** `status`, `compliance_results` or equivalent result array, `ready_for_agent3`, `handoff.ready_count`.
- **Handoff target:** Agent 3 via `agent2_json`.
- **Common failure modes:** Empty Agent 1 result array, malformed JSON string, no item marked ready for Agent 3.
- **Manual test method:** Execute with a known Agent 1 JSON payload and verify `handoff.ready_count >= 1`.

## Agent 3

- **Workflow name:** `AI Health OS - Agent 3 Script Writer V1.1`
- **Purpose:** Convert compliance-safe topic output into short-form video scripts.
- **Expected input:** Full Agent 2 output as `agent2_json`.
- **Main processing stages:** Normalize Agent 2 JSON, select ready content, generate hook/body/video script fields, QA script readiness, produce Markdown report.
- **Expected output:** `scripts[]` with script metadata and handoff readiness.
- **Required compatibility fields:** `status`, `scripts`, `ready_for_agent4` or `handoff.ready_count`.
- **Handoff target:** Agent 4 via `agent3_json`.
- **Common failure modes:** `scripts.length = 0`, no ready script, missing `hook` or `body`.
- **Manual test method:** Execute with known Agent 2 JSON and verify at least one script is ready for Agent 4.

## Agent 4

- **Workflow name:** `AI Health OS - Agent 4 Visual Director V1.1`
- **Purpose:** Transform Agent 3 scripts into visual plans for production.
- **Expected input:** Full Agent 3 output as `agent3_json`.
- **Main processing stages:** Normalize scripts, create storyboard, scene list, shot list, camera movement, B-roll, on-screen text, AI image/video prompts, visual style, QA, Markdown report.
- **Expected output:** `visual_plans[]` or compatible visual project array.
- **Required compatibility fields:** `status`, `visual_plans`, `ready_for_agent5`, `handoff.ready_count`.
- **Handoff target:** Agent 5 via `agent4_json`.
- **Common failure modes:** Empty scripts array, false medical-risk detection, no visual plan marked ready.
- **Manual test method:** Execute with real Agent 3 JSON and verify `ready_for_agent5 = true`.

## Agent 5

- **Workflow name:** `AI Health OS - Agent 5 Voiceover & Subtitle Producer V1.1`
- **Purpose:** Produce voiceover and subtitles from Agent 4 visual plans.
- **Expected input:** Full Agent 4 output as `agent4_json`.
- **Main processing stages:** Normalize visual plans, generate voiceover script, narration segments, subtitle segments, SRT, TTS prompt, pacing notes, subtitle QA, Markdown report.
- **Expected output:** `voiceover_packages[]` ready for publishing packaging.
- **Required compatibility fields:** `status`, `voiceover_packages`, `qa_passed`, `ready_for_agent6`, `handoff.ready_count`.
- **Handoff target:** Agent 6 via `agent5_json`.
- **Common failure modes:** Empty visual plans, no ready package, subtitle QA false positive, missing SRT.
- **Manual test method:** Execute with real Agent 4 JSON and verify voiceover, subtitles, SRT, and `ready_for_agent6 = true`.

## Agent 6

- **Workflow name:** `AI Health OS - Agent 6 Publishing Package & Analytics V1.1`
- **Purpose:** Generate the final manual publishing package.
- **Expected input:** Full Agent 5 output as `agent5_json`.
- **Main processing stages:** Normalize voiceover packages, generate captions, hashtags, SEO keywords, CTA, cover text, publishing checklist, analytics template, A/B test plan, Publishing QA, Markdown report.
- **Expected output:** `publishing_packages[]` and final readiness fields.
- **Required compatibility fields:** `status`, `publishing_packages`, `qa_passed`, `ready_for_manual_publish`, `handoff.ready_count`.
- **Handoff target:** Manual human review and manual publishing.
- **Common failure modes:** Empty voiceover packages, QA failure, missing captions or hashtags, missing manual-review disclaimer.
- **Manual test method:** Execute with real Agent 5 JSON and verify `publishing_packages.length >= 1`, QA passes, and `ready_for_manual_publish = true`.
