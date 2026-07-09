# Migration Risk Register

| Risk ID | Category | Description | Impact | Probability | Evidence | Mitigation | Owner | Status | Blocking |
|---|---|---|---|---|---|---|---|---|---|
| RISK-001 | JSON | JSON shape/casing/null/date differs after migration | Critical | High | | Configure serializer and snapshot test | | Open | Yes |
| RISK-002 | Request Binding | Request.Params behavior not preserved | Critical | High | | LegacyRequestParams adapter | | Open | Yes |
| RISK-003 | Auth | FormsAuth/Cookie auth behavior changes | Critical | High | | Auth/cookie compatibility plan | | Open | Yes |
| RISK-004 | Session | Session key/type/TTL changes | Critical | Medium | | Session contract + serializer | | Open | Yes |
| RISK-005 | Crypto | Old tokens/deep links fail on .NET 8+ | Critical | Medium | | Crypto test vectors | | Open | Yes |
| RISK-006 | View | HTML/static path/script order changes | High | Medium | | View Golden Master | | Open | Yes |
| RISK-007 | Side Effect | DB/external API side effects differ | Critical | Medium | | Side-effect matrix | | Open | Yes |
| RISK-008 | Test Source | Tests generated from migrated output instead of legacy baseline | Critical | Medium | | Require `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md` before porting | | Open | Yes |
| RISK-009 | Legacy Bug Fix | Agent fixes latent legacy bug during parity | High | Medium | | Record in `15_DEFERRED_ISSUES_REPORT.md`, do not fix in parity | | Open | Yes |
