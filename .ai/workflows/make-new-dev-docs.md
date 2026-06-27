# Source Code Handover Workflow

## Objective

Produce 20 Vietnamese developer documents that explain the current system clearly enough for a new developer to set up, navigate, modify, test, debug, and operate it.

## Output Boundary

- Internal artifacts under `inventory/`, `evidence/`, `findings/`, `verification/`, and `validation/` may contain analysis metadata.
- Final and published docs contain current-system knowledge only.
- Documents `01` through `16` must not repeat risks, open questions, limitations, readiness, coverage, evidence indexes, or agent execution details.
- Documents `17` through `20` retain centralized risk, question, evidence, and coverage mappings.

## Preflight

1. Read the selected skill, this workflow, and runtime tool policy.
2. Initialize `.ai/runs/source-code-handover/<run_id>/` with the project script.
3. Record source commit, branch, repository root, and isolation mode.
4. Attempt CodeGraph because this is repository-wide architecture work; use approved fallback only when the workflow can still produce reliable evidence.
5. Keep tool installation separate and approval-gated.

## Phase 0: Deterministic Inventory

Create inventories for projects, entry points, configuration, dependencies, database assets, migrations, routes, API contracts, auth, jobs, queues, realtime, integrations, frontend, Docker/deployment, CI/CD, tests, and runtime artifacts.

Inventory records must identify physical source paths and symbols. Missing or failed discovery remains internal.

## Phase 1: Domain Discovery

- Agent 1: repository, projects, entry points, configuration.
- Agent 2: database, migrations, auth, permissions.
- Agent 3: API contracts, routes, examples, tests.
- Agent 4: business flows, frontend, external systems.
- Agent 5: jobs, realtime, operations, deployment, CI/CD.

Agents write English internal findings from physical source files.

## Phase 2: Verification

- Agent 6 verifies exact files, symbols, routes, tables, keys, and call sites.
- Agent 7 traces request/data/auth/job/integration flows across layers and reconciles contradictions internally.
- Agent 8 runs safe build/test/static checks and verifies runtime/operations facts and secret safety.

Only verified current-system facts pass to Agent 9.

## Phase 3: Developer Documentation

Agent 9 writes exactly the 20 files defined by `.ai/rules/08-source-code-handover-quality-checklist.md`. The developer template applies to documents `01` through `16`.

Agent 9 must:

- explain the system rather than the analysis;
- omit unknown subjects instead of publishing gaps;
- avoid claim labels, Evidence IDs, readiness, limitations, risks, and questions in documents `01` through `16`;
- include practical setup, flows, commands, source paths, change points, and verification steps.

## Phase 4: Independent Validation

Agent 10 checks:

- source accuracy against internal evidence and current files;
- completeness of the 20-document developer set;
- setup and command usability;
- architecture, data-flow, auth, API, job, integration, deployment, and testing depth;
- Vietnamese language, links, placeholders, and secret redaction;
- absence of duplicated mapping/audit content in documents `01` through `16`.

## Publish Gate

Publish only when:

1. Agent 10 writes structured `Verdict: PASS`.
2. Deterministic run validation succeeds.
3. `STATUS.md` shows completed Agents 1-10 and valid isolation.
4. All 20 documents are copied to `docs/`, with mapping content centralized in documents `17` through `20`.
