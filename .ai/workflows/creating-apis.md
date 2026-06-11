# Creating APIs Workflow

## Vietnamese User Summary

Workflow này dùng cho API đã có sẵn. Tạo endpoint/API mới phải dùng `developing-backend-feature-tdd`.

## Skill

Use `.ai/skills/creating-apis/SKILL.md`.

## Allowed Write Paths

- Source files required by the API change.
- Test files required by the API change.
- Existing API documentation files when the repository already maintains them.
- `.ai/runs/creating-apis/<run_id>/`

## Execution

1. Resolve the request through `.ai/registry/triggers.yml`.
2. If the request is for a new endpoint or new API feature, route to `developing-backend-feature-tdd`.
3. Read the `creating-apis` skill.
4. Check git status.
5. Run CodeGraph preflight.
6. Retrieve project/API memory.
7. Identify existing API patterns.
8. Confirm the API contract.
9. Add or update tests before changing behavior when feasible.
10. Implement the smallest coherent change.
11. Add or update documentation when applicable.
12. Run validation commands available in the repository.
13. Store verified findings back to memory when available.
14. Respond to the user in Vietnamese.

## Contract Checklist

- HTTP method.
- Route path.
- Request body, query, and headers.
- Response shape and status codes.
- Auth and permission requirements.
- Validation rules.
- Side effects.
- Persistence or integration dependencies.
- Tests and docs to update.

## Fallbacks

If CodeGraph or MCP Memory is unavailable, follow the fallback rules in:

- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`

## Quality Gates

- [ ] Existing API conventions were checked.
- [ ] Contract is explicit or open questions are recorded.
- [ ] Auth and validation are preserved.
- [ ] Tests or smoke checks were run or limitation recorded.
- [ ] Documentation was updated when required by repo convention.
- [ ] Final response is in Vietnamese.
