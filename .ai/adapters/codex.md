# Codex Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Codex.

## Runtime Instructions

- Read `.ai/README.md` first.
- Resolve the request through `.ai/registry/triggers.yml`.
- Load only the matching skill and workflow.
- Use CodeGraph before source-code investigation when available.
- Use MCP Memory, MCP Filesystem, and MCP Git when available.
- Keep filesystem access scoped to the current project.
- Write runtime artifacts under `.ai/runs/<skillflow_id>/<run_id>/` unless the workflow explicitly allows another path.
- Respond to the user in Vietnamese for chat messages.
