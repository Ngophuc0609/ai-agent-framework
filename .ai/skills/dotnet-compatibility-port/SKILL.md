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

Do not use this skill until the relevant legacy baseline exists or the workflow is explicitly blocked on missing baseline evidence.

## Required Pre-Edit Checks

1. Read the relevant baseline and Golden Master cases.
2. Confirm the target endpoint, view, job, class, or integration boundary.
3. Identify all public contract surfaces affected by the change.
4. List compatibility risks and planned adapters.
5. Add or update focused regression tests where feasible.

## Preferred Patterns

### Request.Params

Do not mechanically replace `Request.Params` with only form or query access. Use a compatibility accessor when legacy actions read mixed sources.

### JsonResult

Determine endpoint behavior from Golden Master:

- If legacy returned a raw JSON object, return an equivalent raw JSON object.
- If legacy returned an escaped JSON string, return an equivalent escaped JSON string.

### FormsAuthentication

Map old principal fields to `ClaimsPrincipal` without changing consumer behavior.

### Session

Map each session key with its old type and TTL. Use explicit serialization for object values.

### HttpContext.Current

Pass required context explicitly or use `IHttpContextAccessor` only at boundaries.

### Server.MapPath

Use an environment/path resolver wrapper to preserve relative path behavior.

### Web.config

Move settings to appsettings or environment configuration when needed, but preserve legacy key names through a compatibility settings wrapper if existing code expects them.

## Review Before Completion

- No business logic refactor.
- No DTO rename or casing drift.
- No serializer default drift.
- No new validation.
- No auth behavior drift.
- No view path or static path drift.
- No secret leakage.
- Build, tests, and contract regression were run or explicitly blocked.

## Output Template

```text
Files changed:
Legacy behavior preserved:
Compatibility adapters used:
Risks:
Tests run:
Diff vs baseline:
Result:
```
