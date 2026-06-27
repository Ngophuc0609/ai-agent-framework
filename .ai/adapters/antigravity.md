# Google Antigravity Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` với Google Antigravity IDE/CLI/managed agent.

## Runtime Instructions

- Use generated workspace instructions from `GEMINI.md`, `.agent/rules/00-ai-framework.md`, and `.agents/AGENTS.md` when present.
- Treat `.ai/registry/` as the source of truth for skill and workflow routing.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before terminal commands, workspace edits, browser/MCP calls, or delegated agent actions.
- For Antigravity environments that support mounted `AGENTS.md`, follow the repository root `AGENTS.md` as the cross-tool fallback.
- Inspect runtime state without installing packages; use documented fallbacks unless the selected workflow requires the missing evidence.
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

## Optimization Profile

- Best fit: cost-optimized multi-step documentation, broad discovery, structured synthesis, and Gemini-family model routing.
- Start with deterministic local tools and `Gemini 3.5 Flash (Low/Medium)` for inventory classification; escalate to `Gemini 3.5 Flash (High)` for verification, conflict analysis, and final review.
- Keep `Claude Opus 4.6 Thinking` and `Claude Sonnet 4.6 Thinking` out of Antigravity routing unless a future explicit user decision changes the policy.
- For `source-code-handover`, Agents 1-5 should prioritize complete physical inventory; Agents 6-8 should do deeper source/symbol/build/runtime verification; Agent 9 writes only from frozen evidence; Agent 10 audits independently.
- If Antigravity lacks a native tool required by `.ai/registry/tool-candidates.json`, record the tool limitation and use local fallback commands when available.
