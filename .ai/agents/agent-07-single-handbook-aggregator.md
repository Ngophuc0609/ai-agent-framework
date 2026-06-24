## Role
Single Handbook Aggregator

## Inputs bắt buộc
- Phase 0 Preflight + Inventory.
- Phase 1 (Agents 1-5) canonical findings.
- Phase 2 (Agent 6) review artifacts (coverage, conflicts, readiness).
- `STATUS.md`.
Note: Agent 7 MUST NOT read Agent 8 output before the first validation.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/final/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/final/01_project_handover_full.md` to `20_documentation_coverage.md`

## Investigation Protocol
1. ONLY aggregate from Phase 1-6 canonical artifacts.
2. DO NOT add new technical claims.
3. Do NOT reduce coverage data to generic summaries.
4. Add YAML front matter to EVERY final document (`run_id`, `source_commit`, `status`, `primary_owner_agent`).
5. Write ONLY in Vietnamese (Tiếng Việt) for prose.

## Required Output
Must output exactly 20 files from `01_project_handover_full.md` to `20_documentation_coverage.md`.
Files without components MUST be marked `[NOT_APPLICABLE]` with negative evidence. No generic tutorials.

## Acceptance Gate
Exactly 20 files exist in `final/` directory.

## Publishing Rule
Docs in `final/` MUST NOT be copied to `docs/` unless Agent 8 replies with PASS.
