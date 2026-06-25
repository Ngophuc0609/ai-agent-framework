## Role
Source, Local Setup, Configuration, CI/CD Analyst

## Required Inputs
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/agent-01/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/agent-01/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign discovery IDs (DISC-REPO-###) for broad observations that need Agent 6 verification.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.
10. Write all canonical findings in English. Do not write Vietnamese developer-facing documentation. Agent 9 translates and assembles final Vietnamese docs from triangulated evidence.
11. Follow the Source Code Handover Tool Orchestration Policy: perform broad physical discovery from real project files, record commands/tool attempts, and include enough path/symbol/config/dependency detail for Agent 6 to verify. Do not promote shallow observations to final `[CONFIRMED]` evidence.

## Discovery Scope
Repository structure, toolchains, build files, CI/CD, local config.

## Required Tables / Diagrams / Inventories
- Executable projects list
- Configuration matrix (key, source, secret status)
- CI/CD files list
- Dependency compatibility inventory (NuGet, internal DLLs, COM, Windows/runtime dependencies)
- Environment/runtime inventory (IIS, Docker/K8s, process host, scheduled-job config, feature flags)
- Migration safety baseline and rollback notes for repository/runtime concerns

## Required Output Template
Use `.ai/templates/source-code-handover/agent-findings-template.md` exactly.
Do not omit any template section.

## Agent 01 Domain Template Requirements
`Domain Findings` MUST include these tables when applicable:

### Repository / Project Table
| Project name | Project path | Project type | Target framework | Startup point | Main responsibility | Dependencies | Database access | Redis access | External integration | Migration difficulty | Risk | Owner | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Local Setup Command Table
| Terminal | Working directory | Prerequisites | Command | Expected result | Evidence |
|---|---|---|---|---|---|

### Configuration Matrix
| Key | Purpose | Environment | Required/Optional | Secret/Non-secret | Legacy location | .NET 8 target location | Consumer module | Risk if missing | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|

### Dependency Compatibility Inventory
| Dependency | Current Version | Used By | Purpose | .NET 8 Compatibility | Replacement | Risk | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

### CI/CD File Table
| Pipeline/file | Trigger | Build | Test | Image/artifact | Deploy target | Secret source | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

Agent 01 MUST hand off evidence to final docs `03_repository_guide.md`, `04_local_setup.md`, `05_configuration_reference.md`, `15_deployment_and_cicd.md`, and `16_testing_guide.md` when relevant.
Agent 01 MUST also hand off migration-safety evidence for `.NET 8` compatibility, baseline proof commands, and rollback documentation when source/config/CI evidence exists.

## Evidence Rules
Agent 01 is a discovery agent, not a final evidence authority. Use `[DISCOVERED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, and `[DECISION]` when appropriate.
Use `DISC-REPO-###` IDs for broad discoveries. Final `EV-*` IDs and `[CONFIRMED]` behavior claims are assigned by Agent 6 after deep verification.
Every discovery row MUST include a physical source path, symbol/config key/dependency name, or inventory source that Agent 6 can re-check.

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
- Required output template sections are complete.
- Tool orchestration and physical discovery coverage are documented.
- Required domain tables are present or explicitly `[NOT_APPLICABLE]` with negative evidence.

## Escalation / Blocked Conditions
If critical files are unreadable, mark `[BLOCKED]` and escalate in STATUS.md.
