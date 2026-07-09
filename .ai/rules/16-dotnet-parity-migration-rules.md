# 16 .NET 1:1 Parity Migration Rules

## Vietnamese User Summary

Rule này khóa migration .NET legacy sang .NET 8+ theo chuẩn 1:1 parity, không modernize contract khi chưa được duyệt.

## Mission

Treat .NET legacy migration as a 1:1 parity migration unless the user explicitly approves a breaking change.

The internal framework may change, but externally observable behavior must stay the same.

## R-00 Default Mode: 1:1 Parity

Migration means parity migration, not refactor, cleanup, redesign, or modernization. Agents may change runtime, framework, project structure, hosting, and compatibility plumbing only as needed to run on .NET 8+ while preserving legacy behavior.

Do not change:

- Endpoint URL, HTTP method, route parameter, query/form/body/header/cookie parameter, or request content-type.
- Response status code, response content-type, response body, JSON property name, JSON casing, object structure, data type, null/empty/missing behavior, DateTime format/timezone, or enum format.
- Redirect behavior, cookie name/domain/path/timeout/SameSite/Secure/HttpOnly, session key, or session value type.
- View HTML structure, form action/method/input name, static asset path, script order, CSS order, image/font path, React root element, client-side route fallback, or browser refresh behavior.
- File upload/download behavior, default sort/filter/paging, database side effects, external API side effects, or business rules.

## R-01 Baseline First

Do not convert production behavior code for an endpoint, view, job, integration, or business capability until the required legacy baseline exists for that slice.

Minimum baseline evidence includes:

- URL/route/action and HTTP method.
- Query/form/body/header/cookie inputs and request content-type.
- Response status, headers, content-type, body, cookies, redirects, JSON casing/null/date/enum behavior.
- Auth, authorization, session reads/writes, view/static output when applicable.
- Database, file, external API side effects, and error cases.

If evidence is missing, set the slice status to:

```text
BLOCKED: Missing legacy baseline/runtime evidence
```

## R-02 Tests From Legacy Baseline

Tests must be derived from legacy baseline evidence before the .NET 8+ implementation is written or accepted:

```text
1. Capture legacy baseline.
2. Create unit/contract/snapshot test specification from the legacy baseline.
3. Create .NET 8+ test scaffold from that test specification.
4. Make the migrated code pass those legacy-derived tests.
```

Never write tests from the new implementation output, because that can validate a migration bug.

## R-03 Migrate One Slice At A Time

Track every endpoint, view, job, integration, or business capability separately.

Use these unit statuses:

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

A slice is complete only when baseline, test spec, implementation, regression evidence, approved differences, and deferred issue records all exist.

## R-04 Minimal Port Only

Allowed parity changes include compatibility replacements such as:

- `System.Web` to ASP.NET Core equivalents.
- `Web.config` to `appsettings.json` or environment variables while preserving legacy key behavior.
- FormsAuthentication to Cookie Authentication with equivalent behavior.
- `HttpContext.Current` to current `HttpContext` or `IHttpContextAccessor`.
- `Server.MapPath` to a path resolver preserving legacy resolution.
- `Request.Params` to a verified compatibility helper.
- Session serialization/deserialization preserving legacy value types.
- JSON serializer configuration preserving legacy output.

Do not clean code, rename DTOs, change wrappers, add validation, optimize queries, change flow, or fix legacy bugs during parity.

## R-05 Request.Params Compatibility

Do not mechanically map `Request.Params` by HTTP method, such as `POST -> Request.Form` or `GET -> Request.Query`.

Legacy `Request.Params` may read query, form, cookies, and server variables. Use a compatibility helper or verified binding strategy, for example:

```csharp
public static string? GetLegacyParam(HttpRequest request, string key)
{
    if (request.HasFormContentType && request.Form.ContainsKey(key))
        return request.Form[key].ToString();

    if (request.Query.ContainsKey(key))
        return request.Query[key].ToString();

    if (request.Cookies.ContainsKey(key))
        return request.Cookies[key];

    return null;
}
```

The source precedence must be verified by baseline/runtime evidence when it can affect behavior.

## R-06 JSON String Versus Raw JSON

Do not mechanically replace legacy `Json(responseString)` with `Content(responseString, "application/json")`.

Use Golden Master evidence:

- If legacy returns a raw JSON object, the migrated output must be the same raw JSON object.
- If legacy returns an escaped JSON string, the migrated output must remain an escaped JSON string.

If the snapshot is missing or ambiguous, mark the slice `BLOCKED` instead of choosing a serializer behavior by preference.

## R-07 Auth, Session, Cookie Contract

Auth/session/cookie behavior is a contract. Inventory and preserve:

- Cookie name, domain, path, timeout, sliding expiration, SameSite, Secure, and HttpOnly.
- LoginPath, AccessDeniedPath, unauthorized behavior (`302`, `401`, JSON, or other), and logout behavior.
- Principal/claims mapping, role mapping, SysAdmin or custom permission mapping.
- Session keys, session value types, session timeout, captcha/OTP temporary flows.

For multi-instance or load-balanced production, do not propose in-memory session as the primary production design. Use distributed session/cache or mark in-memory session as local/dev only.

## R-08 View/UI/Static Assets Are Contracts

Do not treat migration as API-only when views exist. Capture and regress rendered HTML, layout/partial behavior, ViewBag/ViewData/Model, form action/method/input names, script/CSS order, static paths, image/font paths, React root elements, client-side route fallback, and browser refresh behavior.

