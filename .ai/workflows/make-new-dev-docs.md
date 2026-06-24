# Source Code Handover Workflow

## Execution Isolation Policy
1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

Forbidden: `single-runtime-sequential-fallback`, `single-session-multi-role-execution`, `memory-only-agent-handoff`, `implicit-agent-output`, `direct-final-handbook-without-artifacts`

## Phase 0: Preflight + Deterministic Discovery
Before Agent 1-5 runs, the coordinator MUST create:
`.ai/runs/source-code-handover/<run_id>/inventory/` containing JSON files (projects, entry-points, dbcontexts, controllers, etc.) scanned from AST/CodeGraph/CLI. If a component is missing, create the inventory JSON with `0` count.

## Phase 1 to Phase 6 Pipeline
- Agent 1-5: Domain Analysis (Read Phase 0 inventory, match with source evidence).
- Agent 6: Evidence & Coverage Review (Must produce coverage-reconciliation.md).
- Agent 7: Final Documentation Assembly (Reads canonical artifacts, produces 20 files in `.ai/runs/.../final/`).
- Agent 8: Independent Final Validation (Runs `scan-source-code-handover-provenance.sh` and semantic checks, issues verdict).

## Final Validation
Must execute:
- git diff --check
- required output existence check
- canonical artifact/run ID validation
- STATUS.md consistency validation
- provenance/template contamination scan
- secret scan executed and passed
- Markdown/internal link validation
- evidence ID validation
- coverage reconciliation validation
- final docs content-contract validation
- no unresolved critical conflict omitted
- stack-appropriate build/test commands when environment permits
