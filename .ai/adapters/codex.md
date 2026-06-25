# Codex Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Codex.

## Runtime Instructions

- Read `.ai/README.md` first.
- Resolve the request through `.ai/registry/triggers.yml`.
- Load only the matching skill and workflow.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before shell commands, tool calls, or multi-agent workflow execution.
- Use CodeGraph before source-code investigation when available.
- Use MCP Memory, MCP Filesystem, and MCP Git when available.
- Keep filesystem access scoped to the current project.
- Write runtime artifacts under `.ai/runs/<skillflow_id>/<run_id>/` unless the workflow explicitly allows another path.
- For workflows that list agents, execute the agent specs exactly:
  - Use delegated sub-agents only when the user explicitly requested multi-agent/delegated/parallel work and the Codex runtime exposes sub-agent tools.
  - Otherwise run the agents sequentially in the current session.
  - Preserve agent output boundaries and write each required agent output before final synthesis.
  - Record the execution mode in `.ai/handoff/STATUS.md` or `.ai/runs/<skillflow_id>/<run_id>/handoff/STATUS.md`.
- Respond to the user in Vietnamese for chat messages.

## Optimization Profile

- Best fit: source editing, deterministic shell validation, git diff review, framework maintenance, and controlled commit/push delivery.
- Use `rg`, `git`, repository scripts, and focused file reads before model reasoning.
- Prefer one explicit shell command per action; avoid long chained commands except for short validation pipelines.
- For `source-code-handover`, initialize with `.ai/scripts/init-source-code-handover-run.sh` and preserve agent output boundaries even when running agents sequentially in one Codex session.
- Use available sub-agent tools only when the runtime exposes them; otherwise record `single-runtime-sequential-fallback`.
- Do not use memory-derived facts as current evidence without rechecking source files when the claim affects documentation quality, migration, security, or production readiness.
