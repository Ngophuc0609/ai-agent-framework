# Developer Handover Documentation Quality Checklist

## Goal

Enable a new developer to understand the main 80% of the current system and become productive without reading the repository file by file.

## Required Final Documents

1. `01_project_handover_full.md`: project purpose, runtime topology, main modules, quick start, and links to the remaining docs.
2. `02_project_context.md`: business domain, actors, terminology, system boundaries, and external systems.
3. `03_repository_guide.md`: solution/project tree, entry points, dependency direction, and common change locations.
4. `04_local_setup.md`: prerequisites, configuration, database preparation, startup order, commands, URLs, smoke checks, reset, and troubleshooting.
5. `05_configuration_reference.md`: configuration keys, source, precedence, purpose, secret handling, and consuming components.
6. `06_architecture.md`: component and runtime topology, request/data/auth flows, boundaries, and diagrams.
7. `07_database_reference.md`: DbContexts, entities, tables, important fields, relationships, migrations, seed/reset, and read/write consumers.
8. `08_auth_and_security.md`: authentication schemes, token/session lifecycle, claims, roles, policies, protected/anonymous routes, and auth flow.
9. `09_api_catalog.md`: routes, methods, handlers, auth, request/response fields, validation, status/error behavior, side effects, and examples.
10. `10_background_jobs.md`: registration, trigger/schedule, handler, dependencies, stores, side effects, retry/failure behavior, and verification.
11. `11_realtime_signalr_socket.md`: routes, events, producer/consumer, payload, user/group mapping, auth, and client flow.
12. `12_external_integrations.md`: systems, caller, trigger, protocol, auth method, config, contract, timeout/retry behavior, and test method.
13. `13_frontend_guide.md`: apps, routes/pages, components, assets, build flow, auth/API patterns, and debugging.
14. `14_operations_runbook.md`: runtime map, health checks, logs/traces, dependencies, common incidents, verification, restart, and rollback commands.
15. `15_deployment_and_cicd.md`: pipelines, triggers, build/test/scan, artifacts/images, environments, migrations, deployment, approval, rollback, and versioning.
16. `16_testing_guide.md`: test projects, commands, prerequisites, fixtures/mocks, test data, expected results, and how to add tests.
17. `17_known_risks.md`: centralized source-backed risk register.
18. `18_open_questions.md`: centralized unresolved-question register.
19. `19_evidence_index.md`: centralized mapping from documentation claims to source evidence.
20. `20_documentation_coverage.md`: centralized inventory-to-document coverage map.

## Flow Quality

For every important API, job, realtime event, integration, and data mutation, explain:

- entry point and caller,
- input/source data,
- processing and branch rules,
- internal service/repository/client calls,
- database/cache/queue/external side effects,
- output or observable result,
- source files and symbols,
- test or smoke verification.

## Developer Usability

- Start each document with its practical purpose.
- Prefer tables and diagrams for inventories and flows.
- Include a "Điểm thường chỉnh sửa" section where useful.
- Commands must include working directory and expected result.
- Link related documents instead of duplicating content.
- Use Vietnamese prose and preserve technical identifiers.

## Forbidden Content In Documents `01` Through `16`

Topic docs must not contain:

- headings for risks, open questions, limitations, readiness, evidence, or coverage;
- `[CONFIRMED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[BLOCKED]`, `[NOT_APPLICABLE]`, or `EV-*` IDs;
- agent execution status, tool limitations, validation instructions, or analysis methodology;
- template placeholders, invented values, secrets, or generic tutorials unrelated to the repository.

## Centralized Mapping Documents

Documents `17` through `20` are exempt from the topic-document restrictions for their assigned content only. Topic documents may link to them without duplicating their content.

## Internal Quality Control

Agents 6-8 and Agent 10 still use evidence, coverage reconciliation, limitations, conflicts, and rejected findings internally. Those artifacts prove accuracy but are not developer deliverables.

## Acceptance

- Exactly 20 expected Markdown files exist.
- A new developer can set up and run the system.
- Main request, data, auth, job, integration, and deployment flows are understandable.
- Common modification and debugging entry points are documented.
- Source paths, commands, routes, and examples are current.
- Links, Vietnamese language, secret scan, and deterministic validation pass.
