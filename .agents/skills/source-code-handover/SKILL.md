---
name: source-code-handover
description: Use when creating source-code handover documentation, onboarding documentation for new developers, architecture summaries, repository maps, setup guides, API/database/auth documentation, or final project handbooks from source code
---

<!-- generated-by: ai-agent-adapter-sync -->


# Source Code Handover (Evidence-First Documentation Pipeline)

## REQUIRED BACKGROUND
Read `.ai/skills/using-superpowers/SKILL.md` before using this skill.

## Language Policy

### AI Execution Language

All instructions intended for AI agents, coordinators, reviewers, validators, workflows, rules, schemas, artifact contracts, validation reports, and script output messages MUST be written in English.

This includes:
- Skill instructions.
- Workflow phases.
- Agent prompts.
- Rules and quality gates.
- Artifact schemas.
- YAML front matter field names.
- Validation scripts.
- Status labels.
- Error messages.
- Review checklists.
- Coverage reports.
- Provenance scan reports.
- Negative-evidence reports.

Intermediate findings, reviews, inventories, `STATUS.md`, validation reports, and all canonical machine-readable artifacts are English. English intermediate artifacts are not a substitute for Vietnamese final docs.

### Final Documentation Language

All final documentation generated in `.ai/runs/source-code-handover/<run_id>/final/` and published to `docs/` for project developers MUST be written in Vietnamese.

This includes:
- Markdown headings.
- Explanations.
- Tables.
- Diagram labels where natural language is used.
- Risks.
- Open questions.
- Limitations.
- Runbooks.
- Troubleshooting guidance.
- Operational procedures.

The following items MUST remain unchanged and may remain in English:
- Source paths.
- File names.
- Class names.
- Method names.
- Namespace names.
- API routes.
- HTTP methods.
- Configuration keys.
- Environment variable names.
- JSON property names.
- Database table and column names.
- Evidence IDs.
- Commands.
- Code blocks.
- Stack traces.
- Framework/library names.
- Mermaid syntax keywords.

Agent 7 is responsible for Vietnamese final-document generation. Agent 8 validates both content quality and language compliance.

## TOOL ORCHESTRATION POLICY

### Purpose

This skill MUST NOT rely on loading the full repository into model context. The workflow must use indexing, search, semantic analysis, database metadata extraction, runtime artifacts, and evidence manifests to retrieve only the smallest relevant source slice required for each documentation claim.

The required evidence flow is:

```text
Question
-> Search/index query
-> Retrieve focused evidence
-> Trace symbols/calls/data access
-> Validate with an independent artifact
-> Write documentation with evidence
-> Update coverage and gaps
```

Repository-wide source reading is allowed only for deterministic inventory generation. Do not begin analysis by reading entire directories such as `Controllers/`, `Services/`, `Repositories/`, or `Infrastructure/`. Locate the exact route, symbol, method, table, key, job, or configuration key first.

### Tool Priority Order

Agents MUST use tools in this order and record each attempt in the evidence store:

1. Repository manifest and Phase 0 inventory files.
2. Fast text search.
3. Symbol and reference lookup.
4. Semantic/call-graph analysis.
5. SQL metadata and query mapping.
6. Redis/job/integration mapping.
7. Test/Postman/Swagger/runtime artifacts.
8. Git history when legacy behavior is unclear.
9. Manual source reading of only the relevant files and ranges.

### Mandatory Local Tool Categories

These tool categories MUST be attempted when applicable to the repository. If a tool is unavailable or not applicable, record it in `tool-limitations.json` with status `tool_unavailable`, `not_applicable`, or `blocked`.

