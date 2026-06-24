import os

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

common_sections = """
## Role
{role}

## Inputs bắt buộc
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/{agent_id}/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/{agent_id}/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign Evidence IDs (EV-{prefix}-###) for claims.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.

## Discovery Scope
{scope}

## Required Tables / Diagrams / Inventories
{tables}

## Evidence Rules
Must use `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`.
`[CONFIRMED]` claims require source path and line number.

## Negative Evidence Rules
Only use `[NOT_APPLICABLE]` if status is `not_found_after_scan`. `scan_failed` or `tool_unavailable` cannot be marked N/A.

## Coverage Reconciliation
Formula: `accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`

## Required Output Headings
- Scope
- Evidence List
- Discovery Reconciliation
- Domain Findings
- Limitations
- Open Questions
- Risks

## Forbidden Content
No `dotnet new` (unless template repo), no generic code examples, no upstream placeholder domains/passwords without `[UPSTREAM_REFERENCE]`.

## Acceptance Gate
- File exists and is non-empty.
- Coverage math is sound.
- No hallucinated data.

## Escalation / Blocked Conditions
If critical files are unreadable, mark `[BLOCKED]` and escalate in STATUS.md.
"""

agent_1 = common_sections.format(
    role="Source, Local Setup, Configuration, CI/CD Analyst",
    agent_id="agent-01",
    prefix="REPO",
    scope="Repository structure, toolchains, build files, CI/CD, local config.",
    tables="- Executable projects list\n- Configuration matrix (key, source, secret status)\n- CI/CD files list"
)

agent_2 = common_sections.format(
    role="Database & Auth Analyst",
    agent_id="agent-02",
    prefix="DB",
    scope="DbContexts, entities, migrations, raw SQL, identity schemes, policies.",
    tables="- DB topology table\n- DB Dictionary (table/field/type)\n- Auth client/policy inventory\n- ERD diagram (Mermaid)"
)

agent_3 = common_sections.format(
    role="API & Endpoint Analyst",
    agent_id="agent-03",
    prefix="API",
    scope="Controllers, Minimal APIs, OpenAPI, OIDC, Webhooks.",
    tables="- Endpoint catalog (route, method, auth, status codes)\n- Request/Response DTO mapping\n- Flow diagram for complex/critical APIs"
)

agent_4 = common_sections.format(
    role="Business, Frontend, Integration Analyst",
    agent_id="agent-04",
    prefix="BIZ",
    scope="Business logic flows, frontend routing, 3rd party integrations.",
    tables="- Business components list\n- Integration cards (caller, config, failure behavior)\n- Frontend-backend mapping"
)

write_file(".ai/agents/agent-01-source-local.md", agent_1)
write_file(".ai/agents/agent-02-database-auth.md", agent_2)
write_file(".ai/agents/agent-03-api-postman.md", agent_3)
write_file(".ai/agents/agent-04-business-frontend.md", agent_4)
print("Updated Agents 1-4")
