# AI Health OS Release Checklist

Use this checklist before marking any future release stable.

## Backup and import

- [ ] Backup current stable JSON files.
- [ ] Import into a clean n8n test workflow environment.
- [ ] Avoid duplicate workflow names.
- [ ] Confirm Execute Workflow selectors resolve the intended workflows.

## Callable Agent requirements

- [ ] Confirm Agent 1 starts with `When Executed by Another Workflow`.
- [ ] Confirm Agent 2 starts with `When Executed by Another Workflow`.
- [ ] Confirm Agent 3 starts with `When Executed by Another Workflow`.
- [ ] Confirm Agent 4 starts with `When Executed by Another Workflow`.
- [ ] Confirm Agent 5 starts with `When Executed by Another Workflow`.
- [ ] Confirm Agent 6 starts with `When Executed by Another Workflow`.

## Master Orchestrator requirements

- [ ] Confirm all Success Checks take the TRUE branch during the happy-path test.
- [ ] Confirm every Success Check has a FALSE branch to Unified Error Report.
- [ ] Confirm Unified Error Report paths work.
- [ ] Confirm state fields remain present through the final report.
- [ ] Confirm `agent_1_status` through `agent_6_status` are present.
- [ ] Confirm all six Agent statuses are `success`.

## Final output requirements

- [ ] Confirm `final_publishing_packages.length >= 1`.
- [ ] Confirm QA score is present.
- [ ] Confirm `ready_for_manual_publish = true`.
- [ ] Confirm no auto-publishing behavior exists.
- [ ] Confirm no upload to TikTok, Instagram, YouTube, or ad/comment service occurs.
- [ ] Confirm human review disclaimer appears.

## Release tagging

- [ ] Run the full end-to-end test.
- [ ] Save the test evidence.
- [ ] Update documentation and manifest.
- [ ] Tag release only after end-to-end test passes.
