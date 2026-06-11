---
name: <skill-name>
description: Use when <specific trigger contexts and task scope>
---

# <Skill Name>

## Vietnamese User Summary

<Mô tả ngắn bằng tiếng Việt để người dùng hiểu skill này làm gì.>

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- Add task-specific rules here.

## Memory Policy

Use memory tools only for durable, reusable, verified information.

Before starting, search memory for:

- Existing project facts.
- Previous decisions.
- Known bugs.
- Naming conventions.
- Migration rules.
- Documentation conventions.
- Debugging notes.

During work, store only verified facts, such as:

- Project architecture decisions.
- Important API flows.
- Database table meanings.
- Background job behavior.
- External integration behavior.
- Known bugs and root causes.
- Agreed naming or refactor rules.

Do not store:

- Secrets.
- Access tokens.
- Passwords.
- Private keys.
- Temporary logs.
- Unverified guesses.
- Large raw source code.
- Full stack traces unless summarized.

After each major step, save a short memory summary:

- What was analyzed.
- What was confirmed.
- What remains uncertain.
- Which files prove the finding.

Before editing or documenting a module, retrieve memory for that module first.

If memory conflicts with current source code, trust current source code and update memory.

## Workflow

1. Resolve scope.
2. Run required preflight checks.
3. Retrieve memory when project knowledge is involved.
4. Inspect current source or artifacts.
5. Execute the task.
6. Validate the result.
7. Store confirmed findings back to memory when available.
8. Respond to the user in Vietnamese.

## Guardrails

- Keep writes inside allowed paths.
- Preserve existing project patterns.
- Do not expose secrets.
- Do not fabricate unsupported claims.
- Record limitations and open questions.

## Quality Gates

- [ ] Required rules were applied.
- [ ] Evidence exists for important claims.
- [ ] Memory behavior was logged.
- [ ] Allowed write paths were respected.
- [ ] Validation was run or limitation was recorded.
