# .ai Agent Framework

## Vietnamese User Summary

Thư mục `.ai/` là bộ framework dùng chung để điều phối AI agent, skill và workflow cho nhiều công cụ như Codex, Cursor, Claude, Cline hoặc agent nội bộ.

Mục tiêu chính:

- Kích hoạt workflow bằng yêu cầu tự nhiên như `tạo tài liệu` hoặc `tạo api mới`.
- Tách rõ rule, skill, agent, workflow, registry, adapter và runtime state.
- Cho phép thêm skillflow mới mà không phá skill/agent/workflow hiện có.
- Bắt buộc dùng CodeGraph-first, Memory Policy, evidence rule và quality gates cho các workflow đọc source.

## Runtime Policy

All machine-facing instructions in `.ai/` must be written in English.

Vietnamese is allowed only for:

- `Vietnamese User Summary` sections.
- `user_description_vi` metadata.
- `trigger_phrases_vi` values used to match Vietnamese user requests.
- Final chat responses to the Vietnamese-speaking user.

When executing work, agents must think, plan, document internal steps, and write operational instructions in English unless a user explicitly requests Vietnamese output for a deliverable.

## Directory Layout

```text
.ai/
  registry/       # Skill, workflow, trigger, adapter, and tool bootstrap registry.
  rules/          # Shared rules and extension rules.
  skills/         # Superpowers-style skills.
  agents/         # Agent specs.
  workflows/      # Workflow specs.
  adapters/       # Tool-specific execution notes.
  templates/      # Templates for new skills, workflows, agents, and handoff files.
  handoff/        # Shared handoff files for active multi-agent runs.
  runs/           # Runtime state, namespaced by skillflow/run id.
```

## Skill Categories

Skills are grouped by runtime role:

- Primary user-facing skills: active skills that can be selected directly from user intent through `.ai/registry/triggers.yml`.
- Support skills: helper skills used by primary skills or selected directly only when explicit triggers exist.
- Legacy references: long-form guidance files that are loaded only when a skill or workflow references them. They are not standalone skills.

The trigger registry is the routing source of truth. If a user-facing skill should be callable from natural language, add trigger aliases in `.ai/registry/triggers.yml`.

Tool bootstrap commands live in `.ai/registry/tool-bootstrap.json` and are used by `ai-agent-sync` when syncing this framework into another repository.
Optional tool candidates for deep documentation, source evidence, large-repository analysis, and runtime verification live in `.ai/registry/tool-candidates.json`; these are selected by workflows when available and are not installed automatically by default.
Normal task startup checks runtime state but does not install packages. Use `ai-agent-sync --install-tools --yes` only as an explicit bootstrap/maintenance action with runtime-appropriate approval.
Native agent instruction files can be generated from `.ai/` with `ai-agent-adapter-sync`; see `docs/AI_AGENT_ADAPTER_SYNC.md`.

## Add A New Skillflow

1. Read `.ai/rules/11-skillflow-extension-rules.md`.
2. Choose a unique kebab-case `skillflow_id`.
3. Create `.ai/skills/<skillflow_id>/SKILL.md`.
4. Create `.ai/workflows/<skillflow_id>.md`.
5. Create `.ai/agents/<skillflow_id>/` only when the workflow needs dedicated agents.
6. Register the skill, workflow, and triggers in `.ai/registry/`.
7. Use an isolated output namespace.
8. Add quality gates, fallback behavior, memory behavior, and allowed write paths.

## Required Runtime Stack

Preferred for source-reading, documentation, debugging, refactoring, and API-creation workflows:

- MCP Memory
- MCP Filesystem
- MCP Git
- CodeGraph according to the risk matrix, with a documented source-search fallback

Recommended:

- Vector DB/RAG for large repositories
- `docs/PROJECT_CONTEXT.md`
- `docs/FINDINGS.md`
- `docs/DECISIONS.md`

For multi-agent orchestration:

- LangGraph persistence or another agent framework with session memory.

## Important Rules

- Resolve skills and workflows through `.ai/registry/`; do not hard-code triggers.
- Read `.ai/BOOTSTRAP_ONCE.md` only for first-time setup, smoke testing, or an explicit bootstrap request.
- Apply CodeGraph according to task risk; localized work may continue with a documented fallback.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before shell commands, native agent tool calls, delegated agent actions, or source-code-handover runs.
- Retrieve memory before editing or documenting a module.
- Treat current source code as the source of truth when memory conflicts with code.
- Do not store secrets in memory, docs, vectors, or handoff files.
- Do not grant filesystem access outside the active project folder.
- Write runtime state under `.ai/runs/<skillflow_id>/<run_id>/` whenever possible.
- Do not modify unrelated skillflows while adding or updating one skillflow.
