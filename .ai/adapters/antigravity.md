# Google Antigravity Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` với Google Antigravity IDE/CLI/managed agent.

## Runtime Instructions

- Use generated workspace instructions from `GEMINI.md`, `.agent/rules/00-ai-framework.md`, and `.agents/AGENTS.md` when present.
- Treat `.ai/registry/` as the source of truth for skill and workflow routing.
- For Antigravity environments that support mounted `AGENTS.md`, follow the repository root `AGENTS.md` as the cross-tool fallback.
- Run or verify `ai-agent-sync --install-tools --yes` before source-reading or code-changing tasks when runtime state is missing.
- Keep filesystem and external tool access scoped to the active workspace.
- Do not expose secrets in generated instructions, memory, artifacts, or chat responses.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.
