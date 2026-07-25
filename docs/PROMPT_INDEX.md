# AI Health OS Prompt Index

This index summarizes important Codex prompt categories used during the V1 project. It does not invent verbatim historical prompts. Where exact prompts are not stored as prompt files, this document summarizes their purpose and points to the changed files that reflect the work.

## Master Orchestrator

- **Purpose:** Build and stabilize the Master workflow that runs Agent 1 through Agent 6 in sequence.
- **Relevant files:** `00-Workflow-Manager/n8n/ai-health-os-master-orchestrator-agent-1-6-v1.0.json`, `00-Workflow-Manager/tests/test_master_orchestrator_workflow.py`.

## Agent callable workflow conversion

- **Purpose:** Convert Agent workflows into callable sub-workflows that start with `When Executed by Another Workflow` and can be selected by n8n Execute Workflow nodes.
- **Relevant files:**
  - `00-Workflow-Manager/n8n/ai-health-os-agent1-memory-analysis-v1.1.json`
  - `00-Workflow-Manager/n8n/ai-health-os-agent2-compliance-rewriter-v1.1.json`
  - `03-Script-Writer/n8n/ai-health-os-agent3-script-writer-v1.1.json`
  - `04-Video-Director/n8n/ai-health-os-agent4-visual-director-v1.1.json`
  - `05-Voiceover-Subtitle-Producer/n8n/ai-health-os-agent5-voiceover-subtitle-producer-v1.1.json`
  - `06-Publishing-Package-Analytics/n8n/ai-health-os-agent6-publishing-package-analytics-v1.1.json`

## Execute Workflow node repair

- **Purpose:** Ensure Master Execute Workflow nodes use compatible n8n built-in Execute Workflow node structure and can resolve callable Agent workflows.
- **Relevant file:** `00-Workflow-Manager/n8n/ai-health-os-master-orchestrator-agent-1-6-v1.0.json`.

## Output contract repair

- **Purpose:** Add compatibility fields expected by the Master without changing Agent business logic.
- **Relevant files:** `00-Workflow-Manager/n8n/ai-health-os-agent1-memory-analysis-v1.1.json`, `00-Workflow-Manager/tests/test_agent1_memory_analysis_v11_workflow.py`.

## State preservation repair

- **Purpose:** Preserve Master metadata and accumulated Agent outputs/statuses after each Execute Workflow and Normalize stage.
- **Relevant files:** `00-Workflow-Manager/n8n/ai-health-os-master-orchestrator-agent-1-6-v1.0.json`, `00-Workflow-Manager/tests/test_master_orchestrator_workflow.py`.

## Connection graph repair

- **Purpose:** Ensure every Master Success Check has a TRUE branch to the next step and a FALSE branch to Unified Error Report.
- **Relevant files:** `00-Workflow-Manager/n8n/ai-health-os-master-orchestrator-agent-1-6-v1.0.json`, `00-Workflow-Manager/tests/test_master_orchestrator_workflow.py`.

## Documentation

- **Purpose:** Create the official documentation package for the completed AI Health OS V1 project.
- **Relevant files:** `README.md`, `CHANGELOG.md`, `docs/`, and `releases/v1.0/`.
