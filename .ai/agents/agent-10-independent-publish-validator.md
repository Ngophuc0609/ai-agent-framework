## Role
Independent Publish Validator

## Required Inputs
- `.ai/runs/source-code-handover/<run_id>/metadata/`
- `.ai/runs/source-code-handover/<run_id>/inventory/`
- `.ai/runs/source-code-handover/<run_id>/evidence/`
- `.ai/runs/source-code-handover/<run_id>/verification/`
- `.ai/runs/source-code-handover/<run_id>/drafting/`
- `.ai/runs/source-code-handover/<run_id>/final/`
- Current repository source files.
- `STATUS.md`

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/validation/`
- `.ai/runs/source-code-handover/<run_id>/publish/`

## Canonical Artifact
- `mechanical-validation.md`
- `semantic-validation.md`
- `onboarding-usability-review.md`
- `provenance-scan.md`
- `evidence-validation.md`
- `coverage-validation.md`
- `links-validation.md`
- `secret-scan.md`
- `language-validation.md`
- `evidence-store-validation.md`
- `tool-orchestration-validation.md`
- `source-change-validation.md`
- `final-quality-report.md`
- `final-verdict.md`
- `publish/publish-manifest.json`
- `publish/release-note.md`

## Validation Rules
1. **Independence**: Validate final docs without accepting Agent 9 prose as proof. Use only evidence store, verification artifacts, current source files, and deterministic validation scripts.
2. **Provenance & Template Guard**: Check configurable patterns (dotnet new, github.com/skoruba, example.com, Password123, Hangfire or Quartz, NotificationHub, sample only, etc.). Fail if present without `[UPSTREAM_REFERENCE]`.
3. **Evidence**: `[CONFIRMED]` claims must have Evidence IDs in `19_evidence_index.md` and `evidence/evidence-manifest.json`.
4. **Physical Provenance**: Cross-check final Evidence IDs against `focused-slices.json`, verification artifacts, and current repository files. Reject if any final `EV-*` ID is missing, stale, lacks source path/object, or points to a non-existent repo file when `source_type=source`.
5. **Discovery Promotion Guard**: Reject final docs when any `DISC-*` ID appears in final documentation.
6. **Triangulation**: High-risk claims must be supported by Agent 6 source/symbol evidence, Agent 7 cross-layer flow/conflict review, and Agent 8 safety/runtime/ops evidence or explicit limitations.
7. **Coverage**: 20 files must exist. YAML front matter exists. Status matches inventory and verification readiness.
8. **Safety**: Secret scan executed and passed.
9. **Links**: Internal relative links must not be broken.
10. **Checklist**: Validate `.ai/rules/08-source-code-handover-quality-checklist.md`, including exact filenames, required front matter keys, required common sections, claim labels, Evidence ID index coverage, negative evidence for `[NOT_APPLICABLE]`, document-specific minimums, and Ready Gate blockers.
11. **Example Calibration**: Compare final docs against the "Canonical Examples For High-Quality Output" section in `.ai/rules/08-source-code-handover-quality-checklist.md`; reject docs that resemble the bad examples or only restate requirements without evidence-backed content.
12. **Language Compliance**: Validate the language matrix:
    - Intermediate artifacts in `inventory/`, `discovery/`, `findings/`, `verification/`, `validation/`, and `STATUS.md` are English.
    - Final docs in `final/` are Vietnamese.
    - Non-code prose in final docs is not primarily English.
    - Technical identifiers remain unchanged.
    - Internal English artifact headings are not copied into final docs.
13. **Behavior-Level Completeness**: Reject generic module/API descriptions that lack scope, actor/client, data read/write locations, auth/permission checks, side effects, business rules, or evidence.
14. **Migration Safety**: Reject if final docs do not answer what must not change in `.NET 8`, how equivalence will be proven, and how rollback works for risky modules.
15. **Required Matrices**: Validate that the final set includes project inventory, module inventory, API contract matrix, configuration mapping, dependency compatibility, external systems, business rules, state transitions where applicable, quirks, Redis/cache/jobs/queue behavior, and acceptance-question coverage.
16. **Source Change Guard**: If `metadata/source-manifest.jsonl` exists, validate the current source snapshot is not stale before allowing publish.
17. **Skeleton Rejection**: Reject `DOCUMENTATION_SKELETON_ONLY` outputs: thin files, broad reused evidence, category-level coverage denominators, all-Ready status without build/test/runtime/ops evidence, or final docs that merely restate template headings.
18. **Readiness Matrix**: Validate separate statuses for documentation structure, source discovery, evidence quality, documentation coverage, local setup, build, test, runtime, operations, and production handover.
19. **Application Integration Completeness**: Reject `09_api_catalog.md` when discovered APIs lack route, method, auth header shape, required headers, request example, success example, error example, status codes, side effects, curl command, evidence, and status. Gateway/proxy path and upstream service/path are required only when gateway/proxy evidence exists. Versioning, timeout, retry, idempotency, rate limit, and Postman/OpenAPI references belong in a separate policy/source table only when source/config/test/runtime evidence exists; do not require or accept invented per-endpoint values.
20. **External Integration Completeness**: Reject `12_external_integrations.md` when discovered external APIs, upstream/downstream services, service discovery, Redis/cache, queues, webhooks, or gateway destinations lack caller, trigger, protocol, direction, auth method without secrets, config keys, contract, timeout/retry/fallback behavior, failure behavior, health/test strategy, owner when known, evidence, and status.
21. **Operations Debug Completeness**: Reject `14_operations_runbook.md` when it lacks runtime topology, service/port/domain map, dependency map, health checks, log/trace checks, reverse-proxy/upstream map when applicable, fault-isolation matrix, verification commands, fix/next action, rollback, escalation, and incident families for auth, route, upstream, config/service discovery, Redis/cache, database when present, external API, realtime, background jobs, CORS/TLS, and deployment rollback.
22. **Database Operations Completeness**: Reject `07_database_reference.md` when a database exists and any discovered DbContext, DbSet, entity, table, important column, relationship, migration/schema source, seed/reset path, read/write consumer, or data-risk note is missing without an explicit unresolved/negative-evidence record.
23. **Secret Redaction**: Reject final docs, validation reports, and evidence summaries that copy secret values. It is allowed to identify the config key and file path, but values must be redacted.
24. **Evidence-Bound Cells**: Reject `[CONFIRMED]` rows that contain timeout, retry, fallback, rate-limit, auth-header, status/error behavior, success/error example, owner, health/smoke command, Postman/OpenAPI/test source, or external API contract values when the same row cites only broad route/config evidence. These cells require matching source/config/test/runtime evidence, otherwise the row must be `[UNVERIFIED]`, `[INFERRED]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.
25. **Executable Runbook Commands**: Reject runbook commands that reference routes, health endpoints, Docker/Kubernetes commands, certificate paths, trace/correlation IDs, owners, or rollback mechanisms not present in current source/config/runtime artifacts unless they are clearly marked `[UNVERIFIED]` or documented as open questions.
26. **Background Job Inventory Coverage**: Reject `10_background_jobs.md` when any job, scheduler, hosted service, worker, producer, or consumer discovered in `inventory/background-jobs.json` is absent by exact source name, when handler names are missing, when the document has fewer job table rows than discovered jobs, or when it uses a "required keywords" checklist instead of per-job lifecycle documentation.
27. **Background Job Sequence Detail**: Reject `10_background_jobs.md` when discovered jobs lack per-job lifecycle columns for source path, registration source, trigger/schedule/cron, producer, handler, queue/storage, service/repository calls, DB/Redis/external side effects, retry, timeout, idempotency, failure/logging/shutdown behavior, evidence, and status, or when no Mermaid `sequenceDiagram` documents scheduler/worker/handler/store/failure timing.
28. **Database Store Contract Completeness**: Reject `07_database_reference.md` when SQL tables, Mongo collections, or Redis stores are discovered but the document lacks concrete schema/key contracts. SQL tables require per-table column dictionaries. Mongo collections require document field dictionaries. Redis requires key pattern, data type, key inputs, field/member/value shape, TTL/no-expiry evidence, producer/write path, consumer/read path, jobs/APIs affected, rebuild/invalidation path, SQL/Mongo sync source, drift risk, evidence, and status.
29. **Database Keyword-Stuffing Guard**: Reject `07_database_reference.md` when it contains "Required Database Reference Keywords" or similar validation keyword checklists, or when Redis/Mongo are documented only as storage names such as `None (Redis Hash)` / `StatsNews (MongoDB)` without field/value/schema and operational data-flow detail.
30. **80 Percent Code Understanding Gate**: Reject final docs when a new developer cannot understand the main business behavior without opening source code. Important APIs, jobs, realtime events, integrations, config-driven behavior, and data-store flows must include entry point, actor/client, trigger, input/source data, processing logic, internal call chain, external/downstream calls, DB/Redis/Mongo/queue/realtime side effects, config keys, success/error behavior, debug/smoke check, evidence, and status.
31. **Cross-Document Flow Consistency**: Reject if `06_architecture.md`, `09_api_catalog.md`, `10_background_jobs.md`, `11_realtime_signalr_socket.md`, `12_external_integrations.md`, and `14_operations_runbook.md` do not agree on the same route/job/event/integration -> service -> repository/client -> store/external flow, or if one doc documents a side effect that another relevant doc omits without an explicit unresolved gap.
32. **No Validator Text In Final Docs**: Reject any final user-facing doc containing phrases like "Required ... Keywords", "Keywords checklist", or machine-facing validation text. Final docs must explain repository behavior, not how to satisfy validators.
33. **Data Mutation Lineage Gate**: Reject when final docs do not let a reader trace exact data mutations from entry point to storage. For every important SQL table, Mongo collection, Redis key family, queue, and realtime event, docs must identify operation, API/job/service entry point, ID/key source, field/value changed, value source, call chain, secondary side effects, read consumers, consistency rule, debug query/command, evidence, and status.
34. **Per-Route API Contract Gate**: Reject `09_api_catalog.md` when `Complete Discovered Routes and Actions` covers more routes than `API Contract Matrix`, endpoint request/response details, or `Behavior Flow Table`. Every route in `inventory/routes.json` must have endpoint-level request fields, request example, response fields, success example, error example, status codes, validation, auth/header, side effects, behavior flow, evidence, and status, or an explicit unresolved/excluded row with evidence.
35. **Synthetic API Data Guard**: Reject API docs containing generated placeholder/sequential values such as `X-Secret-Key-1`, `ValidationRulesV1`, `Error 1`, `Request Body 1 data`, `appsettings.json (1)`, `news_ids_1`, `TotalView_1`, `Redis Cache 1`, `5050ms`, or `105/min`, and reject `[CONFIRMED]` API evidence rows that cite only a solution/project file such as `*.sln line 1`.