## R-09 Deferred Legacy Issues

Do not fix latent legacy bugs, code smells, security risks, abnormal logic, poor API design, slow queries, missing validation, hard-coded config, or weak exception handling during parity unless the user explicitly approves a behavior-changing fix.

Record them in:

```text
15_DEFERRED_ISSUES_REPORT.md
```

Required table:

```markdown
| ID | Category | Location | Description | Risk | Evidence | Suggested Fix Later | Fix Now? |
|---|---|---|---|---|---|---|---|
| DEF-001 | Security | AuthController.Login | Hard-coded key | High | file/method/line | Move to secret store in modernization phase | No |
```

## R-10 Acceptance Status

Use only these acceptance statuses:

```text
PASS     = New implementation matches the legacy baseline.
FAIL     = New implementation differs from the legacy baseline and requires a parity fix.
BLOCKED  = Baseline, evidence, environment, test data, or tooling is missing.
PARTIAL  = Some useful work is complete, but acceptance evidence is incomplete.
DEFERRED = Issue found and intentionally not fixed during parity.
```

Do not conclude done because build passes, the app starts, one manual case works, or the agent believes the logic is equivalent.

## R-11 Required Deliverables

Every .NET parity migration skill pack must require these files under `migration-docs/` or the workflow run namespace:

```text
00_MIGRATION_SCOPE.md
01_LEGACY_INVENTORY.md
02_LEGACY_BASELINE.md
03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md
04_COMPATIBILITY_DESIGN.md
05_NEW_PROJECT_BASELINE.md
06_NEW_PROJECT_TEST_SCAFFOLD.md
07_ENDPOINT_VIEW_MIGRATION_TRACKER.md
08_CONTRACT_REGRESSION_REPORT.md
09_VIEW_UI_REGRESSION_REPORT.md
10_MIGRATION_RISK_REGISTER.md
11_ACCEPTANCE_CHECKLIST.md
15_DEFERRED_ISSUES_REPORT.md
legacy-baseline.json
```

## R-12 AI Speeds Work, Evidence Decides

AI may scan source, generate inventory, identify risks, draft test specs from baseline, scaffold tests, suggest compatibility layers, port code minimally, read diffs, and create reports.

AI must not invent endpoints, DTO fields, response shapes, features, bug fixes, business rules, or modernization changes. Missing evidence means `BLOCKED`, not guessed output.

## Legacy Compatibility Non-Negotiables

- Do not invent features.
- Do not add new business rules.
- Do not remove legacy behavior because it looks wrong.
- Do not refactor business logic during the parity phase.
- Do not change endpoint URLs, HTTP methods, parameter names, response fields, object structure, casing, data types, null behavior, DateTime format, enum format, content-type, status codes, redirects, cookie behavior, session behavior, view output, or static asset paths unless explicitly approved.
- Do not replace legacy `HTTP 200 + Success=false` with `400`, `401`, or `500` unless the Golden Master proves that behavior.
- Do not replace escaped JSON string responses with raw JSON object responses unless the Golden Master proves legacy returned raw JSON.
- Do not convert `Request.Params` mechanically to only `Request.Form` or only `Request.Query`.
- Keep direct controller response behavior and proxy response behavior separate.
- Never commit or expose secrets, passwords, tokens, API keys, encryption keys, or production credentials.

## Required Phase Order

```text
Phase 0 - Migration Scope
Phase 1 - Legacy Inventory
Phase 2 - Legacy Baseline / Golden Master
Phase 3 - Unit/Contract Test Specification From Legacy Baseline
Phase 4 - New .NET 8+ Base Project
Phase 5 - New Project Test Scaffold
Phase 6 - Minimal Compatibility Design
Phase 7 - Slice-by-slice Endpoint/View/Business Conversion
Phase 8 - Contract/View Regression Against Legacy Baseline
Phase 9 - Acceptance, Deferred Issues, Cutover/Rollback Readiness
```

## Compatibility Checklist

For every migrated endpoint or view, verify:

- Route and HTTP method.
- Query, form, body, route, header, and cookie input.
- Request content-type.
- Response status code.
- Response content-type.
- Response body shape.
- JSON casing and property names.
- Null, missing, and empty behavior.
- DateTime and timezone format.
- Numeric, decimal, and enum behavior.
- Response headers.
- Set-Cookie behavior.
- Redirect behavior.
- Authentication and authorization behavior.
- Session read/write keys and value types.
- Database side effects.
- External API calls.
- File upload/download behavior.
- View HTML and static asset paths.

## Standard Risk Areas

- `Request.Params` fallback behavior across query, form, route, cookies, and server variables.
- MVC5 `Json(string)` versus ASP.NET Core `Content`, `Ok`, and `Json` behavior.
- FormsAuthentication to CookieAuthentication mapping.
- InProc Session to ASP.NET Core Session or Distributed Session.
- `HttpContext.Current` and `Server.MapPath`.
- `JavaScriptSerializer` versus `System.Text.Json` or Newtonsoft.Json.
- DateTime, enum, null handling, PascalCase/camelCase, and numeric precision.
- Razor helper differences.
- BundleConfig, static file paths, and script/style order.
- Deep link, encryption, and token compatibility.

## Done Means

Build pass is not enough. A migration slice is done only when build/tests pass and contract regression against Golden Master passes, or when unresolved gaps are reported as `BLOCKED`/`PARTIAL` with evidence paths.
