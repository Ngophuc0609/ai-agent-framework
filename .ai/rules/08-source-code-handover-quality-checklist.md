# Source Code Handover Quality Checklist

## Purpose

This rule is the mandatory quality checklist for the 20 final documents produced by workflow `source-code-handover`.

This file is AI-facing and written in English. Literal Vietnamese headings and snippets below are required final-document output, not internal execution language.

## Evidence Store Requirement

Before final Markdown documents are accepted, the run MUST include a machine-readable evidence store:

```text
.ai/runs/source-code-handover/<run_id>/evidence/
```

Required files:

- `tool-runs.jsonl`
- `evidence-manifest.json`
- `focused-slices.json`
- `symbol-reference-map.json`
- `data-flow-map.json`
- `sql-metadata.json`
- `api-contract-sources.json`
- `runtime-artifacts.json`
- `tool-limitations.json`

Agent 8 MUST reject final docs when important claims have no Evidence ID in `evidence-manifest.json`, when focused slices are missing for important claims, or when high-risk flows lack symbol/data-flow/independent validation while the required tools were available.

## Scope

This rule applies to every final document in:

```text
.ai/runs/source-code-handover/<run_id>/final/
```

It extends `.ai/rules/07-handover-documentation-dod.md`. If the two rules conflict, this rule is stricter for final document structure and validation.

## Required Front Matter

Every final document MUST start with YAML front matter containing:

```yaml
---
document_id: "DOC-01"
title: "Document title"
run_id: "<run_id>"
source_commit: "<git_sha>"
source_branch: "<branch>"
status: "Ready | Partial | Blocked | Not Applicable"
primary_owner_agent: "agent-xx"
evidence_ids:
  - "EV-XXX-001"
last_verified_at: "<ISO-8601 timestamp>"
---
```

Allowed `status` values are exactly: `Ready`, `Partial`, `Blocked`, `Not Applicable`.

## Required Common Sections

Every final document MUST include these sections:

- `## Phạm vi`
- `## Trạng thái`
- `## Nguồn dữ liệu / Evidence`
- `## Nội dung chính`
- `## Hạn chế`
- `## Câu hỏi mở`
- `## Rủi ro`

If there are no open questions or no document-specific risks, write:

```md
## Câu hỏi mở
Không có.

## Rủi ro
Không có rủi ro riêng ngoài các mục đã ghi trong `17_known_risks.md`.
```

## Claim Status Labels

Important technical claims MUST use one of:

- `[CONFIRMED]`
- `[INFERRED]`
- `[UNVERIFIED]`
- `[CONFLICT]`
- `[NOT_APPLICABLE]`
- `[BLOCKED]`
- `[UPSTREAM_REFERENCE]`
- `[DECISION]`

`[CONFIRMED]` claims require Evidence IDs listed in `19_evidence_index.md`.
Every assumption MUST be labeled `[UNVERIFIED]`. Every conflict MUST be labeled `[CONFLICT]`. Every documented behavior-preservation or migration behavior choice MUST be labeled `[DECISION]` and include a decision owner or required owner confirmation.

## Evidence IDs

Every Evidence ID used in any final document MUST appear in `19_evidence_index.md`.

Allowed patterns:

- `EV-REPO-###`
- `EV-CONFIG-###`
- `EV-DB-###`
- `EV-MIGRATION-###`
- `EV-AUTH-###`
- `EV-API-###`
- `EV-JOB-###`
- `EV-RT-###`
- `EV-OPS-###`
- `EV-CICD-###`
- `EV-TEST-###`
- `EV-NEG-###`
- Domain-expanded negative IDs such as `EV-NEG-RT-###` are allowed only when they are indexed in `19_evidence_index.md`.

Evidence MUST include source path, class/method or line range, verification type, and source commit. A class name alone is not evidence.

## Documentation Capability Requirements

The final documentation set MUST allow a new developer, tech lead, BA, or AI agent with no prior project knowledge to answer these questions accurately:

- What does the system do?
- Who uses it?
- Which API supports which business capability?
- Where is each important value read from and written to?
- Which business rules must be preserved?
- How do Redis/cache, background jobs, queues, and external APIs work?
- Where are authentication and authorization checked?
- Which behavior must not change during migration or modernization?
- How can old and new behavior be proven equivalent?
- How can a module be rolled back when production fails?

