# Skill Pack Review & Update Report

## 1. Files reviewed

| File | Type | Status Before | Status After | Notes |
|---|---|---|---|---|
| `.ai/rules/16-dotnet-parity-migration-rules.md` | Canonical rule | Partial parity guardrails | Updated | Added R-00 through R-12, phase 0 through 9, required deliverables, unit statuses, acceptance statuses, Request.Params and JSON string/raw guardrails. |
| `.ai/workflows/dotnet-parity-migration.md` | Canonical workflow | Baseline/test-first existed but deliverables and phase order were incomplete | Updated | Enforces baseline -> legacy-derived test spec -> new base -> test scaffold -> one-slice conversion -> regression -> deferred issues. |
| `.ai/skills/dotnet-parity-migration/SKILL.md` | Canonical skill | Coordinated parity migration but did not list all required deliverables/statuses | Updated | Added full deliverable set, migration unit statuses, and PASS/FAIL/BLOCKED/PARTIAL/DEFERRED output. |
| `.ai/skills/dotnet-baseline-capture/SKILL.md` | Canonical skill | Strong evidence rules existed, but artifact names and test-spec requirement were incomplete | Updated | Added current deliverable mapping, baseline-first test spec, auth/session/cookie contract, and view/UI/static contract. |
| `.ai/skills/dotnet-compatibility-port/SKILL.md` | Canonical skill | Minimal port guardrails existed | Updated | Added hard block when baseline/tests are missing; strengthened Request.Params, JSON result, auth/session, and deferred issue rules. |
| `.ai/skills/dotnet-contract-regression/SKILL.md` | Canonical skill | Compared contracts but lacked explicit dynamic masking and full acceptance status set | Updated | Added legacy-baseline-only comparison, JSON/view checks, dynamic masking rules, and final status mapping. |
| `.ai/templates/dotnet-parity-migration/*` | Templates/schema | Templates existed for baseline, tests, risk, acceptance | Updated | Added deferred issues template; updated checklist, risk register, and baseline schema with deliverables and migration unit statuses. |
| `bin/ai-agent-adapter-sync` | Adapter generator | Native headers were pointer-only without compact .NET migration guardrails | Updated | Added concise .NET parity guardrails to generated AGENTS/CLAUDE/Copilot/Cline/Cursor/Antigravity headers. |
| `README.md` | User guide | Sync/install guidance only | Updated | Added .NET 1:1 parity migration usage flow, skills, deliverables, and BLOCKED rule. |
| Generated native files | Agent outputs | Out of date after canonical changes | Updated | Regenerated Codex, Claude, Cline, Copilot, Cursor, and Antigravity outputs from `.ai`. |

## 2. Rules applied

| Rule | Applied? | Files Updated | Notes |
|---|---|---|---|
| R-00 1:1 parity by default | Yes | Rule, workflow, parity skill, generated headers, README | Migration is explicitly not modernization/refactor. |
| R-01 No conversion without baseline | Yes | Rule, workflow, baseline skill, port skill | Missing evidence becomes `BLOCKED: Missing legacy baseline/runtime evidence`. |
| R-02 Tests from legacy baseline first | Yes | Rule, workflow, parity skill, baseline skill, checklist, README | `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md` is required before accepting migrated behavior. |
| R-03 One endpoint/view/business flow at a time | Yes | Rule, workflow, parity skill, schema, checklist | Added migration unit statuses. |
| R-04 Minimal .NET port only | Yes | Rule, parity skill, port skill | Business refactor, DTO cleanup, validation changes, query optimizations, and bug fixes are prohibited in parity. |
| R-05 Request.Params compatibility | Yes | Rule, port skill, checklist, generated headers | Method-based mapping is prohibited. |
| R-06 JSON string/raw verification | Yes | Rule, port skill, checklist, regression skill, generated headers | Golden Master decides raw JSON object vs escaped JSON string. |
| R-07 Auth/session/cookie contract | Yes | Rule, baseline skill, port skill | Added full cookie/auth/session inventory and load-balancer note. |
| R-08 View/UI/static assets are contract | Yes | Rule, baseline skill, regression skill | Added rendered HTML, form, script/CSS, static asset, React root, and refresh behavior checks. |
| R-09 Deferred legacy issues | Yes | Rule, workflow, parity skill, port skill, template, README | Issues go to `15_DEFERRED_ISSUES_REPORT.md`; no fix during parity without approval. |
| R-10 Acceptance statuses | Yes | Rule, workflow, parity skill, regression skill, checklist | Standardized PASS/FAIL/BLOCKED/PARTIAL/DEFERRED. |
| R-11 Required deliverables | Yes | Rule, workflow, parity skill, baseline skill, schema, README | Added all required migration-docs files and `legacy-baseline.json`. |
| R-12 AI accelerates but cannot guess evidence | Yes | Rule, baseline skill, workflow, generated headers, README | Missing evidence is blocked; response shapes cannot be invented. |

## 3. Contradictions fixed

| Issue | Old instruction | New instruction | File |
|---|---|---|---|
| Build/app-start treated as enough by omission | Build/test/regression existed, but native headers did not state migration acceptance limits | Build pass is not enough; PASS requires regression against legacy baseline | `.ai/rules/16-dotnet-parity-migration-rules.md`, generated headers |
| Missing baseline fallback unclear in port phase | Port skill allowed plans/scaffolds but did not explicitly block missing pre-edit checks | Missing baseline/tests blocks production business logic conversion | `.ai/skills/dotnet-compatibility-port/SKILL.md` |
| Static endpoint discovery could become shallow docs | Baseline skill warned against empty templates but artifact set did not require legacy-derived test spec | Baseline must include manual source trace, concrete response schema, and legacy-derived test spec | `.ai/skills/dotnet-baseline-capture/SKILL.md` |
| Request.Params shortcut risk | Existing docs warned against replacing with only form/query | Explicitly prohibits `POST -> Request.Form` and `GET -> Request.Query`; requires compatibility precedence evidence | `.ai/rules/16-dotnet-parity-migration-rules.md`, `.ai/skills/dotnet-compatibility-port/SKILL.md` |
| JSON shortcut risk | Existing docs warned against raw/escaped drift | Explicitly prohibits mechanical `Json(responseString)` -> `Content(...)`; requires Golden Master | `.ai/rules/16-dotnet-parity-migration-rules.md`, `.ai/skills/dotnet-compatibility-port/SKILL.md` |
| Legacy bug fixing during parity | Existing docs said do not fix latent bugs but report path varied | Standardized to `15_DEFERRED_ISSUES_REPORT.md` | Rule, workflow, parity/port skills, deferred template |

## 4. Remaining gaps

| Gap | Impact | Recommendation | Blocking? |
|---|---|---|---|
| No `prompts/` or top-level `templates/` directory detected in this repo | Nothing to update there | Keep canonical prompt behavior in `.ai` skills/workflow/templates | No |
| `AGENTS.md`, `CLAUDE.md`, Copilot, Cline, Cursor, and Antigravity files are generated pointer files | They contain compact guardrails, not the full R-00 to R-12 policy copy | Continue treating `.ai/` as source of truth and run `ai-agent-adapter-sync` after framework edits | No |
| Runtime migration projects are not present in this repo | Could not verify real legacy baseline outputs or migrated .NET tests | Apply the updated skill pack inside a target migration repo and collect evidence there | No |

## 5. Final acceptance

PASS: Skill pack instructions, workflow, templates, schema, README, and generated native agent files now enforce the requested .NET 1:1 parity migration flow.
