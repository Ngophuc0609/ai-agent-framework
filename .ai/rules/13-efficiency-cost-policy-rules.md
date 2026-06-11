# 13 Efficiency And Cost Policy Rules

## Vietnamese User Summary

Rule này giúp giảm chi phí và token: không đọc lại toàn bộ repo mỗi lần, dùng model nhỏ cho bước đơn giản, model mạnh chỉ cho phần khó.

## Core Principle

Minimize token usage and avoid repeated full-repository scans.

Use this flow by default:

```text
User request
  -> Skill Router
  -> Memory Search
  -> Narrow Code/File Search
  -> Small model for classification or preliminary analysis
  -> Strong model only for difficult reasoning
  -> Save verified findings or decisions to memory
  -> Update docs or code
```

## Before Reading Files

1. Search memory for existing project facts.
2. Read `docs/PROJECT_CONTEXT.md` if it exists.
3. Read `docs/FINDINGS.md` and `docs/DECISIONS.md` if relevant.
4. Identify the smallest set of files needed for the current task.

## File Reading Rules

Do not read the whole repository unless explicitly required.

Prefer this order:

1. Entry point files.
2. Routing/controller files.
3. Service/use-case files.
4. Repository/database files.
5. Config files.
6. Tests and logs only when needed.

## Model Usage Rules

Use cheaper or smaller reasoning for:

- File discovery.
- File classification.
- Keyword search.
- Summarization.
- Formatting.
- Checklist generation.
- Simple code edits.
- Simple curl generation.
- Commit message drafting.
- Filename normalization.

Use stronger reasoning only for:

- Complex business logic analysis.
- Difficult debugging.
- Architecture decisions.
- Multi-file refactoring.
- Security-sensitive review.
- Legacy vs new-code comparison.
- Race condition, cache, queue, or background-job analysis.
- Safe migration design.

## Scope Strategy

Use a small model or deterministic tool to find the relevant scope first. Use a stronger model only on that narrowed scope.

## Memory Rules

Store only verified reusable facts:

- Architecture decisions.
- Database meanings.
- API flow summaries.
- Background job behavior.
- Known bugs and root causes.
- Naming conventions.
- Migration rules.

Do not store:

- Secrets.
- Raw source code.
- Temporary logs.
- Unverified guesses.
- Large stack traces.

## Context Compression Rules

After analyzing a module, write a short reusable summary:

- What was analyzed.
- Important files.
- Confirmed behavior.
- Risks.
- What still needs verification.

Reuse this summary in later steps instead of rereading all files.

## Diff-Based Review

For code review before commit:

1. Use git diff first.
2. Read only changed files.
3. Read directly dependent files only when needed.
4. Review logic, security, performance, and tests.
5. Draft the commit message in Vietnamese when requested by the user.

Do not review the whole repository unless the change requires it.

## Large Refactor Strategy

For large refactors:

1. Inventory all usages.
2. Create a checklist.
3. Apply changes in small groups.
4. Test each group.
5. Update memory and docs.

Do not refactor the entire repository in one uncontrolled pass.

## Recommended Project Docs

Each project should maintain:

- `docs/PROJECT_CONTEXT.md`
- `docs/ARCHITECTURE_SUMMARY.md`
- `docs/DATABASE_SUMMARY.md`
- `docs/API_SUMMARY.md`
- `docs/JOBS_SUMMARY.md`
- `docs/DEBUG_PLAYBOOK.md`
- `docs/DECISIONS.md`
- `docs/FINDINGS.md`

## Done Rule

At the end of the task, update memory or project docs with reusable findings so future tasks start faster.

## Cost Optimization Checklist

- [ ] Memory was searched before scanning code.
- [ ] `docs/PROJECT_CONTEXT.md` was read when present.
- [ ] The whole repository was not read for a module-scoped task.
- [ ] File reading was limited to the smallest useful set.
- [ ] Git diff was used when the task involved existing code changes.
- [ ] Findings were summarized for reuse.
- [ ] Durable information was written to memory or docs.
- [ ] Secrets, logs, and large raw code were not stored in memory.
- [ ] Strong models were not used for simple formatting or summarization steps.
