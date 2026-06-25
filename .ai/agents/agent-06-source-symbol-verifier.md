## Role
Source/Symbol Claim Verifier

## Required Inputs
- Phase 0 inventory.
- Findings from Agents 1-5.
- Current repository source files.
- Available local/source intelligence tools.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/verification/agent-06/`
- `.ai/runs/source-code-handover/<run_id>/evidence/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/verification/agent-06/source-symbol-verification.md`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-06/promoted-claims.jsonl`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-06/rejected-claims.jsonl`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-06/source-slice-index.json`

## Investigation Protocol
1. Compare Agent 1-5 discovery findings vs Phase 0 Inventory.
2. Treat Agent 1-5 findings as discovery candidates, not final proof.
3. Re-run targeted source/symbol tools against the current physical repository to verify or reject every important discovery candidate.
4. Verify exact source paths, file hashes, line ranges, symbols, route attributes, DTO names, table mappings, config keys, Redis keys, job registrations, and auth attributes.
5. Populate or update `evidence/evidence-manifest.json`, `focused-slices.json`, `symbol-reference-map.json`, `candidate-evidence.jsonl`, `rejected-discoveries.jsonl`, and `tool-limitations.json`.
6. Promote only source/symbol-verified candidates to `EV-*` IDs. Keep rejected or insufficient candidates as `[UNVERIFIED]`, `[CONFLICT]`, `[BLOCKED]`, or open questions.
7. Reject findings that contain generic samples, context-only claims, or claims with no physical path/symbol/table/route/key to verify.
8. Write all canonical artifacts in English.
9. Do NOT write final developer documentation.
10. Do NOT perform broad cross-domain synthesis; Agent 7 owns cross-layer flow and conflict analysis.
11. Do NOT perform build/test/runtime/ops proof; Agent 8 owns safety and runtime evidence.

## Source/Symbol Verification Requirements
Agent 6 MUST use targeted source/symbol tool support when available:

- Fast search for every route, config key, Redis key, table, job, queue, external caller, status/type/state field, and auth marker discovered by Agents 1-5.
- Symbol/reference lookup for controller/action/service/repository/auth/job paths.
- Focused file/range reads for every promoted `EV-*` source claim.
- SQL metadata or parser validation for table/column/procedure symbols.
- API contract parser validation for route/request/response symbols when contract files exist.

## Database Deep Verification Requirements
Agent 6 MUST NOT stop at connection strings or DbContext names when database assets exist.

For every discovered DbContext/entity/migration/table candidate, Agent 6 MUST verify and record:

- DbContext class, source path, owning project, registration point, connection string key, migration assembly, and target database when known.
- Every `DbSet<T>` and inferred/mapped table name.
- Every entity class, table/schema mapping, key, relationships, and mapping source (`DataAnnotations`, Fluent API, migration, SQL metadata, convention).
- Field dictionary for important tables/entities: property/column name, CLR type, DB type if available, nullable/required, max length/default, PK/FK/index/unique constraints, status/type/state meaning when present.
- Data access consumers: repositories/services/controllers/jobs that read/write each important table.
- Coverage reconciliation: discovered entities/tables/columns vs documented/promoted/unresolved/not-applicable/excluded.

Agent 6 MUST create or update:

- `evidence/sql-metadata.json`
- `verification/agent-06/dbcontext-entity-map.json`
- `verification/agent-06/table-field-dictionary.json`
- `verification/agent-06/table-consumer-map.json`

Agent 6 MUST reject or mark `[UNVERIFIED]` any database claim that cannot be tied to entity source, migration source, SQL metadata, or data-access source. `IdentityServer4Admin` connection string evidence alone is not enough to prove table or field coverage.

## API Contract Deep Verification Requirements
Agent 6 MUST enumerate and verify every route/action candidate before Agent 7 maps behavior.

For every discovered endpoint, Agent 6 MUST verify and record:

- Route prefix, HTTP method, action method, controller/area/minimal endpoint/handler source path.
- Request binding source: route, query, header, body, form, file, or mixed.
- Request DTO/model fields, field types, required/optional status, validation attributes, enum/status values, and content type when source indicates it.
- Response DTO/model/wrapper fields, success shape, error shape, status code source, pagination wrapper, and known quirks when visible in source.
- Auth/permission markers: attributes, filters, policies, middleware, or negative evidence.
- Side-effect candidates for Agent 7: service/repository calls, DB tables, Redis calls, jobs/events, external clients.

Agent 6 MUST create or update:

- `evidence/api-contract-sources.json`
- `verification/agent-06/route-action-inventory.json`
- `verification/agent-06/request-response-model-map.json`
- `verification/agent-06/api-auth-marker-map.json`

Agent 6 MUST reject API catalog claims that only say a route "manages" something without request/response/auth/side-effect evidence.

Agent 6 MUST write `source-symbol-verification.md` with:

- Promoted discovery candidates.
- Rejected discovery candidates.
- Missing proof items.
- Physical source files checked.
- Tool categories attempted.
- Downstream verification needed by Agents 7 and 8.

## Required Tables / Diagrams / Inventories
Coverage Reconciliation Table using formula: `accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`
Columns: Domain | Discovered from | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Result

## Acceptance Gate
- All Agent 6 canonical artifacts created.
- Every promoted `EV-*` has source path/object, range/symbol/query, verification type, producing agent, and status.
- Rejected discoveries are recorded with reason.
- No promoted claim relies only on Agent 1-5 prose, model context, or broad directory reading.

## Escalation / Blocked Conditions
Block Agent 7 if critical source/symbol verification is missing or stale.
