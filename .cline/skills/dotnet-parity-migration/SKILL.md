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

The migration must be baseline-first and test-first. Production migration code must not be treated as complete until tests derived from the legacy behavior pass against the .NET 8+ implementation.

## Required Execution Flow

1. Identify the app type: ASP.NET MVC, Web API, WebForms, WCF, Worker, Console, Desktop, or mixed.
2. Build a baseline document set that preserves the current legacy state: architecture, routing, configuration, authentication, session/cookies, request/response contracts, business rules, database and external side effects, views/static assets, and known risks.
3. Build or inspect Golden Master evidence before migration code changes. P0/P1 APIs require request input, response output, field names, data types, object shapes, status codes, headers, cookies, and side effects.
4. Create or update the .NET 8+ unit/integration/snapshot test project before production migration code. Tests must be derived from legacy source and runtime evidence, not invented desired behavior.
5. For each API or business capability, write tests that verify 1:1 behavior from request parameters through business logic to response body and side effects.
6. Scaffold the corresponding .NET 8+ files needed for the target slice only after baseline and test assets exist.
7. Identify compatibility risks: request binding, JSON, model binding, auth, session, crypto, view rendering, file paths, database behavior, and external APIs.
8. Design the smallest compatibility adapter plan.
9. Convert one API or business capability at a time, preserving legacy behavior exactly.
10. Run build, tests, and contract regression.
11. Compare the new output to the legacy baseline.
12. If a latent bug, cleanup opportunity, or optimization is detected, document it in a report and do not fix it during parity migration unless the user explicitly approves a breaking or behavior-changing change.
13. Report `PASS`, `FAIL`, `BLOCKED`, or `PARTIAL` per endpoint or view.

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
- Do not implement migration production code before baseline-derived tests exist, except for explicitly approved scaffolding that contains no business behavior.
- Do not fix latent legacy bugs, validation gaps, naming issues, or performance problems during parity migration. Record them in the risk/improvement report.
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
Test assets:
Change plan:
Files changed:
Verification:
Result: PASS / FAIL / BLOCKED / PARTIAL
```