Do not write generic summaries. Reject vague statements such as:

```md
Module Accounts quản lý tài khoản.
```

Require evidence-backed, behavior-level documentation such as:

```md
[CONFIRMED] Module `Accounts` quản lý tài khoản theo phạm vi `channel_id`. API tạo tài khoản resolve `channel_id` từ request; nếu request không có giá trị thì fallback về authenticated context. `username` phải unique trong phạm vi `channel_id`. Khi tạo thành công, hệ thống insert bảng `Accounts`, ghi audit log và invalidate Redis key `account:*`.

Evidence:
- EV-API-021
- EV-DB-044
- EV-OPS-009
```

## Required System Overview Content

`01_project_handover_full.md`, `02_project_context.md`, and `06_architecture.md` MUST collectively document:

- System purpose.
- User/client groups.
- Main domain/module list.
- External integrated systems.
- Databases.
- Cache/Redis behavior.
- Background jobs.
- Queues or negative evidence that no queue was found.
- Client applications.
- Runtime environments.
- Main operational and migration risks.
- Actors and external systems.

The overview MUST include a system flow diagram, using exact current-source components where found:

```text
User / Client
→ API Gateway hoặc Web Server
→ Legacy .NET Framework Application hoặc current backend host
→ SQL Server
→ Redis
→ Hangfire/Background Job
→ External API
→ SMTP/Storage/Queue
```

If a component is not present, mark it `[NOT_APPLICABLE]` with negative evidence. Do not invent it.

## Required Module Inventory

The final docs MUST include a module inventory table with at least these columns:

```md
| Module | Chức năng | API | Tables | Redis | Jobs | Risk | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
```

Example shape:

```md
| Authentication | Xác thực/token | `/oauth/token` | `Tokens`, `Accounts` | token cache | cleanup | High | EV-AUTH-001, EV-DB-004 | [CONFIRMED] |
| Accounts | Quản lý tài khoản | `/accounts` | `Accounts` | account cache | none | Medium | EV-API-002, EV-DB-010 | [CONFIRMED] |
| Quiz Games | Quản lý game | `/quiz-games` | `QuizGames` | game cache | publish | Medium | EV-API-003, EV-JOB-002 | [CONFIRMED] |
| Quiz Submit | Nộp bài | `/quiz-submit` | `QuizResponses` | ranking cache | callback | High | EV-API-004, EV-OPS-003 | [CONFIRMED] |
```

## Required Project Inventory

Every project in the solution/repository MUST be documented with:

- Project name.
- Project path.
- Project type.
- Target framework.
- Startup point.
- Main responsibility.
- Dependencies.
- Database access.
- Redis access.
- External integration.
- Migration difficulty.
- Risk.
- Owner.
- Status.

Use this table shape:

