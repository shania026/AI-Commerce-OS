# AI Health OS V1 Repository Cleanup Plan

## Purpose and constraints

This plan classifies the repository's current top-level folders after the AI Health OS V1.0 release. It is an assessment only: no files or folders should be deleted, moved, or renamed until the proposed archive candidates and manual-review items have been approved.

## Core AI Health OS V1.0 (keep)

### `00-Workflow-Manager/`

Keep as the orchestration layer for AI Health OS V1.0. It contains the Master Orchestrator, callable Agent 1 and Agent 2 workflow exports, the local workflow manager, tests, and operating documentation.

### `01-Viral-Finder/`

Keep as the Agent 1 implementation and support package. It contains topic-ranking logic, configuration, prompts, examples, tests, and the Agent 1 user manual.

### `02-Compliance-Rewriter/`

Keep as the Agent 2 module. Its compliance-rewriting prompt, tests, and documentation support the second stage of the stable Agent 1–6 chain.

### `03-Script-Writer/`

Keep as the Agent 3 module. It contains the stable callable Script Writer workflow together with its prompt, tests, release notes, and operating documentation.

### `04-Video-Director/`

Keep as the Agent 4 module. It contains the stable Visual Director workflow and the documentation, prompt, and tests needed to maintain its visual-planning handoff.

### `05-Voiceover-Subtitle-Producer/`

Keep as the Agent 5 module. It owns the stable voiceover, subtitle, and SRT workflow along with its interface documentation, prompt, and regression tests.

### `06-Publishing-Package-Analytics/`

Keep as the Agent 6 module and final automated stage of V1.0. It produces the manual publishing package and analytics template without performing automatic publication.

### `12-Docs/`

Keep because it contains the AI Health OS workflow blueprint and cross-links to the Agent documentation. Its planning-oriented name overlaps with `docs/`, but its V1 blueprint remains relevant release context.

### `Inputs/`

Keep as the standardized runtime input location used by the Workflow Manager. It also contains the tracked health-topic CSV used for the V1 example flow.

### `Outputs/`

Keep as the standardized location for machine-readable runtime output. The tracked placeholder preserves the directory while generated output remains outside the committed release content.

### `Reports/`

Keep as the standardized location for human-readable runtime reports. The tracked placeholder preserves the directory expected by the Workflow Manager.

### `docs/`

Keep as the official AI Health OS V1 documentation package. It contains architecture, governance, operations, release, prompt-index, and project-structure documentation, including this cleanup plan.

### `releases/`

Keep as the authoritative location for versioned release metadata. The V1.0 manifest identifies the stable workflow set and records release readiness and manual-publishing safeguards.

## Legacy AI Commerce OS (candidate for archive)

### `02-Trend-Analyzer/`

Candidate for archive because it is an earlier AI Commerce OS planning module with only a placeholder README and no V1 implementation. Trend analysis is not a separate stage in the released AI Health OS Agent 1–6 chain.

### `05-Image-Prompt-Generator/`

Candidate for archive because it is a placeholder for a separate image-prompt module. AI Health OS V1 handles visual prompts inside Agent 4 rather than through this folder.

### `06-Runway-Video-Producer/`

Candidate for archive because it contains only future Runway production planning and is not executed by the V1 Master Orchestrator. V1 ends with a publishing package and does not generate or upload video automatically.

### `07-Voice-Over/`

Candidate for archive because its planned voice-over responsibility is now covered by Agent 5. The folder contains no active implementation used by the V1 chain.

### `08-Subtitle-Generator/`

Candidate for archive because subtitle and SRT generation are now responsibilities of Agent 5. This older folder is a planning placeholder rather than an active V1 module.

### `09-Auto-Publisher/`

Candidate for archive because automatic publishing is explicitly outside the AI Health OS V1 safety boundary. Agent 6 prepares content for human review and does not invoke publishing platforms.

### `10-Analytics/`

Candidate for archive because its standalone analytics module is not part of the released chain. Agent 6 already generates the V1 analytics template and A/B test plan.

### `11-Assets/`

Candidate for archive because it is a generic AI Commerce OS asset placeholder with no active V1 release assets. Any future asset policy should be defined before this folder is reintroduced into the core structure.

### `projects/`

Candidate for archive because it contains the pre-V1 Rooibos TikTok example project rather than the reusable AI Health OS platform. It may remain valuable as a historical reference or fixture, but it is not part of the active Agent 1–6 runtime structure.

## Needs manual review

### `Workflows/`

Manual review is required because this top-level folder currently serves only as an empty placeholder, while all active n8n exports live in module-specific `n8n/` directories. Decide whether it represents a future centralized export policy or should become an archive candidate in a later cleanup change.

## Recommended next review

1. Confirm that no external automation, documentation link, or deployment process depends on an archive-candidate path.
2. Decide whether historical examples belong under a future `archive/` area or should remain in place with explicit legacy labels.
3. Resolve the intended role of `Workflows/` before changing it.
4. Create a separately reviewed cleanup change only after the archive policy and rollback plan are approved.
