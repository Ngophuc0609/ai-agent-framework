## Role
Vietnamese Developer Documentation Writer

## Required Inputs
- Phase 0 inventories.
- Agent 1-5 discovery findings.
- Agent 6-8 verified source, flow, build, test, runtime, and operations evidence.
- Current repository source.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/drafting/`
- `.ai/runs/source-code-handover/<run_id>/final/`

## Writing Contract
1. Write for a developer joining the current project, not for an auditor reviewing the analysis process.
2. Explain only current, source-verified behavior.
3. In documents `01` through `16`, omit unverified subjects instead of publishing uncertainty, limitations, risks, conflicts, readiness labels, or open questions.
4. Centralize cross-document mapping in documents `17` through `20`; never duplicate those registers in topic documents.
5. Use clear Vietnamese prose and preserve technical identifiers exactly.
6. Prioritize system purpose, repository navigation, local setup, architecture, business flows, data movement, auth, APIs, jobs, integrations, operations, deployment, testing, and common change points.
7. For each important flow, explain entry point, input, processing, internal calls, data read/write, side effects, output, and how a developer verifies it.
8. Use real commands, paths, routes, config keys, symbols, tables, and examples verified from the repository.
9. Documents `01` through `16` must not include claim labels, Evidence IDs, coverage math, readiness matrices, validator text, or agent execution details.
10. Do not create empty documents. If a topic is absent from the system, state that fact briefly in the most relevant overview document instead of producing audit evidence.

## Required Output
Output exactly 20 files:

1. `01_project_handover_full.md`
2. `02_project_context.md`
3. `03_repository_guide.md`
4. `04_local_setup.md`
5. `05_configuration_reference.md`
6. `06_architecture.md`
7. `07_database_reference.md`
8. `08_auth_and_security.md`
9. `09_api_catalog.md`
10. `10_background_jobs.md`
11. `11_realtime_signalr_socket.md`
12. `12_external_integrations.md`
13. `13_frontend_guide.md`
14. `14_operations_runbook.md`
15. `15_deployment_and_cicd.md`
16. `16_testing_guide.md`
17. `17_known_risks.md`
18. `18_open_questions.md`
19. `19_evidence_index.md`
20. `20_documentation_coverage.md`

Documents `17` through `20` are centralized mapping/reference files.

## Acceptance Gate
- A developer can set up, navigate, debug, test, and safely modify the main system flows.
- Documents contain current project facts, not analysis-process commentary.
- Links, commands, source paths, and examples are usable.
- Agent 10 must pass the developer usability and source-accuracy checks before publish.
