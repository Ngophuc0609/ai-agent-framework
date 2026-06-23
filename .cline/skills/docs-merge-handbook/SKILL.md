---
name: docs-merge-handbook
description: Use when merging multiple documentation drafts, agent findings, handoff notes, or review outputs into one consistent final project handbook
---

<!-- generated-by: ai-agent-adapter-sync -->


# Docs Merge Handbook

## Vietnamese User Summary

Skill này dùng để tổng hợp nhiều draft hoặc findings thành một handbook cuối nhất quán.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/12-memory-policy-rules.md`

## Workflow

1. Retrieve memory for the project documentation namespace.
2. Read all assigned draft documents and handoff files.
3. Identify duplicates, conflicts, missing evidence, and open questions.
4. Prefer source-backed findings over unsourced prose.
5. Merge content into a single handbook with consistent structure.
6. Preserve uncertainty instead of guessing.
7. Write final readiness and open questions.
8. Store confirmed documentation conventions or project facts back to memory when available.
9. Respond to the user in Vietnamese.

## Output

Write to the output paths defined by the selected workflow. Do not overwrite unrelated docs.


## Memory Policy & Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values (connection strings, JWT signing keys, OAuth secrets, API keys, passwords) into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

Each agent finding must include: inspected scope, evidence references, commands executed, findings, assumptions, open questions, risks, and completion state.

## Final Validation

Before publishing final docs or committing changes, run required-output validation, STATUS.md consistency validation, git diff --check, secret scan, markdown/link validation, and stack-appropriate build or test commands when environment permits.
