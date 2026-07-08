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
- JSON casing, null, date, enum, and numeric behavior.
- Response headers.
- Set-Cookie behavior.
- Redirect behavior.
- Session read/write keys and value types.
- Database, external API, and file side effects.
- React/view/third-party consumer when detected.
- Verification level: `DISCOVERED`, `CODE_VERIFIED`, `RUNTIME_VERIFIED`, `TEST_VERIFIED`, or `UNKNOWN`.

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

## Dynamic Fields

Do not hard-code tokens, timestamps, OTPs, GUIDs, random IDs, generated links, or environment-specific hostnames. Mark them in `dynamic-fields.json` with validation rules.

## Completion Rule

Do not mark baseline `COMPLETE` when:

- Endpoint counts differ between the catalog and `legacy-baseline.json`.
- Any P0 endpoint lacks request or response evidence.
- Crypto or deep-link behavior has no test vector when used.
- Auth, session, or cookie behavior is unknown.
- Proxy JSON object/string behavior is unknown.
