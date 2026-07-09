# Deferred Issues Report

Use this file as `15_DEFERRED_ISSUES_REPORT.md` during parity migration.

Do not fix these issues during the 1:1 parity phase unless the user explicitly approves a separate breaking/fix phase.

| ID | Category | Location | Description | Risk | Evidence | Suggested Fix Later | Fix Now? |
|---|---|---|---|---|---|---|---|
| DEF-001 | Security | AuthController.Login | Hard-coded key | High | file/method/line | Move to secret store in modernization phase | No |

