# Documentation Definition of Done (DoD)

Mọi agent tham gia quá trình Handover phải tuân thủ nghiêm ngặt chuẩn này.

## 1. Quy tắc chung: mỗi claim phải có Evidence
- Status: Confirmed | Inferred | Unverified | Conflict | Not Applicable
- Every `[CONFIRMED]` claim requires an Evidence ID (e.g., EV-DB-001).

## 2. Bộ tài liệu mục tiêu
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
`accounted = documented + unresolved + not applicable with negative evidence + excluded with explicit reason`

## 4. Documentation Coverage Manifest (20_documentation_coverage.md)
Must use structural tables calculating `accounted` components versus `discovered` components from Phase 0 Inventory.

## 5. Negative Evidence Rule
`[NOT_APPLICABLE]` must include search roots, commands executed, results, and negative evidence IDs.
