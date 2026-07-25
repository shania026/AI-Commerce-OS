# AI Health OS V1

AI Health OS is an n8n-based automation system for producing health and wellness short-video publishing packages from a structured content brief. It coordinates six independent agents that rank a topic, rewrite it for safer health-compliance language, write a script, create a visual plan, produce voiceover/subtitle assets, and assemble a final publishing package.

## V1 status

**AI Health OS V1 is complete and stable as of 2026-07-24.** The confirmed V1 chain runs automatically from the Master Orchestrator through Agent 1, Agent 2, Agent 3, Agent 4, Agent 5, and Agent 6, then returns a Final Publishing Package.

## Stable end-to-end flow

```text
Master Orchestrator
→ Agent 1: Memory Analysis / Topic Ranking
→ Agent 2: Health Compliance Rewriter
→ Agent 3: Script Writer
→ Agent 4: Visual Director
→ Agent 5: Voiceover & Subtitle Producer
→ Agent 6: Publishing Package & Analytics
→ Final Publishing Package
```

## Stable workflow names

Import and use these workflow names exactly:

1. `AI Health OS - Master Orchestrator Agent 1-6 V1.0`
2. `AI Health OS - Agent 1 Memory Analysis V1.1`
3. `AI Health OS - Agent 2 Health Compliance Rewriter V1.1`
4. `AI Health OS - Agent 3 Script Writer V1.1`
5. `AI Health OS - Agent 4 Visual Director V1.1`
6. `AI Health OS - Agent 5 Voiceover & Subtitle Producer V1.1`
7. `AI Health OS - Agent 6 Publishing Package & Analytics V1.1`

## Quick start: import into n8n

1. Start Docker Desktop.
2. Open n8n at `http://localhost:5678`.
3. Import the six Agent workflows first.
4. Import the Master Orchestrator workflow last.
5. Open the Master Orchestrator.
6. Confirm each Execute Workflow node can select the correct Agent workflow.
7. Run the Master workflow from the Master input form.
8. Inspect the final execution output and Final Publishing Package.

## Important publishing warning

Agent 6 **does not auto-publish**. It does not upload videos to TikTok, Instagram, YouTube, or any other platform. The final package is prepared for **manual human review** only. A human must approve all content before publishing.

## Release documentation

See:

- `docs/PROJECT_BIBLE.md`
- `docs/ARCHITECTURE.md`
- `docs/AGENT_MANUAL.md`
- `docs/OPERATIONS_RUNBOOK.md`
- `releases/v1.0/MANIFEST.md`
