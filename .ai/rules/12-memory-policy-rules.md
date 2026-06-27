# 12 Memory Policy Rules

## Summary

Use memory only for durable, verified, project-namespaced facts. Runtime inspection and package installation are separate actions.

## Required Flow

For source reading, documentation, debugging, refactoring, and API creation:

1. Check Memory runtime state using safe local inspection.
2. Retrieve project memory when available; otherwise activate the repository-document fallback.
3. Scan current source and compare it with remembered facts.
4. Trust current source when it conflicts with memory.
5. Store only confirmed, durable findings when memory writes are available.

## Runtime Check Versus Installation

Safe checks may verify:

- `.ai/runtime/memory/memory.jsonl`
- `.ai/runtime/mcp-servers.json`
- configured MCP server availability

Do not run `ai-agent-sync --install-tools --yes`, a package manager, or a network installer during normal startup. Installation is an explicit bootstrap/maintenance action and must follow the active runtime's approval policy.

If Memory is unavailable, continue with repository documents when the selected workflow permits it. Record the limitation, do not claim a memory read/write, and lower confidence/readiness when missing memory materially affects the task.

## Retrieval And Storage

Retrieve relevant architecture decisions, known bugs, naming conventions, migration rules, and documentation conventions before deep source work when Memory is available.

Store only verified summaries with evidence paths. Never store secrets, credentials, private keys, raw source dumps, temporary logs, unverified guesses, or full stack traces.

Use a stable project namespace such as:

```text
project:<repo-name>:facts
project:<repo-name>:debug-findings
project:<repo-name>:migration-decisions
```

## Repository Fallback

When MCP Memory is unavailable:

1. Record the limitation in run status and the final response.
2. Use `docs/PROJECT_CONTEXT.md`, `docs/FINDINGS.md`, and `docs/DECISIONS.md` when present.
3. Do not pretend Memory was read or written.
4. Keep the fallback inside the active repository and apply the same secret-safety rules.

## Preferred Stack

- MCP Memory, MCP Filesystem, and MCP Git when available.
- CodeGraph according to `.ai/rules/10-codegraph-first-rules.md`.
- LangGraph persistence or equivalent only when a multi-agent workflow requires durable orchestration state.
