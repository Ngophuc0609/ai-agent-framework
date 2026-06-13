# Legacy Reference: Merge Docs To Single Handbook

## Reference Status

This file is a legacy reference only. Do not register it as a standalone skill or workflow.

The active workflow path is `.ai/workflows/docs-merge-handbook.md`. Load this file only when that workflow or `.ai/skills/docs-merge-handbook/SKILL.md` needs expanded merge guidance.

## Vietnamese User Summary

File này là reference legacy cho skill tổng hợp handbook cuối.

## Purpose

Use this reference when the selected workflow needs a detailed merge process beyond `.ai/skills/docs-merge-handbook/SKILL.md`.

## Inputs

- Agent draft documents.
- Handoff status.
- Open questions.
- Conflicts.
- Decisions.
- Existing final documentation when present.

## Process

1. Retrieve documentation-related memory.
2. Read all draft outputs.
3. Identify duplicates and conflicts.
4. Prefer evidence-backed claims.
5. Preserve uncertainty and open questions.
6. Merge into a coherent single handbook.
7. Check that the handbook is useful for a new developer.
8. Store confirmed project facts and documentation conventions back to memory when available.

## Required Output

The handbook must include:

- System overview.
- Setup and runtime.
- Architecture map.
- Database/auth/API summaries when present.
- Business and frontend flows when present.
- Operations and deployment notes when present.
- Debugging guide.
- Open questions.
- Evidence and limitations.

## Final Response

Respond to the user in Vietnamese with changed files, readiness, conflicts, and open questions.
