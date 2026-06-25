# GitHub Copilot Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` với GitHub Copilot Chat, Copilot code review và Copilot coding agent.

## Runtime Instructions

- Use generated repository instructions from `.github/copilot-instructions.md` when present.
- Use generated path-specific instructions from `.github/instructions/ai-framework.instructions.md` when present.
- Treat `.ai/registry/` as the source of truth for skill and workflow routing.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before workspace edits, terminal suggestions, pull request comments, or coding-agent actions.
- For Copilot coding agents that support `AGENTS.md`, also follow the repository root `AGENTS.md`.
- Run or verify `ai-agent-sync --install-tools --yes` before source-reading or code-changing tasks when runtime state is missing.
- Keep secrets out of generated instructions, chat responses, docs, memory, and pull request comments.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## Optimization Profile

- Best fit: inline coding help, pull request review, CI-aware suggestions, GitHub issue/PR context, and small scoped edits.
- Use `.github/instructions/ai-framework.instructions.md` as the deep framework bundle for Copilot contexts that support path-specific instructions.
- For broad documentation or multi-agent workflows, Copilot should create or update artifacts but must not claim build/test/runtime verification unless it has real command or CI evidence.
- Prefer GitHub-native evidence when available: commit, PR, workflow run, code scanning, Dependabot, and issue links.
- Do not expose secrets in PR comments or generated docs; redact values while preserving key names.
