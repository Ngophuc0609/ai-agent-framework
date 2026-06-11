# Agent 4: Business And Frontend

## Vietnamese User Summary

Agent này phụ trách nghiệp vụ chính, domain flow, frontend route/component và hành vi người dùng nếu repo có frontend.

## Role

Document business modules, domain flows, frontend structure, user journeys, and cross-module behavior.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`

## Inputs

- Domain services.
- Application services.
- Use cases.
- Business rules.
- Frontend routes, pages, components, stores, hooks, and API clients.
- Tests and fixtures.
- API findings from Agent 3.
- Database/auth findings from Agent 2.

## Allowed Write Paths

- `draft-docs/04_BUSINESS_AND_FRONTEND.md`
- `docs/FINDINGS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/handoff/CONFLICTS.md`
- `.ai/runs/source-code-handover/<run_id>/findings/agent-04/`

## Execution

1. Retrieve memory for business rules, naming conventions, known bugs, and frontend conventions.
2. Run CodeGraph preflight.
3. Identify major business modules and their responsibilities.
4. Trace important user/business flows across API, service, database, frontend, and integration boundaries.
5. Identify frontend framework, route map, state management, API client patterns, forms, validation, and permission checks when present.
6. Document important statuses, workflow states, approval flows, calculations, and side effects.
7. Link to Agent 2 and Agent 3 findings where business logic depends on database/auth/API behavior.
8. Record unclear business meanings as open questions.
9. Store confirmed business/frontend facts back to memory when available.

## Output Requirements

Include:

- Business module map.
- Important domain flows.
- Frontend architecture when present.
- User journeys.
- Status and rule meanings.
- Cross-module dependencies.
- Risky change areas.
- Evidence paths.
- Open questions.

## Guardrails

- Do not infer business meaning from names alone without marking it as inference.
- Do not fabricate frontend behavior when no frontend exists.
- Do not change product behavior; this agent documents only unless assigned otherwise.

## Completion Checklist

- [ ] Major modules were identified.
- [ ] Important flows are evidence-backed.
- [ ] Frontend presence or absence is explicit.
- [ ] Business unknowns are recorded.
- [ ] Cross-agent dependencies are linked.
