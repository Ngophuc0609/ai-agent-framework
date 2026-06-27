# Cursor Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Cursor.

## Runtime Instructions

- Load `.ai/README.md`, `.ai/registry/triggers.yml`, and only the selected skill/workflow.
- Keep Cursor rules thin; delegate workflow behavior to `.ai/rules/`.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before terminal commands, Composer edits, or agent-mode actions.
- Use the current workspace as the filesystem boundary.
- Prefer source evidence from files, CodeGraph, tests, and git history.
- Write user-facing chat responses in Vietnamese.

## Optimization Profile

- Best fit: interactive code navigation, focused edits, UI/code review, and quick source-to-symbol tracing inside the open workspace.
- Use Cursor Agent/Composer for scoped edits only after file discovery narrows the target set.
- Prefer `rg --files`, symbol search, and IDE references over broad recursive scans.
- For large documentation workflows, write artifacts under `.ai/runs/...` first and publish only after validation passes.
- If the Cursor environment cannot run a required terminal/tool action, record the limitation and produce an explicit manual command instead of pretending verification happened.
- Use `.agents/skills` as a Cursor-supported project skill surface; keep each `SKILL.md` compatible with the Agent Skills standard.
