# Maintaining Existing APIs Workflow

## Vietnamese User Summary

Workflow này dùng cho API đã có sẵn. Tạo endpoint/API mới phải dùng `developing-backend-feature-tdd`.

## Skill

Use `.ai/skills/maintaining-existing-apis/SKILL.md`.

## Allowed Write Paths

- Source files required by the API change.
- Test files required by the API change.
- Existing API documentation files when the repository already maintains them.
- `.ai/runs/maintaining-existing-apis/<run_id>/`

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

## Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only, not source of truth. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Execution

1. Resolve the workflow from `.ai/registry/workflows.yml`. Expected key: `maintaining-existing-apis`. If missing, record a blocking finding and continue in fallback mode.
2. If the request is for a new endpoint or new API feature, route to `developing-backend-feature-tdd`.
3. Read the `maintaining-existing-apis` skill.
4. Check git status.
5. Run CodeGraph preflight.
6. Retrieve project/API memory (as supplementary context).
7. Identify existing API patterns.
8. Confirm the API contract.
9. Add or update tests before changing behavior when feasible.
10. Implement the smallest coherent change.
11. Add or update documentation when applicable.
12. Run final validation commands available in the repository (e.g. secret scan, git diff --check, tests).
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
- [ ] No secrets were exposed.
- [ ] Final response is in Vietnamese.
