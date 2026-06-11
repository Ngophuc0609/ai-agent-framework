# 06 Quality Gates

## Vietnamese User Summary

Rule này định nghĩa các điều kiện bắt buộc trước khi coi một workflow là hoàn thành.

## General Gates

Before finishing any workflow, verify:

- The selected skill and workflow were resolved through the registry.
- Required rules were applied.
- Allowed write paths were respected.
- Runtime limitations are documented.
- User-facing chat response is in Vietnamese.
- The cost optimization checklist was applied.

## Source-Code Gates

For source-code reading, documentation, debugging, refactoring, or API creation:

- CodeGraph preflight was attempted.
- If CodeGraph was unavailable, user-approved fallback was used.
- Memory was retrieved before module analysis when memory tools were available.
- Project summary docs were read before deeper source reads when present.
- File reads were narrowed to the current task scope.
- Current source code was treated as the source of truth.
- Important claims include file or command evidence.
- Inferences are labeled.
- Unknowns are listed as open questions.

## Memory Gates

- Project namespace is used.
- No secrets are stored.
- No large raw source code is stored.
- Only verified durable findings are saved.
- Memory writes are logged.
- Conflicting memory is updated or flagged for review/delete.

## Documentation Gates

- The documentation covers only evidence-backed areas.
- Missing areas are marked as not detected instead of fabricated.
- Final output includes readiness.
- Final response summarizes files and status rather than pasting full docs.

## API Gates

For API changes:

- Existing route/controller/service patterns were checked.
- Auth, validation, middleware, and error conventions were preserved.
- Request/response contracts were confirmed or documented.
- Tests or smoke checks were added or updated when feasible.
- API docs/OpenAPI/Postman files were updated when the repo already maintains them.

## Cost Gates

- Memory was searched before scanning code.
- `docs/PROJECT_CONTEXT.md` was read when present.
- Whole-repository reading was avoided unless necessary.
- Git diff was used for review or commit tasks involving existing changes.
- Strong reasoning was reserved for difficult analysis, security, architecture, debugging, or multi-file refactoring.
- Reusable findings were summarized into memory or project docs.

## Readiness Levels

- `Ready`: All required outputs exist, evidence is sufficient, and no blocking unknowns remain.
- `Partial`: Useful output exists but some evidence, validation, or tool support is incomplete.
- `Blocked`: Execution cannot continue without user input or missing external capability.
