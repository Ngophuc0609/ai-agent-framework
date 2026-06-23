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

1. `PROJECT_HANDOVER_FULL.md` (Summary & Index link to the others)
2. `PROJECT_CONTEXT.md`
3. `REPOSITORY_GUIDE.md`
4. `LOCAL_SETUP.md`
5. `CONFIGURATION_REFERENCE.md`
6. `ARCHITECTURE.md`
7. `DATABASE_REFERENCE.md`
8. `AUTH_AND_SECURITY.md`
9. `API_CATALOG.md`
10. `BACKGROUND_JOBS.md`
11. `REALTIME_SIGNALR_SOCKET.md`
12. `EXTERNAL_INTEGRATIONS.md`
13. `FRONTEND_GUIDE.md`
14. `OPERATIONS_RUNBOOK.md`
15. `DEPLOYMENT_AND_CICD.md`
16. `TESTING_GUIDE.md`
17. `KNOWN_RISKS.md`
18. `OPEN_QUESTIONS.md`
19. `EVIDENCE_INDEX.md`
20. `DOCUMENTATION_COVERAGE.md`

**CRITICAL LANGUAGE REQUIREMENT**: ALL 20 FILES MUST BE WRITTEN IN VIETNAMESE (Tiếng Việt). Technical terms and variables may remain in English.

You MUST read from the physical `.md` files of Agent 1-6. DO NOT HALLUCINATE.
