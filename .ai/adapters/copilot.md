# GitHub Copilot Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` với GitHub Copilot Chat, Copilot code review và Copilot coding agent.

## Runtime Instructions

- Use generated repository instructions from `.github/copilot-instructions.md` when present.
- Use generated path-specific instructions from `.github/instructions/ai-framework.instructions.md` when present.
- Treat `.ai/registry/` as the source of truth for skill and workflow routing.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before workspace edits, terminal suggestions, pull request comments, or coding-agent actions.
- In isolated Copilot sync, do not require a root `AGENTS.md`; use Copilot's `.github` instruction and skill surfaces. Treat root `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` as alternative/fallback instruction surfaces only when they were intentionally generated.
- Inspect runtime state without installing packages; use repository-document fallbacks and record limitations when optional tools are missing.
- Keep secrets out of generated instructions, chat responses, docs, memory, and pull request comments.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## Optimization Profile

- Best fit: inline coding help, pull request review, CI-aware suggestions, GitHub issue/PR context, and small scoped edits.
- Use `.github/instructions/ai-framework.instructions.md` as a scoped pointer to current framework policy.
- For broad documentation or multi-agent workflows, Copilot should create or update artifacts but must not claim build/test/runtime verification unless it has real command or CI evidence.
- Prefer GitHub-native evidence when available: commit, PR, workflow run, code scanning, Dependabot, and issue links.
- Do not expose secrets in PR comments or generated docs; redact values while preserving key names.
