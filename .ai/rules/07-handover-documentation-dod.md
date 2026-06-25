# Documentation Definition of Done (DoD)

Every agent participating in the Source Code Handover workflow MUST follow this standard.

## 0. Mandatory Quality Checklist

Every final document MUST also comply with `.ai/rules/08-source-code-handover-quality-checklist.md`.
If front matter, common sections, Evidence Index, coverage manifest, negative evidence, or forbidden-content checks are missing or invalid, Agent 10 MUST return `REJECT_REQUIRES_REVISION` or `BLOCKED`, never `PASS`.

## 1. General Rule: Every Claim Needs Evidence
- Status: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, `[DECISION]`
- Every `[CONFIRMED]` claim MUST have an Evidence ID.
- Every `[DECISION]` item MUST include the decision owner or required owner confirmation.

## 2. Target Document Set (20 lowercase files with numeric prefixes)
- `01_project_handover_full.md`
- `02_project_context.md`
- `03_repository_guide.md`
- `04_local_setup.md`
- `05_configuration_reference.md`
- `06_architecture.md`
- `07_database_reference.md`
- `08_auth_and_security.md`
- `09_api_catalog.md`
- `10_background_jobs.md`
- `11_realtime_signalr_socket.md`
- `12_external_integrations.md`
- `13_frontend_guide.md`
- `14_operations_runbook.md`
- `15_deployment_and_cicd.md`
- `16_testing_guide.md`
- `17_known_risks.md`
- `18_open_questions.md`
- `19_evidence_index.md`
- `20_documentation_coverage.md`

## 3. Mandatory Coverage Rule
Coverage math denominator MUST come from Phase 0 inventory.
`accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`

## 4. Documentation Coverage Manifest (20_documentation_coverage.md)
Must use structural tables grouping by domain (Repository, Database, API, Background Jobs, Realtime) listing: `discovered`, `documented`, `accounted`, `unresolved`, `status`, `gaps`.

## 5. Negative Evidence Rule
`[NOT_APPLICABLE]` is ONLY valid when documented with: Component/scope, source roots, search patterns, tools used, results, impact, and negative evidence ID. It cannot be used if status is `scan_failed` or `tool_unavailable`.

## 6. Standardized Evidence Index
`19_evidence_index.md` MUST contain table:
`Evidence ID | Topic | Claim | Source Path | Line/Method | Verification Type | Source Commit | Status`
Valid ID patterns: `EV-REPO-###`, `EV-CONFIG-###`, `EV-DB-###`, `EV-MIGRATION-###`, `EV-AUTH-###`, `EV-API-###`, `EV-JOB-###`, `EV-RT-###`, `EV-OPS-###`, `EV-TEST-###`, `EV-CICD-###`, `EV-NEG-###`.
