# AI Health OS Project Structure

This document explains the repository layout for AI Health OS V1.

## Top-level structure

```text
00-Workflow-Manager/
01-Viral-Finder/
02-Compliance-Rewriter/
03-Script-Writer/
04-Video-Director/
05-Voiceover-Subtitle-Producer/
06-Publishing-Package-Analytics/
12-Docs/
docs/
Inputs/
Outputs/
Reports/
releases/
CHANGELOG.md
README.md
```

## Workflow manager

`00-Workflow-Manager/` contains the CLI Workflow Manager and n8n orchestration assets. It includes:

- `workflow.py` for local Agent 1 MVP runs.
- Master Orchestrator n8n JSON.
- Agent 1 and Agent 2 n8n workflow exports.
- Workflow Manager docs and tests.

## Agent folders

Each Agent folder documents or implements one stage of the pipeline:

- `01-Viral-Finder/`: Agent 1 ranking logic and Python implementation.
- `02-Compliance-Rewriter/`: Agent 2 documentation, prompt, and tests.
- `03-Script-Writer/`: Agent 3 n8n workflows, docs, prompt, and tests.
- `04-Video-Director/`: Agent 4 n8n workflows, visual prompt, docs, and tests.
- `05-Voiceover-Subtitle-Producer/`: Agent 5 n8n workflows, prompt, docs, and tests.
- `06-Publishing-Package-Analytics/`: Agent 6 n8n workflows, prompt, docs, and tests.

## n8n JSON exports

n8n workflow JSON exports live under each relevant `n8n/` directory. Stable V1 callable workflows use V1.1 Agent names and the Master V1.0 name.

## Tests

Tests live under each module's `tests/` directory. They include:

- Python unit tests.
- n8n workflow structure checks.
- Node.js execution of embedded n8n Code-node JavaScript.

## Documentation

Documentation is split into:

- `docs/`: official V1 documentation package.
- Agent-specific `docs/` directories.
- `12-Docs/`: blueprint and project planning documents.

## Prompts

Prompt files live under each Agent's `prompts/` directory. Prompt changes must be documented in `docs/PROMPT_INDEX.md`.

## Releases

`releases/` stores release documentation and manifests. Stable workflow exports should be referenced, not moved or overwritten.

## Archive

If deprecated workflow exports or previous versions need to be retained outside the active folders, create an `archive/` folder and document what was archived and why. Do not delete stable releases.