## Final Documentation Language Validation
`language-validation.md` MUST report PASS/FAIL for:
- Required Vietnamese headings in every final document.
- Vietnamese prose presence outside code blocks.
- No copied English intermediate headings in final docs.
- English intermediate artifact headings remain English.
- No translated technical identifiers, Evidence IDs, paths, routes, config keys, JSON keys, database names, commands, or code blocks.

Reject with `REJECT_REQUIRES_REVISION` if final prose is mostly English, final docs include internal instructions, final docs copy English findings without Vietnamese synthesis, or technical identifiers were translated/altered.

## Required Review Matrix
`final-quality-report.md` MUST include the quick review table from `.ai/rules/08-source-code-handover-quality-checklist.md` with one row per final document.

## Required Output
`final-verdict.md` MUST be a structured verdict report, not a one-line token.

Minimum required lines:

```text
Verdict: PASS | REJECT_REQUIRES_REVISION | BLOCKED
Run ID: <run_id>
Source Commit: <source_commit>
Validator Agent: agent-10
Status Gate: PASS | FAIL
Quality Gate: PASS | FAIL
Evidence Gate: PASS | FAIL
Language Gate: PASS | FAIL
Publish Gate: PASS | FAIL
```

Agent 10 MUST NOT write `Verdict: PASS` unless:

- `.ai/scripts/validate-source-code-handover-status.py <run_dir>` passes.
- `.ai/scripts/validate-source-code-handover-evidence-store.py <run_dir>/evidence` passes.
- `.ai/scripts/validate-source-code-handover-physical-evidence.py <run_dir> <repo_root>` passes.
- `.ai/scripts/validate-source-code-handover-quality.py <run_dir>/final` passes.
- `.ai/scripts/validate-source-code-handover-language.sh <run_id>` passes.
- Final docs have no repeated prose padding, no dominant long prose lines, and no generic repeated paragraph used to satisfy word-count thresholds.
- `final-quality-report.md` contains the Quick Review Table with one row per required final document and a non-PASS reason for every rejected or partial document.
- API integration, external integration, operations/debug, and database-operation completeness checks pass or are explicitly marked `Partial`, `Not Verified`, `[UNVERIFIED]`, `[BLOCKED]`, or `[NOT_APPLICABLE]` with negative evidence.

A bare `PASS`, `REJECT_REQUIRES_REVISION`, or `BLOCKED` line is invalid and MUST be rejected by the publish validator.
