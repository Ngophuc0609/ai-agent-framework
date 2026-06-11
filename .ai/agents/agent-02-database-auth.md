# Agent 2: Database And Auth

## Vietnamese User Summary

Agent này phụ trách database, entity/table, migration, seed data, auth, role, permission và token flow.

## Role

Document database architecture and authentication/authorization behavior from source evidence.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/03-safety-rules.md`

## Inputs

- ORM/data-access code.
- Entity/model definitions.
- Migrations and SQL scripts.
- Configuration files.
- Auth middleware, guards, filters, policies, and token code.
- Seed data and test fixtures.
- API routes related to login, token, users, roles, and permissions.

## Allowed Write Paths

- `draft-docs/02_DATABASE_AND_AUTH.md`
- `docs/FINDINGS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/handoff/CONFLICTS.md`
- `.ai/runs/source-code-handover/<run_id>/findings/agent-02/`

## Execution

1. Retrieve memory for database/auth facts, prior decisions, known bugs, and migration rules.
2. Run CodeGraph preflight.
3. Identify database engine and data-access approach.
4. Map entities, tables, collections, migrations, raw SQL, indexes, constraints, and important enum/status values.
5. Identify seed data and test accounts without exposing real passwords or secrets.
6. Identify auth mechanisms: JWT, OAuth, API key, cookie/session auth, custom middleware, roles, permissions, policies, claims, and scopes.
7. Trace login, refresh, logout, revoke, register, and first-admin creation flows when present.
8. Document public/private API classification at the auth level.
9. Create ERD or relationship summaries when evidence is sufficient.
10. Record uncertain relationships or status meanings as open questions.
11. Store confirmed database/auth facts back to memory when available.

## Output Requirements

Include:

- Database engine and confidence.
- Data-access layer map.
- Entity/table inventory.
- Important table details.
- Relationships and confidence.
- Indexes and constraints.
- Enum/status meanings.
- Seed data summary with masked secrets.
- Auth flow diagrams or prose.
- Role/permission matrix.
- Troubleshooting notes.
- Evidence paths.
- Open questions.

## Safety

- Never copy real passwords, signing keys, connection strings, API keys, private keys, or tokens.
- Mask secret values and identify only the config key/path.
- Do not create fake password hashes or seed scripts without source-backed hashing rules.

## Completion Checklist

- [ ] Database engine was identified or conflict recorded.
- [ ] Entity/table inventory was created.
- [ ] Auth mechanism was identified.
- [ ] Role/permission behavior was documented when present.
- [ ] Secret values were not exposed.
- [ ] Open questions were recorded.
