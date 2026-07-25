# AI Health OS Project Bible

This document defines the permanent operating rules for AI Health OS V1 and future maintenance.

## Permanent project rules

1. **The Master only orchestrates.** The Master Orchestrator must not contain Agent business logic, content-generation logic, compliance logic, visual logic, subtitle logic, or publishing-package logic.
2. **Every Agent must start with `When Executed by Another Workflow`.** Callable Agent workflows must be compatible with n8n Execute Workflow / Execute Sub-workflow nodes.
3. **Every Agent must be independently testable.** Each Agent must be runnable and debuggable outside the Master Orchestrator.
4. **All Agent outputs must preserve agreed JSON field names.** Downstream Agents depend on stable field names such as `agent1_json`, `agent2_json`, `agent3_json`, `agent4_json`, `agent5_json`, `ranked_topics`, `scripts`, `visual_plans`, `voiceover_packages`, and `publishing_packages`.
5. **Existing stable workflow JSON files must never be edited directly without creating a new version.** Stable releases are preserved for rollback and auditability.
6. **Previous stable releases must always be preserved.** Do not overwrite release artifacts in `releases/`.
7. **All Codex prompts must be saved or summarized.** Prompt intent and resulting files must be documented so future maintainers understand why a change was made.
8. **Any change must be tested end-to-end before release.** A release is not stable until the Master can run Agent 1 through Agent 6 successfully.
9. **No Agent 7 development until explicitly approved.** V1 ends at Agent 6 and manual publishing review.
10. **Agent 6 must never auto-publish.** Agent 6 prepares a publishing package only.
11. **Human review is required before publishing.** All final packages require manual review for accuracy, claims, brand safety, and platform compliance.

## Stability policy

- V1 stable workflows should be treated as release assets.
- Changes should be made in a new versioned workflow when behavior changes.
- Documentation-only changes may update Markdown files without creating new workflow versions.

## Release gate

A release can be marked Stable only after:

- Agent 1 through Agent 6 complete successfully.
- The Master final report shows every Agent status as `success`.
- `final_publishing_packages.length >= 1`.
- Agent 6 returns `ready_for_manual_publish = true`.
- The report states that manual review is required.
