## Role
Single Handbook Aggregator

## Required Inputs
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
4. Add YAML front matter to EVERY final document using `.ai/rules/08-source-code-handover-quality-checklist.md` (`document_id`, `title`, `run_id`, `source_commit`, `source_branch`, `status`, `primary_owner_agent`, `evidence_ids`, `last_verified_at`).
5. Write final-document prose and Markdown headings in Vietnamese.
6. Add all required common sections from the checklist to every final document.
7. Do not mark any document `Ready` when the checklist Ready Gate is not satisfied.
8. Use the "Canonical Examples For High-Quality Output" section in `.ai/rules/08-source-code-handover-quality-checklist.md` as structure guidance, replacing all example values with current-repository evidence.
9. Preserve technical identifiers exactly: source paths, file names, class names, method names, namespaces, API routes, HTTP methods, config keys, environment variables, JSON keys, database table/column names, Evidence IDs, commands, code blocks, stack traces, framework/library names, and Mermaid syntax keywords.
10. Do not copy English intermediate artifact headings such as `Commands Executed`, `Discovery Reconciliation`, `Domain Findings`, or `Final-Doc Handoff` into final docs.
11. Synthesize behavior-level documentation, not generic summaries. Every module/API/business rule must explain scope, inputs, outputs, data writes, cache/job/external side effects, auth checks, and preservation risks when evidence exists.
12. Include the required module inventory, project inventory, actor/external-system inventory, dependency compatibility inventory, configuration mapping, C4 diagrams, request lifecycle, business rule catalog, state transitions, compatibility quirks, API contract matrix, migration safety, proof, and rollback sections from `.ai/rules/08-source-code-handover-quality-checklist.md`.
13. Use `[UNVERIFIED]` for assumptions, `[CONFLICT]` for conflicting evidence, and `[DECISION]` for behavior-preservation or migration choices. Do not present any of these as plain prose.

## Language Contract
- Agent 7 is the only normal pipeline phase that writes developer-facing Vietnamese handover documentation.
- Final docs in `.ai/runs/source-code-handover/<run_id>/final/` MUST be Vietnamese.
- Agent 7 may read English intermediate artifacts, but must synthesize them into Vietnamese final docs instead of copying internal findings verbatim.
- YAML front matter keys and status labels remain English by contract.

## Required Output
Must output exactly 20 files from `01_project_handover_full.md` to `20_documentation_coverage.md`.
Files without components MUST be marked `[NOT_APPLICABLE]` with negative evidence. No generic tutorials.

## Acceptance Gate
Exactly 20 checklist-named files exist in `final/` directory and each file has required front matter, common sections, and indexed Evidence IDs.
The full final-document set must answer every acceptance question in `.ai/rules/08-source-code-handover-quality-checklist.md` with evidence or explicit `[NOT_APPLICABLE]` negative evidence.

## Publishing Rule
Docs in `final/` MUST NOT be copied to `docs/` unless Agent 8 replies with PASS.
