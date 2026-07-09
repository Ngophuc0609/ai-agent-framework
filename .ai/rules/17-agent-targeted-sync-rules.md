# Agent-Targeted Sync Rules

## Purpose

Prevent duplicated or conflicting instruction, rule, skill, and workflow context when syncing this framework for one AI agent host.

## Source Of Truth

`.ai/` remains the canonical authoring source. Native files are generated adapters and must stay compact unless a restricted runtime explicitly requires a materialized bundle.

## Targeted Sync Rules

1. Generate only the selected agent's verified native surfaces by default.
2. Do not generate portable fallback surfaces for a selected agent unless the sync command explicitly requests `portable` or `legacy-all` profile output.
3. Do not place the same skill body in two directories that the same agent host is likely to auto-discover.
4. Keep always-on native files pointer-only and under the pointer size budget.
5. Load `.ai/` rules, workflows, and skills progressively from the selected skill/workflow, not as an eager bundle.
6. Treat unverified agent-specific directories as fallback-only and label them clearly in docs and generated manifests.
7. Prefer path-scoped or on-demand native rule systems over always-on duplicated rule files.
8. If official documentation is missing or ambiguous, use the smallest safe native entrypoint and record the mapping as `[INFERRED]` or fallback-only.
9. For Antigravity latest CLI (`agy`), treat `.agents/skills/<skill>/SKILL.md` as a verified native project skill surface based on the current runtime note supplied for this framework.

## Default Isolated Surface Matrix

| Agent | Verified default surfaces | Skill surface | Fallback surfaces |
|---|---|---|---|
| Codex | `AGENTS.md` | `.agents/skills/<skill>/SKILL.md` | None |
| Claude Code | `CLAUDE.md` | `.claude/skills/<skill>/SKILL.md` | `.claude/rules/*` only when deep rules are requested |
| Cline | `.clinerules/00-ai-framework.md` | `.cline/skills/<skill>/SKILL.md` | `AGENTS.md` fallback disabled by default |
| Cursor | `.cursor/rules/00-ai-framework.mdc` | No verified native project skill output by default | `.agents/skills` only in portable/legacy profiles |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/ai-framework.instructions.md` | `.github/skills/<skill>/SKILL.md` | `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` alternatives disabled by default |
| Antigravity | `GEMINI.md` | `.agents/skills/<skill>/SKILL.md` | `.agent/rules`, `.agents/AGENTS.md` only in portable/legacy profiles |
| Portable Agent Skills | `AGENTS.md` | `.agents/skills/<skill>/SKILL.md` | Used only when the user selects the generic `agents` target |

## Profiles

- `isolated`: default. Generate only verified native surfaces for the requested agent.
- `portable`: generate verified native surfaces plus explicitly labeled portable fallback surfaces.
- `legacy-all`: reproduce the broad historical output for repositories that intentionally support multiple agent hosts from one sync.

## Acceptance

Agent-targeted sync is acceptable only when:

- A single-agent shortcut such as `ai-agent-sync agy` does not create unrelated rule entrypoints.
- Antigravity shortcut output must create `.agents/skills` because Antigravity CLI latest project skills are native there.
- Generated manifests record the selected profile.
- Any fallback-only output is opt-in.
- Documentation explains whether `.ai/` is canonical source, native adapter output, or fallback.
