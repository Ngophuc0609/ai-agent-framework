# 12 Memory Policy Rules

## Vietnamese User Summary

Rule này quy định cách dùng memory: chỉ lưu thông tin bền vững, đã xác minh, có namespace theo project, không bao giờ lưu secret.

## Core Policy

Use memory tools only for durable, reusable, verified information.

Do not use memory as a temporary log, source-code cache, secret store, or place for unverified guesses.

## Required Flow

For source reading, documentation, debugging, refactoring, and API creation:

1. Retrieve memory.
2. Scan current source code.
3. Compare memory with code.
4. Use code as the source of truth.
5. Write or update docs/code.
6. Store confirmed findings back to memory.

## Before Starting

Search memory for:

- Existing project facts.
- Previous decisions.
- Known bugs.
- Naming conventions.
- Migration rules.
- Documentation conventions.
- Debugging notes.

## During Work

Store only verified facts, such as:

- Project architecture decisions.
- Important API flows.
- Database table meanings.
- Background job behavior.
- External integration behavior.
- Known bugs and root causes.
- Agreed naming or refactor rules.

Do not store:

- Secrets.
- Access tokens.
- Passwords.
- Private keys.
- Temporary logs.
- Unverified guesses.
- Large raw source code.
- Full stack traces unless summarized.

## After Each Major Step

Save a short memory summary containing:

- What was analyzed.
- What was confirmed.
- What remains uncertain.
- Which files prove the finding.

## Retrieval Rule

Before editing or documenting a module, retrieve memory for that project namespace and module first.

## Conflict Rule

If memory conflicts with current source code, trust current source code and update memory.

## Security Rules

- Do not store secrets in memory.
- Do not grant filesystem access to the whole drive.
- Allow only the active project folder.
- Log every memory write.
- Provide a review/delete mechanism for incorrect memory.
- Memory must use a project namespace.

## Required Stack

Required:

- MCP Memory.
- MCP Filesystem.
- MCP Git.

Recommended:

- Vector DB/RAG for large repositories.
- `docs/PROJECT_CONTEXT.md` for repo summary.
- `docs/FINDINGS.md` for agent findings.
- `docs/DECISIONS.md` for technical decisions.

For multi-agent systems:

- LangGraph persistence or another agent framework with session memory.

## Namespace Format

Memory keys or namespaces must include a stable project namespace, for example:

```text
project:<repo-name>:facts
project:<repo-name>:debug-findings
project:<repo-name>:migration-decisions
```

If the project name is unknown, infer it from the repository folder and verify it against source or manifest files.

## Fallback

If MCP Memory is unavailable:

1. Record the limitation in run status and final response.
2. Use repo-local docs as fallback:
   - `docs/PROJECT_CONTEXT.md`
   - `docs/FINDINGS.md`
   - `docs/DECISIONS.md`
3. Do not pretend that MCP Memory was written.
