---
name: dotnet-compatibility-port
description: Use when editing source code to port ASP.NET MVC, Web API, or .NET Framework code to ASP.NET Core or .NET 8+ using compatibility adapters while preserving 1:1 behavior.
---

# .NET Compatibility Port

## Vietnamese User Summary

Skill này dùng khi sửa code để port sang .NET 8+ nhưng vẫn giữ behavior legacy theo baseline.

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

Make the smallest source changes necessary to run on .NET 8+ while preserving legacy behavior.

Do not use this skill for production migration code until the relevant legacy baseline and baseline-derived tests exist.

If the workflow is blocked on missing baseline evidence or missing tests, this skill may only create migration plans, scaffold files with no business behavior, risk reports, or test assets. Do not convert business logic until the user supplies evidence or explicitly approves a documented exception.

## Required Pre-Edit Checks

1. Read the relevant baseline and Golden Master cases.
2. Read the baseline-derived unit/integration/snapshot tests for the target slice.
3. Confirm the target endpoint, view, job, class, or integration boundary.
4. Identify all public contract surfaces affected by the change.
5. Verify tests cover request inputs, business outcome, response status, response headers, content type, field names, data types, object shape, null/date/enum/numeric behavior, cookies, session, and side effects when applicable.
6. List compatibility risks and planned adapters.
7. Add or update missing focused regression tests before production behavior code.

If any item above is missing, do not convert production business logic. Mark the slice `BLOCKED: Missing legacy baseline/runtime evidence` or `BLOCKED: Missing baseline-derived tests`, and create only documentation, test specs, test scaffolds, or no-behavior project scaffolding.

## Preferred Patterns

### Request.Params

Do not mechanically replace `Request.Params` with only form or query access. Use a compatibility accessor when legacy actions read mixed sources.

Do not use a rule such as `POST -> Request.Form` or `GET -> Request.Query`. Legacy `Request.Params` can combine form, query string, cookies, and server variables. Preserve the observed precedence, and if precedence is not proven but can affect behavior, mark the slice `BLOCKED`.

### JsonResult

Determine endpoint behavior from Golden Master:

- If legacy returned a raw JSON object, return an equivalent raw JSON object.
- If legacy returned an escaped JSON string, return an equivalent escaped JSON string.

Do not choose raw object versus escaped string from framework defaults, DTO shape, or preference. If Golden Master evidence is missing, mark the slice `BLOCKED`.

Do not mechanically convert `Json(responseString)` to `Content(responseString, "application/json")`. Use `Content`, `Ok`, `Json`, or a custom compatibility result only when it reproduces the captured legacy wire output exactly.

### FormsAuthentication

Map old principal fields to `ClaimsPrincipal` without changing consumer behavior.

Preserve cookie name, domain, path, timeout, sliding expiration, SameSite, Secure, HttpOnly, LoginPath, AccessDeniedPath, unauthorized behavior, logout behavior, principal/claims/role mapping, and custom SysAdmin or permission behavior from baseline.

### Session

Map each session key with its old type and TTL. Use explicit serialization for object values.

For multi-instance or load-balanced production, do not use in-memory session as the primary design unless the user explicitly limits the scope to local/dev or the compatibility design documents an equivalent distributed session/cache plan.

### HttpContext.Current

Pass required context explicitly or use `IHttpContextAccessor` only at boundaries.

### Server.MapPath

Use an environment/path resolver wrapper to preserve relative path behavior.

### Web.config

Move settings to appsettings or environment configuration when needed, but preserve legacy key names through a compatibility settings wrapper if existing code expects them.

## Review Before Completion

- Baseline-derived tests existed before production behavior conversion.
- Request input and response output match legacy field names, data types, object shape, status, headers, cookies, and dynamic rules.
- No business logic refactor.
- No DTO rename or casing drift.
- No serializer default drift.
- No new validation.
- No auth behavior drift.
- No view path or static path drift.
- Latent bugs, cleanup opportunities, and optimizations were documented separately instead of fixed during parity migration.
- Any latent legacy issue is recorded in `15_DEFERRED_ISSUES_REPORT.md` with `Fix Now? = No` unless the user approved a separate breaking/fix phase.
- No secret leakage.
- Build, tests, and contract regression were run or explicitly blocked.

## Output Template

```text
Files changed:
Legacy behavior preserved:
Baseline-derived tests:
Compatibility adapters used:
Risks:
Tests run:
Diff vs baseline:
Deferred issues:
Result: PASS / FAIL / BLOCKED / PARTIAL / DEFERRED
```