```md
| Project name | Project path | Project type | Target framework | Startup point | Main responsibility | Dependencies | Database access | Redis access | External integration | Migration difficulty | Risk | Owner | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

## Required Actors And External Systems

Document actors such as `Admin`, `Editor`, end user, mobile app, web frontend, third-party auth, payment service, email service, news service, storage service, and analytics service only when found or inferred with evidence.

Every external system MUST have:

- Name.
- Purpose.
- Protocol.
- Auth method.
- Direction.
- Criticality.
- Fallback.
- Owner.
- Evidence.
- Status.

Use this table shape:

```md
| External system | Purpose | Protocol | Auth method | Direction | Criticality | Fallback | Owner | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
```

## Required Dependency Compatibility Inventory

The final docs MUST list NuGet packages, internal DLLs, COM dependencies, Windows dependencies, and other runtime dependencies discovered from source/config.

Use this table shape:

```md
| Dependency | Current Version | Used By | Purpose | .NET 8 Compatibility | Replacement | Risk | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
```

Compatibility classification MUST be one of:

- `Compatible directly`
- `Compatible with upgrade`
- `Needs adapter`
- `Needs replacement`
- `Needs rewrite`
- `Unknown / POC required`

## Required Configuration Mapping

The final docs MUST map all discovered:

- `Web.config`
- `App.config`
- Connection strings.
- AppSettings.
- Environment variables.
- Secrets, redacted.
- Certificates.
- File paths.
- IIS settings.
- Scheduled jobs config.
- Feature flags.

Use this table shape:

```md
| Key | Purpose | Environment | Required/Optional | Secret/Non-secret | Legacy location | .NET 8 target location | Consumer module | Risk if missing | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|
```

Secret values MUST be redacted. Preserve key names.

## Required Architecture Content

`06_architecture.md` MUST document:

- Application layers.
- Dependency direction.
- Entry points.
- Controller/service/repository flow.
- Configuration flow.
- Authentication flow.
- Authorization flow.
- Exception flow.
- Logging flow.
- Background job flow.
- Data flow.

C4 diagrams are mandatory:

- C1 System Context.
- C2 Container Diagram.
- C3 Component Diagram for each high-risk module when present.

C3 is required for high-risk modules such as Authentication, Authorization, Quiz Submit, Payment, Lucky Draw, Background Job, Redis-heavy modules, or external integration modules. Do not draw C3 for every class.

Legacy or current request lifecycle MUST identify where validation, auth, exception mapping, response wrapping, and audit logging happen:

```text
HTTP Request
→ IIS or current web host
→ Global.asax / Program.cs / Startup.cs
→ OWIN middleware or ASP.NET Core middleware
→ Authentication
→ Authorization
→ Filter
→ Controller
→ Service
→ Repository
→ SQL / Redis / Job / External API
→ Exception handler
→ HTTP Response
```

If the stack is not legacy .NET Framework, adapt the labels to current source and mark missing legacy components `[NOT_APPLICABLE]` with negative evidence.

## Required Domain And Business Rules

Final docs MUST describe business entities, not only database entities. Examples include `Account`, `Channel`, `Quiz Game`, `Quiz Question`, `Question Option`, `Quiz Response`, `Gift`, `Challenge`, `Template`, `Role`, and `Permission` when present.

Each business entity MUST document:

- Business meaning.
- Identifier.
- Lifecycle.
- Status/state.
- Relationships.
- Important rules.
- Related APIs.
- Related tables.
- Evidence.
- Status.

Every important business rule MUST use this structure:

```md
### Rule ID: BR-<DOMAIN>-###

#### Name
<Vietnamese rule name.>

#### Scope
<Module or entity scope.>

#### Trigger
<API route, job, event, UI action, or scheduler.>

#### Preconditions
- <Condition with evidence.>

#### Processing
1. <Step.>
2. <Step.>

#### Output
- HTTP response.
- Database record.
- Redis mutation.
- Audit log.

#### Failure Rules
- <Failure case.>

#### Compatibility Rule
Behavior phải giữ nguyên khi migrate sang .NET 8, unless a `[DECISION]` says otherwise.

#### Evidence
- Source path.
- Class.
- Method.
- Related SQL/Redis key.
```

Business entities with fields named `status`, `type`, `kind`, or `state` MUST include a state transition table:

```md
| From state | To state | Allowed/Forbidden | Actor allowed | Validation condition | Side effect | Database update | Cache invalidation | Job/event trigger | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|
```

Do not write only `status = 1 là active`. Explain behavior:

```md
[CONFIRMED] `status = 1` nghĩa là Active. Chỉ `Admin` hoặc `Owner` có thể chuyển từ Draft sang Active. Khi Active, game được phép public access. Khi Closed, không được tạo `QuizResponse` mới.
```

## Required Compatibility Quirks

Document behaviors that are unusual but must be preserved, including:

- Client sends `form-urlencoded` instead of JSON.
- Field name contains a typo but clients depend on it.
- API returns HTTP 200 for some business errors.
- `channel_id` fallback from claim/authenticated context.
- `answer_id` contains multiple comma-separated IDs.
- Endpoint uses `officer_id` while database stores `channel_id`.
- Redis value is a plain string instead of JSON.

Each quirk MUST include:

- Description.
- Known reason, or `[UNVERIFIED]` if unknown.
- Affected client/dependency.
- Whether it must be preserved.
- Retirement plan after migration.
- Decision owner.
- Evidence.
- Status.

Use this table shape:

```md
| Quirk ID | Description | Known reason | Affected client/dependency | Preserve? | Retirement plan | Decision owner | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
```

## Required API Contract Detail

Every endpoint MUST document:

- Route.
- HTTP method.
- Module.
- Authentication.
- Required permission.
- Request content type.
- Headers.
- Query parameters.
- Request model.
- Validation rules.
- Response model.
- Success response.
- Error response.
- Status codes.
- Database side effects.
- Redis side effects.
- Jobs/events.
- External API calls.
- Idempotency.
- Rate limit.
- Known quirks.
- Evidence.
- Status.

Use this table shape:

```md
| API ID | Route | Method | Module | Auth | Permission | Content type | Headers | Query | Request model | Validation | Response model | Success | Error | Status codes | DB side effects | Redis side effects | Jobs/events | External calls | Idempotency | Rate limit | Known quirks | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

