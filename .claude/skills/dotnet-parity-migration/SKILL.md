---
name: dotnet-parity-migration
description: Use when migrating any .NET legacy application to .NET 8 or newer while preserving exact 1:1 behavior, API contracts, DTO structures, views, authentication, session, cookies, and external behavior.
---

<!-- generated-by: ai-agent-adapter-sync -->


# .NET Parity Migration

## Vietnamese User Summary

Skill này điều phối migration .NET legacy sang .NET 8+ theo chuẩn 1:1 contract và behavior parity.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/03-safety-rules.md`
- `.ai/rules/05-workflow-execution-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/15-agent-runtime-tool-policy.md`
- `.ai/rules/16-dotnet-parity-migration-rules.md`

## Supporting Skills

Load only the supporting skill needed for the current phase:

- `.ai/skills/dotnet-baseline-capture/SKILL.md` before migration code changes.
- `.ai/skills/dotnet-compatibility-port/SKILL.md` when editing code.
- `.ai/skills/dotnet-contract-regression/SKILL.md` after porting.

## Goal

Upgrade the internal .NET runtime or framework while preserving every externally observable behavior unless a breaking change is explicitly documented and approved.

This is not a feature project and not a refactor project.

## Required Execution Flow

1. Identify the app type: ASP.NET MVC, Web API, WebForms, WCF, Worker, Console, Desktop, or mixed.
2. Build an inventory of endpoints, views, routes, config, auth, session, cookies, database usage, external APIs, static files, and side effects.
3. Build or inspect a Golden Master baseline before code changes.
4. Identify compatibility risks: request binding, JSON, model binding, auth, session, crypto, view rendering, file paths, database behavior, and external APIs.
5. Design the smallest compatibility adapter plan.
6. Port the smallest compatible slice.
7. Run build, tests, and contract regression.
8. Compare the new output to the legacy baseline.
9. Report `PASS`, `FAIL`, `BLOCKED`, or `PARTIAL` per endpoint or view.

## Compatibility Adapters To Prefer

- `LegacyRequestParams` for `Request.Params` behavior.
- `LegacyJsonResult` or per-endpoint response compatibility for MVC5 `JsonResult` behavior.
- `LegacySessionSerializer` for session object values.
- `LegacyPathResolver` for `Server.MapPath` behavior.
- `LegacyAuthClaimsMapper` for FormsAuthentication or custom principal compatibility.
- `LegacyCryptoAdapter` for old encryption, deep-link tokens, or signed links.
- Compatibility settings wrappers when legacy key names must remain stable.

## Prohibited Shortcuts

- Do not treat build success as acceptance.
- Do not guess legacy behavior when evidence is missing.
- Do not add or remove business rules.
- Do not modernize contracts during the parity phase.
- Do not replace legacy `HTTP 200 + Success=false` with `400`, `401`, or `500` unless the baseline proves that behavior.
- Do not replace escaped JSON string responses with raw JSON object responses unless the Golden Master proves legacy returned raw JSON.
- Do not mechanically replace `Request.Params` with only `Request.Form` or only `Request.Query`.
- Do not clean up old DTO property names when frontend or integration consumers depend on them.

## Output Template

```text
Migration Step:
Target:
Legacy evidence:
Baseline status:
Risk areas:
Change plan:
Files changed:
Verification:
Result: PASS / FAIL / BLOCKED / PARTIAL
```
