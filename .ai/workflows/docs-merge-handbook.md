# Docs Merge Handbook Workflow

## Vietnamese User Summary

Workflow này tổng hợp nhiều draft, findings hoặc handoff notes thành một handbook cuối nhất quán.

## Skill

Use `.ai/skills/docs-merge-handbook/SKILL.md`.

Load `.ai/skills/skill-docs-merge-to-single-handbook.md` only when expanded legacy merge guidance is needed.

## Inputs

- Agent draft documents.
- Handoff status.
- Open questions.
- Conflicts.
- Decisions.
- Existing final documentation when present.

## Allowed Write Paths

- `docs/`
- `.ai/runs/docs-merge-handbook/<run_id>/`
- `.ai/handoff/`

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

## Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only, not source of truth. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Workflow

1. Resolve the workflow from `.ai/registry/workflows.yml`. Expected key: `docs-merge-handbook`. If missing, record a blocking finding and continue in fallback mode.
2. Retrieve documentation-related memory when available (as supplementary context).
3. Read the assigned draft outputs and handoff files.
4. Identify duplicates, conflicts, missing evidence, and open questions.
5. Prefer evidence-backed findings over unsourced prose.
6. Preserve uncertainty instead of guessing. Do not introduce new claims without evidence.
7. Merge content into a coherent handbook for a new developer.
8. Run final validation (markdown link validation, secret scan, required output check).
9. Check final readiness and list remaining conflicts or open questions.
10. Store confirmed project facts and documentation conventions back to memory when available.
11. Respond to the user in Vietnamese with changed files, readiness, conflicts, and open questions.

## Required Output

The handbook must include relevant sections from this list:

- System overview.
- Setup and runtime.
- Architecture map.
- Database, auth, and API summaries when present.
- Business and frontend flows when present.
- Operations and deployment notes when present.
- Debugging guide.
- Open questions.
- Evidence and limitations.

## Quality Gates

- All included claims are source-backed or clearly marked as inferred/unverified.
- Duplicate and conflicting findings are reconciled or listed as conflicts.
- Missing evidence is not filled in by guesswork.
- Secrets, tokens, private keys, and raw logs are not stored in docs or memory.
- Final readiness is marked as `Ready`, `Partial`, or `Blocked`.

## Fallback Behavior

If required drafts or handoff files are missing, produce a partial handbook from available evidence and list missing inputs as open questions.
