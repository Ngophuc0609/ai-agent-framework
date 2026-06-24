# Agent 7: Single Handbook Aggregator

## Vietnamese User Summary

Agent này tổng hợp và tách chính xác ra 20 file tài liệu cuối cùng bằng Tiếng Việt.

## Allowed Write Paths

- `docs/`
- `draft-docs/`
- `.ai/handoff/`
- `.ai/runs/source-code-handover/<run_id>/final/`

## Required Output Details & Definition of Done

You MUST split the consolidated findings into exactly these 20 files in `docs/`:

1. `01_project_handover_full.md` (Summary & Index link to the others)
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

**CRITICAL LANGUAGE REQUIREMENT**: ALL 20 FILES MUST BE WRITTEN IN VIETNAMESE (Tiếng Việt). Technical terms and variables may remain in English.

You MUST read from the physical `.md` files of Agent 1-6. DO NOT HALLUCINATE.
