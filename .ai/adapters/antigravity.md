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

## Model Routing For Source Handover

When running `source-code-handover` or `make-new-dev-docs` in Antigravity:

- Use Gemini models only.
- Do not use `Claude Opus 4.6 Thinking`.
- Do not use `Claude Sonnet 4.6 Thinking`.
- Follow `.ai/workflows/make-new-dev-docs-model-routing.md` and `.ai/model-routing/model-routing-matrix.md` for the Antigravity Gemini matrix.
- Prefer `Gemini 3.5 Flash (Medium)` for cost-sensitive discovery and normal findings.
- Prefer `Gemini 3.5 Flash (High)` for Agents 2, 3, 5, 6, 7, 8, 9, and 10.
- Use `Gemini 3.5 Flash (Low)` only for low-risk inventory classification, formatting, and checklist cleanup.
- Use `Gemini 3.1 Pro (High)` only as a Gemini-family fallback for complex review/synthesis when `Gemini 3.5 Flash (High)` is unavailable or underperforms.
- Record the selected model and any downgrade/escalation in `STATUS.md`.
