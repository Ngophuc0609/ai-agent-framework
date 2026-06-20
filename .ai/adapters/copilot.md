# GitHub Copilot Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` với GitHub Copilot Chat, Copilot code review và Copilot coding agent.

## Runtime Instructions

- Use generated repository instructions from `.github/copilot-instructions.md` when present.
- Use generated path-specific instructions from `.github/instructions/ai-framework.instructions.md` when present.
- Treat `.ai/registry/` as the source of truth for skill and workflow routing.
- For Copilot coding agents that support `AGENTS.md`, also follow the repository root `AGENTS.md`.
- Run or verify `ai-agent-sync --install-tools --yes` before source-reading or code-changing tasks when runtime state is missing.
- Keep secrets out of generated instructions, chat responses, docs, memory, and pull request comments.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.
