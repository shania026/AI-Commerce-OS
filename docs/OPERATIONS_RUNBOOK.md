# AI Health OS Operations Runbook

This runbook is for beginner operators running AI Health OS V1 in n8n.

## 1. Start Docker Desktop

1. Open Docker Desktop.
2. Wait until Docker shows it is running.
3. Start the n8n container if it is not already running.
4. Confirm the container exposes port `5678`.

## 2. Open n8n

1. Open a browser.
2. Go to `http://localhost:5678`.
3. Log in to n8n.

## 3. Import workflows

1. Import Agent workflows first.
2. Import the Master Orchestrator last.
3. Avoid duplicate workflow names. If a duplicate exists, rename or archive the older copy before importing the stable workflow.
4. Confirm that each Agent workflow starts with `When Executed by Another Workflow`.

## 4. Confirm a workflow is callable

1. Open the Master Orchestrator.
2. Open each Execute Workflow node.
3. Confirm the target Agent workflow appears in the selector.
4. Select the correct stable workflow if it is not already selected.
5. Save the Master workflow.

## 5. Run the Master Workflow

Use the Master input form and provide these test values:

- `topic`: Rooibos Tea Before Bed
- `product_name`: FYNELA Rooibos Tea
- `target_audience`: US wellness audience
- `target_platform`: TikTok
- `video_duration_seconds`: 30
- `language`: en-US
- `brand_tone`: warm, calm, educational, trustworthy
- `additional_requirements`: Educational content only. Avoid medical claims. Focus on a relaxing bedtime routine and general wellness education.
- `research_context`: Rooibos is a naturally caffeine-free herbal tea from South Africa. The content should focus on general wellness education, relaxation, and evening routines. Do not make disease treatment, prevention, cure, or guaranteed outcome claims.

Submit the form and wait for the execution to finish.

## 6. Inspect Executions

1. Open the n8n Executions page.
2. Select the latest Master Orchestrator execution.
3. Confirm each stage ran in order:
   - Master Input
   - Prepare Agent 1 Input
   - Execute Agent 1
   - Normalize Agent 1 Output
   - Agent 1 Success Check
   - Continue the same pattern through Agent 6
   - Build Final Master Report
   - AI Health OS Final Report

## 7. Identify the first failed node

If the workflow fails or routes to Unified Error Report:

1. Open the execution details.
2. Find the first red node or the first Success Check that took the false branch.
3. Open the node input and output panels.
4. Check `status`, `success`, `error_message`, `parse_error`, and required arrays.

## 8. Inspect Input and Output JSON

For any node:

1. Click the node in the execution view.
2. Open the Input tab.
3. Open the Output tab.
4. Verify expected JSON fields are present.
5. For Agent handoffs, confirm the full prior Agent output is passed as `agent1_json`, `agent2_json`, `agent3_json`, `agent4_json`, or `agent5_json`.

## 9. Export a workflow

1. Open the workflow.
2. Use the n8n export option.
3. Save the JSON with the stable filename or a new versioned filename.
4. Do not overwrite stable release files without creating a new version.

## 10. Import a workflow

1. Open n8n.
2. Select import workflow.
3. Choose the JSON file.
4. Save the workflow.
5. Confirm it appears in the workflow list.
6. Confirm callable workflows appear in Execute Workflow selectors.

## 11. Avoid duplicate workflow names

Duplicate names can confuse Execute Workflow selectors. Keep exactly one active stable copy for each workflow name. Archive old copies or add a clear suffix such as `ARCHIVE`.

## 12. Final success indicators

A successful V1 run should show:

- Agent 1–6 all succeeded.
- `final_publishing_packages.length >= 1`.
- Agent 6 QA score is 100 for the stable Rooibos test.
- `ready_for_manual_publish = true`.
- The final report includes a human-review disclaimer.
