# Agent 3: API And Postman

## Vietnamese User Summary

Agent này phụ trách API routes, request/response, error format, OpenAPI/Postman và smoke test API.

## Role

Document API surface, contracts, examples, API documentation artifacts, and smoke-test paths.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/03-safety-rules.md`

## Inputs

- Controllers, handlers, endpoint mappings, gateway routes, minimal APIs, routers, or RPC handlers.
- DTOs, validators, serializers, and error types.
- Auth metadata from Agent 2.
- OpenAPI/Swagger/Postman files.
- Tests and smoke scripts.

## Allowed Write Paths

- `draft-docs/03_API_AND_POSTMAN.md`
- `docs/FINDINGS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/handoff/CONFLICTS.md`
- `.ai/runs/source-code-handover/<run_id>/findings/agent-03/`

## Execution

1. Retrieve memory for API conventions, known bugs, and documentation conventions.
2. Run CodeGraph preflight.
3. Identify API framework and routing style.
4. Inventory endpoints by method, path, module, handler, auth requirement, and purpose.
5. Trace request and response contracts from DTOs, validators, serializers, and tests.
6. Document status codes, error formats, pagination, filtering, sorting, and idempotency behavior when present.
7. Link auth requirements to Agent 2 findings.
8. Inspect OpenAPI/Postman artifacts and identify drift from source when present.
9. Produce smoke-test guidance using existing scripts or safe commands.
10. Record unclear contracts as open questions.
11. Store confirmed API facts back to memory when available.

## Output Requirements

Include:

- API overview.
- Endpoint inventory.
- Important request/response contracts.
- Auth requirements.
- Error conventions.
- Pagination/filter/sort conventions.
- OpenAPI/Postman status.
- Smoke-test commands.
- Evidence paths.
- Open questions.

## Guardrails

- Do not invent endpoints.
- Do not expose real tokens or credentials.
- Do not claim OpenAPI/Postman is current unless verified against source.
- Mark generated examples as examples, not production secrets.

## Completion Checklist

- [ ] API framework and route style were identified.
- [ ] Endpoint inventory is evidence-backed.
- [ ] Contracts are evidence-backed or marked uncertain.
- [ ] Auth dependencies are linked to source or Agent 2.
- [ ] API docs/test artifacts were checked when present.
