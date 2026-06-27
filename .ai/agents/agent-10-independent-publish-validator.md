## Role
Independent Developer Documentation Validator

## Required Inputs
- Current repository source.
- Phase 0 inventories and Agent 6-8 evidence.
- `.ai/runs/source-code-handover/<run_id>/final/`.
- `STATUS.md`.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/validation/`
- `.ai/runs/source-code-handover/<run_id>/publish/`

## Validation Contract
1. Require exactly the 20 developer documents defined by Agent 9.
2. Verify every technical statement against current source or internal evidence without exposing audit details in final docs.
3. Reject documents `01` through `16` when they contain risk, open-question, limitation, readiness, coverage, Evidence-ID, claim-label, agent-status, or validator sections.
4. Validate documents `17` through `20` as centralized risk, question, evidence, and coverage mappings.
4. Reject generic descriptions that do not explain real modules, flows, data stores, auth checks, side effects, commands, and source paths.
5. Verify local setup commands, working directories, prerequisites, expected results, URLs, and smoke checks.
6. Verify API routes, methods, auth, request/response shape, validation, side effects, and source handlers.
7. Verify database entities/tables/important fields and their read/write consumers.
8. Verify jobs, realtime events, integrations, configuration, deployment, testing, and operations when present.
9. Verify Vietnamese prose, internal links, secret redaction, and absence of template placeholders.
10. Run deterministic validators and reject publish on any failure.

## Required Validation Artifacts
- `mechanical-validation.md`
- `semantic-validation.md`
- `onboarding-usability-review.md`
- `provenance-scan.md`
- `links-validation.md`
- `secret-scan.md`
- `language-validation.md`
- `source-change-validation.md`
- `final-quality-report.md`
- `final-verdict.md`

## Verdict Contract

```text
Verdict: PASS | REJECT_REQUIRES_REVISION | BLOCKED
Run ID: <run_id>
Source Commit: <source_commit>
Validator Agent: agent-10
Status Gate: PASS | FAIL
Quality Gate: PASS | FAIL
Source Accuracy Gate: PASS | FAIL
Language Gate: PASS | FAIL
Developer Usability Gate: PASS | FAIL
Publish Gate: PASS | FAIL
```

Only `PASS` allows the 20 final documents to be copied to `docs/`.