## Required Migration Safety Content

The final docs MUST answer:

- If migrated to .NET 8, what must not change?
- How can the new system prove it behaves like the old system?
- What baseline tests, smoke tests, contract tests, or data comparisons are required before migration?
- How can a new module be rolled back if production fails?

Use this table shape:

```md
| Behavior / Module | Must not change | Baseline proof | .NET 8 target risk | Rollback plan | Owner | Evidence | Status |
|---|---|---|---|---|---|---|---|
```

## Final Documentation Acceptance Questions

Agent 8 MUST reject the documentation unless the final set can answer these checks with evidence or explicit `[NOT_APPLICABLE]` negative evidence:

- Dev mới có thể chạy hệ thống local từ tài liệu không?
- AI có thể xác định entry point và request lifecycle không?
- Có biết mọi API thuộc module nào không?
- Có biết request, response, status code và error contract không?
- Có biết business rule nằm ở đâu không?
- Có biết table/column/status field có ý nghĩa gì không?
- Có biết Redis key nào được đọc/ghi/xóa không?
- Có biết job nào được tạo và retry ra sao không?
- Có biết external API nào được gọi không?
- Có biết quyền được kiểm tra ở đâu không?
- Có test baseline trước migration không?
- Có thể chứng minh .NET 8 giữ nguyên behavior không?
- Có rollback được khi production lỗi không?
- Mọi kết luận quan trọng có evidence không?
- Có phân biệt observed, inferred, unverified, conflict và decision không?

## Not Applicable Rule

`[NOT_APPLICABLE]` is valid only with negative evidence:

- Component/scope checked.
- Source roots.
- Search patterns.
- Command/tool or CodeGraph query.
- Result count.
- Operational impact.
- Evidence ID such as `EV-NEG-###` or `EV-NEG-RT-###`.

Do not use `Not Applicable` because the agent ran out of time or lacked enough context.

## Forbidden Content

Final docs MUST NOT present these as current repository behavior without `[UPSTREAM_REFERENCE]` and evidence:

- `dotnet new` or template creation instructions, unless the repo is template tooling.
- A repository URL different from the current git remote.
- Example Docker images, domains such as `example.com`, or placeholder setup.
- Real secrets, passwords, client secrets, API keys, JWT keys, or connection strings.
- `Password123`, `Secret123`, `your-api-key`, `your-client-secret`.
- Invented APIs, hubs, jobs, test code, backup behavior, log rotation, or integrations.
- Vague alternatives such as `Hangfire or Quartz`, `Hangfire hoặc Quartz`, `Redis or some cache`, or `Redis hoặc cache nào đó`.
- Upstream Gitter, PayPal, Patreon, or template content outside a clearly labeled `[UPSTREAM_REFERENCE]` section.

## Canonical Examples For High-Quality Output

Agent 7 MUST use these examples as structure patterns when assembling final documents.
Agent 8 MUST use these examples as pass/fail calibration when validating quality.
Do not copy example values into final docs; replace every project name, path, route, command, and Evidence ID with current-repository evidence.

### Example: Good Front Matter

```yaml
---
document_id: "DOC-04"
title: "Local Setup"
run_id: "source-code-handover-20260624-153000"
source_commit: "4f2a9c1"
source_branch: "main"
status: "Partial"
primary_owner_agent: "agent-01"
evidence_ids:
  - "EV-REPO-001"
  - "EV-CONFIG-003"
last_verified_at: "2026-06-24T15:30:00+07:00"
---
```

