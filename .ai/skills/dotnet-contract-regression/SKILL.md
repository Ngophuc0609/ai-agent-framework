---
name: dotnet-contract-regression
description: Use when verifying converted .NET 8+ behavior against Golden Master snapshots and deciding PASS, FAIL, or BLOCKED for migrated endpoints, views, and side effects.
---

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

## Difference Classification

Every difference must be classified:

- `MATCH`: same as legacy.
- `DYNAMIC_MATCH`: value differs but matches an approved dynamic rule.
- `APPROVED_BREAKING_CHANGE`: explicitly documented and approved.
- `MIGRATION_BUG`: unintended difference.
- `BLOCKED`: cannot verify due to missing baseline, environment, tooling, or data.

## Completion Rule

A task is done only when all P0/P1 items are `MATCH` or `DYNAMIC_MATCH`, with no unresolved `MIGRATION_BUG`.

## Report Format

```text
Regression Result: PASS / FAIL / BLOCKED
Endpoint/View:
Legacy baseline path:
New output path:
Matches:
Differences:
Bug classification:
Required fix:
```
