---
name: dotnet-parity-migration
description: Use when migrating any .NET legacy application to .NET 8 or newer while preserving exact 1:1 behavior, API contracts, DTO structures, views, authentication, session, cookies, and external behavior.
---

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

## Required Deliverables

Create or update these files under `migration-docs/` or the selected run namespace:

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

Do not treat a blank template as a deliverable. Each file must contain evidence-backed content or an explicit `BLOCKED`/`NOT_APPLICABLE` reason.

## Required Execution Flow

0. Define migration scope and initialize the tracker.
1. Identify the app type: ASP.NET MVC, Web API, WebForms, WCF, Worker, Console, Desktop, or mixed.
2. Build a legacy inventory: architecture, routing, configuration, authentication, session/cookies, views/static assets, jobs, integrations, and current risks.
3. Build or inspect Golden Master baseline evidence before migration code changes. P0/P1 APIs require request input, response output, field names, data types, object shapes, status codes, headers, cookies, and side effects.
4. Create `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md` from the legacy baseline. Do not derive tests from the new .NET 8+ output.
5. Create or update the .NET 8+ base project and test scaffold. Tests must exist before production behavior conversion.
6. For each endpoint, view, or business capability, write tests that verify 1:1 behavior from request parameters through business logic to response body and side effects.
7. Scaffold the corresponding .NET 8+ files needed for the target slice only after baseline and test assets exist.
8. Identify compatibility risks: request binding, JSON, model binding, auth, session, crypto, view rendering, file paths, database behavior, and external APIs.
9. Design the smallest compatibility adapter plan.
10. Convert one endpoint, view, job, integration, or business capability at a time, preserving legacy behavior exactly.
11. Run build, tests, and contract/view regression against the legacy baseline.
12. Compare the new output to the legacy baseline, not to expected behavior invented from the new code.
13. If a latent bug, cleanup opportunity, security risk, or optimization is detected, document it in `15_DEFERRED_ISSUES_REPORT.md` and do not fix it during parity migration unless the user explicitly approves a breaking or behavior-changing change.
14. Report `PASS`, `FAIL`, `BLOCKED`, `PARTIAL`, or `DEFERRED` per endpoint or view.

## Migration Unit Status

Every endpoint, view, job, integration, or business capability must use one of:

```text
NOT_STARTED
BASELINE_READY
TEST_SPEC_READY
BASE_PROJECT_READY
CONVERTING
REGRESSION_RUNNING
PASS
FAIL
BLOCKED
DEFERRED
```

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
- Do not mark a generated endpoint list or a blank template as a completed baseline.
- Do not mark a slice `PASS` when the response body is documented only as `object`, `dynamic`, `anonymous object`, `var`, or unresolved `data`.

## Output Template

```text
Migration Step:
Target:
Legacy evidence:
Baseline status:
Migration unit status:
Risk areas:
Test assets:
Change plan:
Files changed:
Verification:
Deferred issues:
Result: PASS / FAIL / BLOCKED / PARTIAL / DEFERRED
```