| Tool category | Preferred tools | Required use |
|---|---|---|
| Fast text search | `rg`, `git grep`, Sourcegraph code search when available | Routes, config keys, Redis keys, table names, stored procedures, jobs, auth attributes, exception types, compatibility branches, feature flags |
| Build/compile context | `dotnet build` for .NET projects | Validate project graph, target frameworks, references, compile context |
| Symbol navigation | Roslyn, LSP, SCIP, Sourcegraph code intelligence, IDE symbol index | Go to definition, find references, implementations, callers, service/repository consumers |
| Semantic analysis | CodeQL, Roslyn call graph extraction, custom C# AST analyzer | Controller-service-repository chains, request-to-SQL/Redis data flow, auth check locations, exception mapping, transaction and retry paths |
| Pattern scanner | Semgrep, custom regex rules, Roslyn analyzers | Legacy framework, `System.Web`, `HttpContext.Current`, OWIN, raw SQL, Redis, Hangfire/Quartz, external clients, silent catches, auth bypass, status/type/state patterns |
| SQL metadata | SQL Server catalog queries, DacFx/sqlpackage extraction, schema compare export, SQL parser | Tables, columns, PK/FK, indexes, views, stored procedures, functions, triggers, constraints, computed columns |
| API contract parser | Swagger/OpenAPI parser, Postman parser, integration-test extraction | Request/response models, status codes, headers, auth, content types, examples, smoke contracts |
| Runtime artifact parser | Logs, Hangfire export, Redis snapshot, API traffic sample, database query logs | Actual request/response shape, wrapper, status code, retry, job execution, TTL, datatype, fallback, external failure behavior |
| Evidence store | JSON/JSONL/CSV manifests, SQLite/DuckDB when useful | Persist tool outputs, evidence IDs, coverage, gaps, and tool limitations |

### Optional High-Value Tools

For large repositories or multi-repo systems, prefer Sourcegraph MCP, GitHub MCP Server, CodeQL, SCIP/LSP indexes, SQLite/DuckDB evidence graphs, Mermaid/PlantUML generation, and docs/version lookup tools when available and trusted. Treat community MCP wrappers as optional integrations that must be pinned and sandboxed before use.

### Required Search Patterns

Fast search MUST include repository-relevant variants of:

```text
HttpGet HttpPost HttpPut HttpDelete Route RoutePrefix MapHttpRoute
Authorize AllowAnonymous HttpContext.Current ConfigurationManager WebConfigurationManager
ConnectionStrings Redis StackExchange.Redis Hangfire Quartz BackgroundJob RecurringJob
SqlCommand SqlConnection ExecuteSqlCommand StoredProcedure TransactionScope BeginTransaction Commit Rollback
catch retry fallback callback webhook channel_id officer_id tenant_id status type kind state
```

### High-Risk Flow Rule

For high-risk flows, text search alone is insufficient. Validate the path using semantic analysis, symbol references, call graph, tests, runtime artifacts, or an equivalent independent artifact.

High-risk flows include:

- Authentication.
- Authorization.
- Payment.
- Quiz submit.
- Lucky draw.
- Data synchronization.
- Callback/webhook.
- Background jobs.
- Redis fallback.
- Database transaction.
- External API retry.

### Evidence Store Contract

Before Agent 7 writes final Markdown docs, the run MUST contain a machine-readable evidence store under:

```text
.ai/runs/source-code-handover/<run_id>/evidence/
```

Required files:

- `tool-runs.jsonl`: one record per tool command/query, including command/query, working directory, status, timestamp, output artifact path, and limitation if any.
- `evidence-manifest.json`: maps every Evidence ID to source path/range, symbol, claim, verification type, source commit, producing agent, and downstream final docs.
- `focused-slices.json`: lists exact file ranges, symbols, SQL objects, API contracts, log snippets, or runtime artifacts admitted into model context.
- `symbol-reference-map.json`: records definitions, references, implementations, callers, and call-chain edges used for claims.
- `data-flow-map.json`: records request-to-service-to-repository-to-SQL/Redis/job/external flow evidence for high-risk paths.
- `sql-metadata.json`: records SQL schema metadata or a clear `not_applicable` / `tool_unavailable` limitation.
- `api-contract-sources.json`: records Swagger, Postman, test, or traffic sources used for API contract evidence.
- `runtime-artifacts.json`: records logs, Hangfire, Redis, traffic, database query logs, or a clear limitation.
- `tool-limitations.json`: records unavailable tools, failed commands, inaccessible systems, and readiness impact.

Agent 6 MUST review the evidence store before Agent 7 starts. Agent 8 MUST reject final docs if important claims bypass the evidence store or if high-risk flows lack independent validation.