Why this passes:

- `document_id` matches the filename number.
- Status is one of the allowed values.
- Evidence IDs are real IDs that must exist in `19_evidence_index.md`.
- The document owner maps back to the agent responsible for the evidence.

### Example: Bad Front Matter

```yaml
---
title: "Setup"
status: "Done"
evidence_ids: []
---
```

Why this fails:

- Missing `document_id`, `run_id`, `source_commit`, `source_branch`, `primary_owner_agent`, and `last_verified_at`.
- Status `Done` is not allowed.
- Empty evidence makes the document non-auditable.

### Example: Good Evidence-Backed Claim

```md
[CONFIRMED] Project API bật Swagger trong pipeline development.

Evidence:
- EV-API-014
- Source: `src/AdminApi/Startup.cs`, method `Configure`
- Verification type: Source
- Source commit: `4f2a9c1`
```

Why this passes:

- The claim is specific and testable.
- It references a source path and method, not just a class name.
- The Evidence ID must be present in `19_evidence_index.md`.

### Example: Bad Evidence Claim

```md
[CONFIRMED] Hệ thống có Swagger.

Evidence:
- Startup.cs
```

Why this fails:

- The claim is too broad.
- `Startup.cs` alone is not an Evidence ID.
- There is no source path, method/line, verification type, or source commit.

### Example: Good Not Applicable Section

