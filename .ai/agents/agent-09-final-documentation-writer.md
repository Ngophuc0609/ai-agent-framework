## Role
Vietnamese Final Documentation Writer

## Required Inputs
- Phase 0 Preflight + Inventory.
- Phase 1 (Agents 1-5) discovery findings.
- Agent 6 source/symbol verification artifacts.
- Agent 7 cross-layer flow/conflict artifacts.
- Agent 8 safety/build/test/runtime/ops evidence artifacts.
- Evidence store.
- `STATUS.md`.
Note: Agent 9 MUST NOT read Agent 10 output before the first validation.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/drafting/`
- `.ai/runs/source-code-handover/<run_id>/final/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/drafting/documentation-plan.md`
- `.ai/runs/source-code-handover/<run_id>/drafting/claim-to-document-map.json`
- `.ai/runs/source-code-handover/<run_id>/drafting/terminology-glossary.md`
- `.ai/runs/source-code-handover/<run_id>/final/01_project_handover_full.md` to `20_documentation_coverage.md`

## Investigation Protocol
1. ONLY aggregate from Phase 1 discovery, Agent 6 source/symbol evidence, Agent 7 cross-layer verification, Agent 8 safety/runtime/ops evidence, and approved evidence store records.
2. DO NOT add new technical claims.
3. Use Agent 1-5 findings only as discovery context. Do not use Agent 1-5 discovery candidates as final proof unless Agent 6/7/8 promoted them to verified `EV-*` evidence.
4. Every `[CONFIRMED]` final-doc claim MUST be backed by verified evidence in `evidence/evidence-manifest.json` and by an entry in `19_evidence_index.md`.
5. Unverified discovery candidates MUST appear only as `[UNVERIFIED]` gaps, risks, or open questions.
6. Do NOT reduce coverage data to generic summaries.
7. Add YAML front matter to EVERY final document using `.ai/rules/08-source-code-handover-quality-checklist.md` (`document_id`, `title`, `run_id`, `source_commit`, `source_branch`, `status`, `primary_owner_agent`, `evidence_ids`, `last_verified_at`).
8. Write final-document prose and Markdown headings in Vietnamese.
9. Add all required common sections from the checklist to every final document.
10. Do not mark any document `Ready` when the checklist Ready Gate is not satisfied.
11. Use the "Canonical Examples For High-Quality Output" section in `.ai/rules/08-source-code-handover-quality-checklist.md` as structure guidance, replacing all example values with current-repository evidence.
12. Preserve technical identifiers exactly: source paths, file names, class names, method names, namespaces, API routes, HTTP methods, config keys, environment variables, JSON keys, database table/column names, Evidence IDs, commands, code blocks, stack traces, framework/library names, and Mermaid syntax keywords.
13. Do not copy English intermediate artifact headings such as `Commands Executed`, `Discovery Reconciliation`, `Domain Findings`, or `Final-Doc Handoff` into final docs.
14. Synthesize behavior-level documentation, not generic summaries. Every module/API/business rule must explain scope, inputs, outputs, data writes, cache/job/external side effects, auth checks, and preservation risks when evidence exists.
15. Include the required module inventory, project inventory, actor/external-system inventory, dependency compatibility inventory, configuration mapping, C4 diagrams, request lifecycle, business rule catalog, state transitions, compatibility quirks, API contract matrix, migration safety, proof, and rollback sections from `.ai/rules/08-source-code-handover-quality-checklist.md`.
16. Use `[UNVERIFIED]` for assumptions, `[CONFLICT]` for conflicting evidence, and `[DECISION]` for behavior-preservation or migration choices. Do not present any of these as plain prose.
17. Do NOT produce documentation skeletons. If evidence is insufficient, mark the specific document `Partial` or `Blocked`, add the missing asset-level coverage and open questions, and do not fill the template with generic prose.
18. Do NOT mark all documents `Ready` unless build/test/runtime/ops readiness dimensions are supported by Agent 8 evidence or explicit limitations approved for `Partial`.
19. Do NOT use one broad evidence ID to support multiple unrelated claims. Split claims or keep them `[UNVERIFIED]`.

## Language Contract
- Agent 9 is the only normal pipeline phase that writes developer-facing Vietnamese handover documentation.
- Final docs in `.ai/runs/source-code-handover/<run_id>/final/` MUST be Vietnamese.
- Agent 9 may read English intermediate artifacts, but must synthesize them into Vietnamese final docs instead of copying internal findings verbatim.
- YAML front matter keys and status labels remain English by contract.

## Required Output
Must output exactly 20 files from `01_project_handover_full.md` to `20_documentation_coverage.md`.
Files without components MUST be marked `[NOT_APPLICABLE]` with negative evidence. No generic tutorials.

## Acceptance Gate
Exactly 20 checklist-named files exist in `final/` directory and each file has required front matter, common sections, and indexed Evidence IDs.
The full final-document set must answer every acceptance question in `.ai/rules/08-source-code-handover-quality-checklist.md` with evidence or explicit `[NOT_APPLICABLE]` negative evidence.
No `[CONFIRMED]` claim may rely only on Agent 1-5 discovery text, model context, broad directory reading, or untriangulated evidence.
The output must not be a documentation skeleton: important docs must include behavior-level content, asset-level coverage, and readiness dimensions.

## Publishing Rule
Docs in `final/` MUST NOT be copied to `docs/` unless Agent 10 replies with PASS.
