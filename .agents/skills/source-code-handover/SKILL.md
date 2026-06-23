---
name: source-code-handover
description: Use when creating source-code handover documentation, onboarding documentation for new developers, architecture summaries, repository maps, setup guides, API/database/auth documentation, or final project handbooks from source code
---

<!-- generated-by: ai-agent-adapter-sync -->


# Source Code Handover

## Vietnamese User Summary

Skill này dùng để tạo tài liệu bàn giao source code cho developer mới.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/01-documentation-skill.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`

## Main Workflow

Use `.ai/workflows/make-new-dev-docs.md`.

Use `.ai/workflows/make-new-dev-docs-model-routing.md` when the request includes cost, balanced, high-accuracy, or model-routing intent.

Detailed legacy reference is available at `.ai/skills/skill-source-code-handover-docs.md`. Load it only when the selected workflow needs the expanded agent checklist.

## Memory Policy

Before starting, retrieve memory for project facts, prior decisions, known bugs, naming conventions, migration rules, documentation conventions, and debugging notes.

During work, store only verified facts such as architecture decisions, API flows, database table meanings, background job behavior, external integration behavior, known bugs with root causes, and agreed naming/refactor rules.

Do not store secrets, tokens, passwords, private keys, temporary logs, unverified guesses, large raw source code, or full stack traces.

After each major step, save a short memory summary with what was analyzed, what was confirmed, what remains uncertain, and which files prove the finding.

Before editing or documenting a module, retrieve memory for that module first.

If memory conflicts with current source code, trust current source code and update memory.

## Execution Summary

1. Resolve the workflow through the registry.
2. Run CodeGraph preflight.
3. Retrieve project memory.
4. Run assigned agents or sequential fallback.
5. Produce evidence-backed docs only.
6. Review conflicts and open questions.
7. Generate final handbook when requested by the workflow.
8. Store confirmed findings back to memory when available.
9. Respond to the user in Vietnamese.
