# 03 Safety Rules

## Vietnamese User Summary

Rule này bảo vệ secret, giới hạn quyền filesystem và tránh ghi sai phạm vi project.

## Secret Handling

- Never store secrets in memory, docs, handoff files, vector stores, or chat responses.
- Never print access tokens, passwords, private keys, signing keys, connection strings, or API keys verbatim.
- Mask detected secrets and reference only their file path and config key when needed.
- If a real secret appears in source, document the risk without copying the value.

## Filesystem Scope

- Restrict filesystem operations to the active project folder.
- Do not grant or request access to the entire drive.
- Do not write outside the project folder unless the user explicitly requests a specific path.
- Before recursive delete or move operations, verify the resolved absolute path is inside the intended directory.

## Memory Safety

- Use a project namespace for all memory reads and writes.
- Store only durable, reusable, verified findings.
- Log memory writes in the workflow status.
- Provide a review/delete path for incorrect memory.
- If memory conflicts with source code, trust source code and update memory.

## Destructive Actions

- Do not run destructive commands unless explicitly requested.
- Do not reset or revert user changes unless explicitly requested.
- Treat uncommitted changes as user-owned unless proven otherwise.

## Documentation Safety

- Do not invent architecture, APIs, database tables, credentials, or runtime behavior.
- Mark uncertainty clearly.
- Keep evidence paths close to claims.
