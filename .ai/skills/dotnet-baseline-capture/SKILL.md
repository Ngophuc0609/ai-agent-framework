---
name: dotnet-baseline-capture
description: Use when capturing Golden Master behavior before migrating .NET legacy code, including APIs, views, JSON, cookies, sessions, redirects, database side effects, and external API behavior.
---

# .NET Legacy Baseline Capture

## Vietnamese User Summary

Skill này tạo baseline/Golden Master trước khi migrate .NET legacy, không sửa source code.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/03-safety-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/15-agent-runtime-tool-policy.md`
- `.ai/rules/16-dotnet-parity-migration-rules.md`

## Goal

Create a trustworthy, evidence-backed baseline for legacy behavior before migration.

Do not edit production code while running this skill. Do not call write endpoints against production systems.

Endpoint discovery tools are only a starting point. After tools identify endpoints, the agent must manually inspect each selected endpoint's source code path and write a detailed baseline. Do not stop at generated empty templates or endpoint lists.

## Required Artifacts

Generate or update the applicable artifacts under the migration output namespace chosen by the repo or workflow:

- `01_LEGACY_SYSTEM_OVERVIEW.md`
- `02_API_CONTRACT_CATALOG.md`
- `03_LEGACY_JSON_COMPATIBILITY_PROFILE.md`
- `04_AUTH_SESSION_COOKIE_MAP.md`
- `05_CRYPTO_DEEP_LINK_MAP.md`
- `06_STATE_AND_SIDE_EFFECT_MATRIX.md`
- `07_EXTERNAL_INTEGRATION_MAP.md`
- `08_VIEW_STATIC_ROUTING_MAP.md`
- `09_GOLDEN_MASTER_TEST_CASES.md`
- `10_MIGRATION_RISK_REGISTER.md`
- `legacy-baseline.json`

Templates live in `.ai/templates/dotnet-parity-migration/`.

Use the current parity deliverable names from `.ai/rules/16-dotnet-parity-migration-rules.md`. The legacy artifact names above may be folded into:

- `00_MIGRATION_SCOPE.md`
- `01_LEGACY_INVENTORY.md`
- `02_LEGACY_BASELINE.md`
- `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md`
- `04_COMPATIBILITY_DESIGN.md`
- `05_NEW_PROJECT_BASELINE.md`
- `06_NEW_PROJECT_TEST_SCAFFOLD.md`
- `07_ENDPOINT_VIEW_MIGRATION_TRACKER.md`
- `08_CONTRACT_REGRESSION_REPORT.md`
- `09_VIEW_UI_REGRESSION_REPORT.md`
- `10_MIGRATION_RISK_REGISTER.md`
- `11_ACCEPTANCE_CHECKLIST.md`
- `15_DEFERRED_ISSUES_REPORT.md`
- `legacy-baseline.json`

Baseline capture owns the legacy evidence and the test specification source. New-project files may be created as stubs only when they clearly state `NOT_STARTED` or `BLOCKED`; do not present them as completed implementation artifacts.

## Required Endpoint Fields

For every endpoint, capture:

- ID.
- URL and HTTP method.
- Controller/action/source file.
- Auth requirement and authorization rule.
- Request content-type.
- Query, form, body, route, header, and cookie parameters.
- Response status and content-type.
- Response body shape.
- Response schema with concrete field names, nested object/array shapes, nullable behavior, and data types.
- Response construction trace, including the exact code path that builds anonymous objects, dynamic objects, DTOs, dictionaries, `DataTable`, `JObject`, serialized strings, or proxy payloads.
- Business sequence diagram for the endpoint or capability.
- Business rule summary for every decision branch that affects the response or side effects.
- JSON casing, null, date, enum, and numeric behavior.
- Response headers.
- Set-Cookie behavior.
- Redirect behavior.
- Session read/write keys and value types.
- Database, external API, and file side effects.
- React/view/third-party consumer when detected.
- Verification level: `DISCOVERED`, `CODE_VERIFIED`, `RUNTIME_VERIFIED`, `TEST_VERIFIED`, or `UNKNOWN`.
- Analysis status: `COMPLETE`, `PARTIAL`, or `BLOCKED`.

## Baseline-First Test Specification

After each endpoint, view, or business capability reaches `BASELINE_READY`, create or update `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md`.

The test specification must be sourced from legacy evidence only and must include:

- Exact request inputs from route, query, form, body, header, cookie, and session where applicable.
- Expected response status, headers, content-type, cookies, redirects, body text, JSON property names, casing, data types, object structure, null/missing/empty behavior, date/time format, enum representation, and dynamic field rules.
- Business branch conditions and expected branch outcomes.
- Database, file, external API, auth, permission, session, and cookie side effects.
- View contracts when applicable: rendered HTML, layout/partial, ViewBag/ViewData/Model, form names, script/CSS order, static asset paths, and browser refresh/deep-link behavior.

Do not generate unit or contract expectations from the new .NET implementation.

## Auth, Session, Cookie Baseline Contract

Capture these fields when auth/session/cookies affect the slice:

- Cookie name, domain, path, timeout, sliding expiration, SameSite, Secure, HttpOnly.
- LoginPath, AccessDeniedPath, unauthorized behavior, logout behavior.
- Principal, claims, role, SysAdmin, or custom permission mapping.
- Session key, value type, serialization format, timeout, captcha/OTP temporary state.

If production uses multiple instances or a load balancer, record that in the baseline and flag in-memory session as local/dev only unless legacy evidence proves otherwise.

## View/UI/Static Baseline Contract

For views or UI-backed endpoints, capture:

- Rendered HTML and layout/partial composition.
- ViewBag/ViewData/Model fields and types.
- Form action, method, and input names.
- Script order, CSS order, static file paths, image/font paths.
- React root element or client-side route fallback when present.
- Browser refresh/F5 and deep-link behavior.

## Manual Source Trace Requirement

Do not fill baseline artifacts by copying a blank template and populating only route/controller names from scanning tools.

For every P0/P1 endpoint, complete this source trace before writing the endpoint contract:

1. Open the controller/action source file and inspect the action body line by line.
2. Follow every call that contributes to request parsing, business decisions, response construction, status codes, headers, cookies, session, database writes, external calls, file operations, and redirects.
3. Resolve `new { ... }`, `dynamic`, `object`, `var`, dictionaries, `DataTable`, `JObject`, serialized strings, and wrapper responses such as `new { status = 200, data = ... }` to concrete response fields.
4. When `data` or another field is assigned from a service/repository/helper, inspect that method and continue tracing until the concrete DTO, anonymous object fields, database projection, or serializer payload is known.
5. If a response branch has multiple shapes, document every branch separately with its condition.
6. Write a sequence diagram that shows the request entering the controller, service/helper calls, database/external/file interactions, response construction, and returned payload.
7. Record evidence paths with file names and line references for controller, service, repository, DTO/model, config, and serializer behavior.

Do not describe unresolved payloads as only `object`, `dynamic`, `anonymous object`, `var`, `data`, or `mixed`. If concrete fields cannot be proven, mark the endpoint `analysisStatus: BLOCKED` for that response branch and list the missing evidence.

## Response Schema Detail

For every response body, document:

- Top-level fields in exact order when order is observable or serializer-dependent.
- Nested object fields.
- Array item type and item object fields.
- Field data type as observed or proven from source: `string`, `number`, `integer`, `boolean`, `object`, `array`, `null`, date/time string format, enum representation, or legacy serialized string.
- Nullable/missing/empty behavior.
- Field source: literal value, request parameter, database column/projection, DTO property, computed business rule, config value, session value, external API value, or dynamic runtime value.
- Branch condition for each alternative schema.

If runtime payload exists, it is the preferred evidence for exact serialized output. If only static source evidence exists, record `verificationLevel: CODE_VERIFIED` and clearly mark serializer/runtime-dependent fields as requiring runtime confirmation.

## Verification Level Definitions

Use these definitions strictly. Do not promote an endpoint beyond the evidence that was actually inspected.

- `DISCOVERED`: The endpoint was found from routes, controllers, views, client calls, configuration, or documentation, but its behavior has not been validated.
- `CODE_VERIFIED`: Controllers, models, routing logic, serializers, filters, and directly referenced source were statically analyzed. Static scripts and source-derived catalogs can reach only this level.
- `RUNTIME_VERIFIED`: Actual HTTP request and response evidence from a running legacy application was inspected, such as proxy exports, traffic dumps, server-side capture files, or browser/network captures.
- `TEST_VERIFIED`: Golden Master tests were executed against the legacy system or against checked-in captured fixtures that were produced from the running legacy system.
- `UNKNOWN`: Required evidence is missing or contradictory.

Inference from C# models, controller signatures, route tables, serializer defaults, or generated static catalogs is strictly prohibited as a basis for `RUNTIME_VERIFIED`.

## Golden Master Capture

For each P0/P1 endpoint or view, capture:

```text
request.json
request-headers.json
request-cookies.json
expected-status.txt
response-headers.json
response-cookies.json
response-body.json or response-body.txt
dynamic-fields.json
side-effects.md
notes.md
```

## Handling Missing Evidence

When Golden Master request or response files are missing, fail closed.

- If `request.json`, `response-body.json`, `response-body.txt`, proxy exports, browser captures, or equivalent runtime files are missing, do not infer, mock, synthesize, or generate them from C# models.
- Do not create sample response bodies from controller return types, DTO classes, comments, Swagger, or static extractor scripts.
- Mark the endpoint `verificationLevel: CODE_VERIFIED` when static source evidence exists, otherwise use `DISCOVERED` or `UNKNOWN`.
- Mark `analysisStatus: PARTIAL` when useful static evidence exists but runtime evidence is incomplete.
- Mark `analysisStatus: BLOCKED` when P0/P1 runtime evidence is required and cannot be obtained in the current runtime.
- Record the missing evidence in `notes.md`, the risk register, and any run status or tool limitation artifact used by the workflow.
- Prompt the user with concrete unblock options instead of filling the gap with generated data.

Use this user prompt shape when blocked on runtime evidence:

```text
Runtime evidence is missing for <endpoint>. I can only mark it CODE_VERIFIED from source.

