---
name: using-superpowers
description: Use when applying the Superpowers methodology for discovering, reading, and following skills before executing a task
---

<!-- generated-by: ai-agent-adapter-sync -->


# Using Superpowers

## Vietnamese User Summary

Skill này là chuẩn nền để agent luôn kiểm tra, đọc và dùng đúng skill trước khi làm việc.

## Superpowers Method

1. Check whether the user's request matches any available skill.
2. Read the selected skill before taking action.
3. Follow the skill's workflow and required rules.
4. Load referenced files only when needed.
5. Keep context small and evidence-driven.
6. If no skill applies, proceed with general rules and record the gap when useful.

## Skill Usage Rules

- Do not skip an applicable skill.
- Do not invent skill behavior that is not in the skill file.
- Do not create a separate `superpower` capability module.
- Treat skills as reusable operational instructions.
- Prefer concise `SKILL.md` files with directly linked references.

## Language

- Use English for execution instructions and artifacts unless the deliverable explicitly requires Vietnamese.
- Use Vietnamese for chat responses to the user.