```md
Status: [NOT_APPLICABLE]

Đã kiểm tra:
- Source roots đã kiểm tra: `src/`, `apps/`, `services/`
- Pattern đã tìm: `Hub<`, `MapHub`, `IHubContext`, `HubConnectionBuilder`, `.on(`, `.invoke(`
- Lệnh/công cụ: `rg -n "Hub<|MapHub|IHubContext|HubConnectionBuilder|\\.on\\(|\\.invoke\\(" src apps services`
- Kết quả: 0 hub registration, 0 runtime hub class, 0 production realtime client usage.

Tác động:
- Không cần runbook SignalR cho source commit hiện tại.

Evidence:
- EV-NEG-RT-001
```

Why this passes:

- It documents what was searched, where, by which tool, and what the negative result means.
- The negative evidence is traceable through an Evidence ID.

### Example: Bad Not Applicable Section

```md
[NOT_APPLICABLE] Không thấy SignalR.
```

Why this fails:

- No source roots.
- No search patterns.
- No command/tool.
- No result count.
- No operational impact.
- No negative Evidence ID.

### Example: Good Local Setup Command

````md
### Terminal 2 - Admin API

**Thư mục chạy lệnh**

```bash
cd src/AdminApi
```

**Điều kiện trước khi chạy**

- SQL Server container from Terminal 1 is healthy.
- `appsettings.Development.json` exists with secret values supplied through user secrets or environment variables.

**Lệnh**

```bash
dotnet run --project AdminApi.csproj --launch-profile Development
```

**Kết quả kỳ vọng**

- Service lắng nghe tại `https://localhost:7043`.
- Swagger trả HTTP 200 tại `https://localhost:7043/swagger`.
- Health endpoint trả HTTP 200 tại `https://localhost:7043/health`.

**Evidence**

- EV-REPO-004
- EV-CONFIG-007
````

Why this passes:

- It has working directory, prerequisites, exact command, expected runtime result, and Evidence IDs.
- It avoids generic `dotnet run` without context.

### Example: Bad Local Setup Command

````md
Chạy API:

```bash
dotnet run
```
````

Why this fails:

- No working directory.
- No project/profile.
- No prerequisite.
- No expected port/URL/health check.
- No evidence.

### Example: Good API Endpoint Card

```md
### API-USER-001 - Tạo user

| Trường | Nội dung |
|---|---|
| HTTP method | `POST` |
| Full route | `/api/users` |
| Controller/action | `UsersController.Create` |
| Auth scheme/policy | Bearer, policy `UserWrite` |
| Request DTO | `src/AdminApi/Contracts/CreateUserRequest.cs` |
| Response DTO | `src/AdminApi/Contracts/UserResponse.cs` |
| Success codes | `201` |
| Error codes | `400`, `401`, `403`, `409` |
| Validation | Data annotations on `CreateUserRequest` |
| Side effects | Inserts `Users` row |
| Evidence | EV-API-021, EV-AUTH-010, EV-DB-044 |
| Status | [CONFIRMED] |
```

Why this passes:

- It identifies the exact route, controller/action, DTOs, auth, validation, status codes, side effects, and evidence.

### Example: Bad API Endpoint Card

```md
POST /api/users creates a user.
```

Why this fails:

- Missing auth, DTO, validation, response/error contract, side effects, and evidence.

### Example: Good Risk Entry

```md
| Risk ID | Severity | Status | Evidence | Impact | Exploit/failure precondition | Owner | Remediation | Target/next step |
|---|---|---|---|---|---|---|---|---|
| RISK-AUTH-001 | High | [CONFIRMED] | EV-AUTH-018 | Access token bị lộ vẫn còn hiệu lực trong 24h. | Token bị lộ và không có kiểm tra thu hồi token. | Security/API owner | Giảm thời hạn token hoặc bổ sung revocation validation. | Xác nhận chính sách token production với maintainer. |
```

Why this passes:

- It is actionable and tied to impact, precondition, owner, remediation, and evidence.

### Example: Bad Risk Entry

```md
- Cần cải thiện bảo mật.
```

Why this fails:

- Generic.
- No evidence, severity, owner, or action.

### Example: Good Open Question

```md
| Question ID | Câu hỏi | Tại sao quan trọng | Evidence đã tìm | Suggested owner | Blocking level | Status | Next action |
|---|---|---|---|---|---|---|---|
| Q-OPS-001 | Repo chưa ghi rõ thời gian lưu log production. | Điều tra sự cố phụ thuộc vào log còn được lưu. | EV-OPS-012, EV-CICD-003 | DevOps owner | Medium | Open | Hỏi maintainer về nền tảng logging và chính sách retention. |
```

Why this passes:

- It comes from a concrete evidence gap and has an owner, impact, blocking level, and next action.

### Example: Bad Open Question

```md
- Production vận hành như thế nào?
```

Why this fails:

- Too broad and not tied to a specific evidence gap.

### Example: Good Coverage Row

```md
| Domain | Discovery source | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Status | Gaps |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| API actions/routes | `inventory/routes.json` | 42 | 39 | 3 | 0 | 0 | 42 | Partial | `18_open_questions.md#q-api-003` |
```

Why this passes:

- `Accounted = Documented + Unresolved + N/A + Excluded`.
- The denominator comes from Phase 0 inventory.
- Gaps link to the open question or risk register.

### Example: Bad Coverage Row

```md
| API | Many | Most | Good |
```

Why this fails:

- No denominator, no formula, no inventory source, no gap link.

## Required Final Documents

The final directory MUST contain exactly these files:

1. `01_project_handover_full.md`
2. `02_project_context.md`
3. `03_repository_guide.md`
4. `04_local_setup.md`
5. `05_configuration_reference.md`
6. `06_architecture.md`
7. `07_database_reference.md`
8. `08_auth_and_security.md`
9. `09_api_catalog.md`
10. `10_background_jobs.md`
11. `11_realtime_signalr_socket.md`
12. `12_external_integrations.md`
13. `13_frontend_guide.md`
14. `14_operations_runbook.md`
15. `15_deployment_and_cicd.md`
16. `16_testing_guide.md`
17. `17_known_risks.md`
18. `18_open_questions.md`
19. `19_evidence_index.md`
20. `20_documentation_coverage.md`

## Document-Specific Minimums

- `01_project_handover_full.md`: real project name, git remote, branch, commit, purpose, modules, runtime topology summary, readiness, coverage summary, Critical/High risk summary, high-impact open questions, links to the other 19 docs, and a quick-start pointer to `04_local_setup.md`.
- `02_project_context.md`: business problem, roles, boundaries, external dependencies, glossary, upstream/template origin, custom vs upstream areas, and known legacy/technical debt.
- `03_repository_guide.md`: every executable project, module type, entry point, dependency graph, common change points, generated folders to avoid, and source-path evidence.
- `04_local_setup.md`: verified or `[UNVERIFIED]` OS/tool versions, required software, config/secret provisioning, database/migration/seed steps, certificate/hosts setup when present, startup order, exact commands with working directory/prerequisites/expected result, URLs/ports, smoke checks, reset steps, and troubleshooting.
- `05_configuration_reference.md`: config matrix for keys, project, local/production required flags, secret flag, source/precedence, description, evidence, and status.
- `06_architecture.md`: component topology, runtime topology, request/data/auth flows, database/integration/cache/realtime/job boundaries when present, evidence-backed patterns, and diagrams only when source evidence supports them.
- `07_database_reference.md`: database topology, discovery coverage, entity/table inventory, field dictionary for important tables, ERD when relationships exist, migration/seed runbook, and accounted coverage.
- `08_auth_and_security.md`: schemes, cookies, JWT/OIDC/OAuth behavior when present, credential sources without secrets, token and account lifecycle, claim/client/scope inventories, role-policy-endpoint map, anonymous endpoints, CORS/CSRF/rate-limit evidence, and auth risks.
- `09_api_catalog.md`: API discovery coverage, endpoint cards, parameter tables, error contracts from real middleware/filters, evidence-backed samples, and smoke tests for important APIs.
- `10_background_jobs.md`: scans for hosted services, background services, Hangfire, Quartz, timers, channels/queues, cron/retry workers, scripts, and includes job cards for every discovered job.
- `11_realtime_signalr_socket.md`: scans hub/server/client patterns, routes, auth, transport, events, payloads, reconnect behavior, scale-out/backplane, user/group mapping, and smoke test information, or negative evidence when absent.
- `12_external_integrations.md`: integration cards with caller, trigger, protocol, auth without secrets, contract or unresolved marker, timeout/retry/failure behavior, config keys, test strategy, owner when known, evidence, and status.
- `13_frontend_guide.md`: UI apps, route/page inventory, view/component mapping, assets, JS/CSS entry points, build flow, lockfiles, localization, auth flow, API call pattern, theme, debug steps, and common build errors.
- `14_operations_runbook.md`: runtime topology, service map, reverse proxy routing, domain/port map, volumes/networks, environment source, health endpoints, logs, trace IDs, dependencies, backup/restore evidence, restart/scaling behavior, certificates, secret rotation, and incident runbooks.
- `15_deployment_and_cicd.md`: pipeline files, platform, triggers, build/test/scan steps, image/artifact, registry, environment promotion, secret injection, migration policy, deployment command/manifest, approval gate, rollback, versioning, and missing CI/CD evidence when absent.
- `16_testing_guide.md`: all test projects and test-like assets, commands, prerequisites, expected and last observed results, fixtures/data, mocks, destructive/non-destructive behavior, known failures, and coverage tooling when present.
- `17_known_risks.md`: only actionable risks with severity, status, evidence, impact, preconditions, owner, remediation, and next step.
- `18_open_questions.md`: only source-evidence gaps with question ID, importance, evidence checked, owner, blocking level, status, and next action.
- `19_evidence_index.md`: every Evidence ID used elsewhere with topic, claim, source path, line/method, verification type, source commit, and status.
- `20_documentation_coverage.md`: coverage equation and minimum domains from Phase 0 inventory, with gaps linked to `17_known_risks.md` or `18_open_questions.md`.

## Ready Gate

Do not mark the run or any final output `Ready` if any of these are missing:

- Git remote, branch, and commit.
- Phase 0 inventory.
- Real Evidence Index.
- Coverage reconciliation.
- Detailed database entity/table/field coverage when database exists.
- Detailed API contract coverage when APIs exist.
- Job/hub/event contracts when jobs or realtime components exist.
- Local setup commands with working directory, prerequisites, and expected result.
- Config matrix when config exists.
- Operations map when Docker/ops assets exist.
- Test inventory when test projects exist.
- Template/upstream content properly isolated.
- Secret scan pass.
- Agent 8 final verdict `PASS`.
- No unresolved Critical conflict.

## Quick Review Table

Agent 8 MUST evaluate each final file against:

| File | Front matter | Evidence | Inventory/coverage | Contract tables | Diagrams when needed | Runbook/test | No template content | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