To unblock RUNTIME_VERIFIED or TEST_VERIFIED baseline capture, provide one of:
1. Fiddler, Postman, browser DevTools, or proxy exports containing request and response payloads.
2. Permission to use the template `.ai/templates/dotnet-parity-migration/LegacyTrafficDumper.cs` in the legacy app to dump local/staging traffic.
3. Golden Master tests or checked-in fixtures generated from the running legacy application.
```

If the user chooses the traffic dumper option, copy or adapt the template into the legacy application only with user approval and only for local or staging capture. Never install it in production and never log secrets without redaction.

## Dynamic Fields

Do not hard-code tokens, timestamps, OTPs, GUIDs, random IDs, generated links, or environment-specific hostnames. Mark them in `dynamic-fields.json` with validation rules.

## Completion Rule

Do not mark baseline `COMPLETE` when:

- Endpoint counts differ between the catalog and `legacy-baseline.json`.
- Any P0 endpoint lacks request or response evidence.
- Any P0/P1 endpoint response schema is documented only as `object`, `dynamic`, `anonymous object`, `var`, or unresolved `data`.
- Any P0/P1 endpoint lacks manual source trace evidence and a business sequence diagram.
- Crypto or deep-link behavior has no test vector when used.
- Auth, session, or cookie behavior is unknown.
- Proxy JSON object/string behavior is unknown.