## Required Rules
- `.ai/rules/00-global-rules.md`
- `.ai/rules/01-documentation-skill.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/07-handover-documentation-dod.md`
- `.ai/rules/08-source-code-handover-quality-checklist.md`

## Required Templates
- Agent 1-5 findings MUST use `.ai/templates/source-code-handover/agent-findings-template.md`.
- Agent 7 final documents MUST use `.ai/templates/source-code-handover/final-document-template.md`.
- Evidence store files SHOULD follow `.ai/templates/source-code-handover/evidence-store-template.md`.
- Templates define the stable shape for every project. Agents may add project-specific sections only after all required template sections and checklist-specific tables are complete.
- Do not copy placeholder values from templates into final outputs.

## Execution Isolation Policy & Fallbacks
Isolation is MANDATORY. Valid modes:
1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

Forbidden Legacy Modes: `single-runtime-sequential-fallback`, `single-session-multi-role-execution`, `memory-only-agent-handoff`, `implicit-agent-output`, `direct-final-handbook-without-artifacts`

If runner lacks isolation capability, STOP before Agent 1, log `blocked-no-isolation-capability` in `STATUS.md`, generate block report, DO NOT run Agent 7, DO NOT publish.

## Artifact-First Handoff Policy & Coordinator Restrictions
- Physical files on disk are the ONLY official handoff mechanism. 
- Coordinator CANNOT bypass Agents 1-6 to generate docs directly.
- `draft-docs/` shared path is NEVER the source of truth. Canonical artifacts are ONLY in `.ai/runs/source-code-handover/<run_id>/...`

## Disk Validation Gate
- Next agent must not start until previous agent artifact passes.
- Artifact must have YAML front matter (`run_id`, `source_commit`, `created_at`, `status`).
- Final documents must satisfy the front matter, common sections, evidence, negative-evidence, forbidden-content, and document-specific requirements in `.ai/rules/08-source-code-handover-quality-checklist.md`.

## Current Repository Provenance & Template Guard
- Final docs ONLY describe the currently checked-out repository.
- NO generic framework knowledge, template docs, upstream READMEs, generic passwords (Password123), or sample domains (example.com).
- Upstream references must be isolated in `docs/02_project_context.md` with `[UPSTREAM_REFERENCE]`.

## Evidence & Negative Evidence Policy
- Valid Labels: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, `[DECISION]`
- Use `[DECISION]` for behavior-preservation, migration compatibility, rollback, or intentional behavior-change decisions. Include owner or required owner confirmation.
- `[NOT_APPLICABLE]` is strictly for `not_found_after_scan` and MUST include negative evidence IDs (`EV-NEG-###`).

## Secret Safety
Secret scan MUST be executed and passed. No unredacted secrets or credential-like literals are permitted.

## Pipeline Phases
Phase 0: Preflight + Deterministic Discovery (create JSON inventories).
Phase 1: Agent 1–5 Domain Analysis (match findings against Phase 0 inventory).
Phase 2: Agent 6 Evidence/Coverage/Conflict Review.
Phase 3: Agent 7 Final Documentation Assembly.
Phase 4: Agent 8 Independent Quality Validation.
Phase 5: Agent 7 Revision (only if Agent 8 REJECTS).
Phase 6: Final Publish.

## Readiness Policy
- **Ready**: Execution isolation passed. Phase 0 valid. Agents 1-6 passed. Agent 7 created 20 canonical docs. Agent 8 passed. No critical conflicts. No unresolved cores. No template contamination. Secret scan passed. Coverage math passed.
- **Partial**: Isolation passed. Inventory & coverage exist. Runtime/prod limitations noted. Local dev possible. Agent 8 finds no critical failure. No `Ready` claims for unverified areas.
- **Blocked**: No isolation. No reliable inventory. Stale/missing artifacts. Coverage fails. Template contamination. Agent 8 rejects without revision. Critical evidence conflict.

## Publish Policy
Documents in `.ai/runs/.../final/` MUST NOT be copied to `docs/` until Agent 8 validation is complete and yields a `PASS` verdict.
