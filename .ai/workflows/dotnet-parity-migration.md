# .NET Parity Migration

## Vietnamese User Summary

Workflow này migrate .NET legacy sang .NET 8+ bằng baseline, compatibility port và contract regression.

## Purpose

Migrate .NET legacy systems to .NET 8+ while preserving 1:1 external behavior.

## Trigger

Registered in:

- `.ai/registry/triggers.yml`

## Required Files

- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`
- `.ai/skills/dotnet-parity-migration/SKILL.md`
- `.ai/skills/dotnet-baseline-capture/SKILL.md`
- `.ai/skills/dotnet-compatibility-port/SKILL.md`
- `.ai/skills/dotnet-contract-regression/SKILL.md`
- `.ai/rules/16-dotnet-parity-migration-rules.md`
- `.ai/templates/dotnet-parity-migration/`

## Allowed Write Paths

- `.ai/runs/dotnet-parity-migration/<run_id>/`
- `docs/dotnet-parity-migration/`
- `docs/migration/`
- Test projects or snapshot fixture folders in the target repository when they already exist or are explicitly created for migration regression.
- Source files needed for the scoped migration slice when the current phase is compatibility porting.

Do not write directly to production configuration, deployment secrets, or unrelated modernization docs.

## Output Namespace

Runtime state should use:

```text
.ai/runs/dotnet-parity-migration/<run_id>/
```

Recommended subdirectories:

```text
baseline/
contracts/
golden-master/
regression/
risks/
validation/
```

## Execution

1. Resolve the requested phase:
   - baseline capture.
   - compatibility port.
   - contract regression.
   - full parity migration.
2. Check git status.
3. Inspect runtime state using safe local checks. Do not install SDKs, packages, or tools automatically.
4. Retrieve project memory when available. If memory is unavailable, use repository docs fallback and record the limitation.
5. Attempt CodeGraph for broad source inventory or dependency tracing. For localized endpoint work, use `rg`, IDE/LSP references, and narrow source reads when CodeGraph is unavailable.
6. Identify the target app type and target slice.
7. If baseline is missing, stop porting and run `dotnet-baseline-capture`.
8. If baseline conflicts, record the conflict and ask for clarification or runtime evidence.
9. Design compatibility adapters before editing production code.
10. Port only the smallest framework-incompatible slice.
11. Add or update Golden Master regression coverage when feasible.
12. Run build, tests, and contract comparison.
13. Classify every difference as `MATCH`, `DYNAMIC_MATCH`, `APPROVED_BREAKING_CHANGE`, `MIGRATION_BUG`, or `BLOCKED`.
14. Report readiness per endpoint or view.

## Phase Prompts

### Baseline Capture

Use when the user asks to create a legacy baseline, capture Golden Master behavior, or prepare before migration. Do not edit source code. Do not call production write endpoints.

### Compatibility Port

Use when the baseline exists and the user asks to port an endpoint, view, or code slice to .NET 8+. Read the relevant baseline before editing.

### Contract Regression

Use after porting to compare .NET 8+ output with legacy Golden Master snapshots. Do not mark done while unapproved migration bugs remain.

## Quality Gates

- [ ] Skill, workflow, and trigger were resolved through `.ai/registry/`.
- [ ] `.ai/rules/16-dotnet-parity-migration-rules.md` was applied.
- [ ] Legacy baseline exists or the task is explicitly `BLOCKED`.
- [ ] P0/P1 endpoints or views have Golden Master evidence before porting.
- [ ] Compatibility risks were listed before source edits.
- [ ] No business rule refactor or unapproved contract change was introduced.
- [ ] Build/test/regression commands were run or explicitly blocked with reason.
- [ ] All differences were classified.
- [ ] Secrets were not exposed.
- [ ] Runtime limitations and fallback evidence were recorded.

## Fallback Behavior

- Missing CodeGraph: use `rg`, project references, route maps, and narrowed source reads; mark confidence reduced for broad inventory.
- Missing runtime legacy environment: create `CODE_VERIFIED` baseline only and mark runtime snapshots `BLOCKED`.
- Missing test project: create executable curl/Postman/snapshot assets or documented manual Golden Master cases.
- Missing memory: use repository docs fallback and do not claim memory was read or written.

## Final Response Contract

Report:

```text
Status: PASS / FAIL / BLOCKED / PARTIAL
Endpoint/View:
Legacy evidence:
Changes made:
Compatibility risks:
Contract differences:
Tests run:
Fallbacks/limitations:
Next required action:
```
