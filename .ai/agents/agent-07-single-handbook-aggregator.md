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

1. `01_PROJECT_HANDOVER_FULL.md` (Summary & Index link to the others)
2. `02_PROJECT_CONTEXT.md`
3. `03_REPOSITORY_GUIDE.md`
4. `04_LOCAL_SETUP.md`
5. `05_CONFIGURATION_REFERENCE.md`
6. `06_ARCHITECTURE.md`
7. `07_DATABASE_REFERENCE.md`
8. `08_AUTH_AND_SECURITY.md`
9. `09_API_CATALOG.md`
10. `10_BACKGROUND_JOBS.md`
11. `11_REALTIME_SIGNALR_SOCKET.md`
12. `12_EXTERNAL_INTEGRATIONS.md`
13. `13_FRONTEND_GUIDE.md`
14. `14_OPERATIONS_RUNBOOK.md`
15. `15_DEPLOYMENT_AND_CICD.md`
16. `16_TESTING_GUIDE.md`
17. `17_KNOWN_RISKS.md`
18. `18_OPEN_QUESTIONS.md`
19. `19_EVIDENCE_INDEX.md`
20. `20_DOCUMENTATION_COVERAGE.md`

**CRITICAL LANGUAGE REQUIREMENT**: ALL 20 FILES MUST BE WRITTEN IN VIETNAMESE (Tiếng Việt). Technical terms and variables may remain in English.

You MUST read from the physical `.md` files of Agent 1-6. DO NOT HALLUCINATE.
