# 16 .NET Parity Migration Rules

## Vietnamese User Summary

Rule này khóa migration .NET legacy sang .NET 8+ theo chuẩn 1:1 parity, không modernize contract khi chưa được duyệt.

## Mission

Treat .NET legacy migration as a 1:1 parity migration unless the user explicitly approves a breaking change.

The internal framework may change, but externally observable behavior must stay the same.

## Non-Negotiable Rules

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
Phase 0 - Legacy Inventory
Phase 1 - Golden Master Baseline
Phase 2 - Compatibility Design
Phase 3 - Minimal Porting
Phase 4 - Contract Regression
Phase 5 - Browser/View Regression
Phase 6 - Staging/Cutover/Rollback
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

Build pass is not enough. A migration slice is done only when build/tests pass and contract regression against Golden Master passes, or when unresolved gaps are reported as `BLOCKED`.
