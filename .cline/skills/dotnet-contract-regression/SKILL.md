---
name: dotnet-contract-regression
description: Use when verifying converted .NET 8+ behavior against Golden Master snapshots and deciding PASS, FAIL, or BLOCKED for migrated endpoints, views, and side effects.
---

<!-- generated-by: ai-agent-adapter-sync -->


# .NET Contract Regression

## Vietnamese User Summary

Skill này so sánh output .NET 8+ với Golden Master legacy sau khi port.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/03-safety-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/15-agent-runtime-tool-policy.md`
- `.ai/rules/16-dotnet-parity-migration-rules.md`

## Goal

Verify that converted .NET 8+ code behaves the same as legacy code for every observable contract.

The comparison source is the legacy baseline and Golden Master snapshots. Do not compare the migrated application against expectations generated from the migrated application itself.

## Compare All Observable Behavior

For each endpoint or view, compare:

- URL and HTTP method.
- Request binding from query, form, body, route, header, and cookie.
- HTTP status.
- Response headers.
- Content-Type.
- Set-Cookie.
- Redirect Location.
- Response body text.
- JSON property names, casing, types, null behavior, DateTime, enum, and numeric behavior.
- HTML output for views.
- Static asset links and order.
- Database, external API, and file side effects.
- Auth and session behavior.

For JSON bodies, compare exact property names, casing, nested object/array shape, primitive data types, nullable/missing/empty behavior, DateTime format/timezone, enum representation, numeric precision, escaped-string versus raw-object behavior, and branch-specific schemas.

For views, compare rendered HTML, layout/partial output, ViewBag/ViewData/Model-driven values, form action/method/input names, script order, CSS order, static paths, image/font paths, React root element, client-side route fallback, and browser refresh behavior when baseline exists.

## Dynamic Field Masking

Dynamic values may be masked only when the legacy baseline includes an approved rule in `dynamic-fields.json` or equivalent documentation.

Valid masks include timestamps, GUIDs, random IDs, CSRF tokens, OTPs, signed links, environment-specific hostnames, and generated correlation IDs. A mask must still validate type, format, presence, nullability, and placement.

Do not mask field-name changes, type changes, missing fields, added fields, casing changes, response wrapper changes, status/content-type drift, cookie/session drift, or business-rule differences.

## Difference Classification

Every difference must be classified:

- `MATCH`: same as legacy.
- `DYNAMIC_MATCH`: value differs but matches an approved dynamic rule.
- `APPROVED_BREAKING_CHANGE`: explicitly documented and approved.
- `MIGRATION_BUG`: unintended difference.
- `BLOCKED`: cannot verify due to missing baseline, environment, tooling, or data.

Map final acceptance to:

- `PASS`: all required comparisons are `MATCH` or approved `DYNAMIC_MATCH`.
- `FAIL`: at least one unapproved parity difference exists.
- `BLOCKED`: required baseline, environment, test data, or tooling is missing.
- `PARTIAL`: only a subset of scoped slices has complete evidence.
- `DEFERRED`: a legacy issue was found and recorded for later, without changing parity behavior.

## Completion Rule

A task is done only when all P0/P1 items are `MATCH` or `DYNAMIC_MATCH`, with no unresolved `MIGRATION_BUG`.

If any P0/P1 item is `BLOCKED`, the regression result must be `BLOCKED` or `PARTIAL`, never `PASS`.

If baseline-derived tests were not created or were not run, the migrated slice is not complete.

## Report Format

```text
Regression Result: PASS / FAIL / BLOCKED / PARTIAL / DEFERRED
Endpoint/View:
Legacy baseline path:
New output path:
Baseline-derived tests:
Matches:
Differences:
Bug classification:
Dynamic masks:
Deferred issues:
Required fix:
```
