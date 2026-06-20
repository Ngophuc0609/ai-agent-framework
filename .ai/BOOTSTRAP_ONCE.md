# AI Framework Bootstrap Once

## Vietnamese User Summary

File này là prompt khởi tạo dùng một lần cho mỗi repo. Bạn có thể đưa file này cho Cline, Cursor, Claude, Copilot, Codex hoặc agent khác để yêu cầu đọc framework `.ai/` và từ các lần sau luôn làm việc theo framework này.

## Copy/Paste Prompt

```text
You are working inside this repository.

Before doing any coding, documentation, debugging, review, refactor, commit, or analysis task, read and follow the repository AI framework under `.ai/`.

This repository uses `.ai/` as the source of truth for agent behavior.

Required bootstrap steps:

1. Read `.ai/README.md`.
2. Read the adapter file that matches your tool when available:
   - Cline: `.ai/adapters/cline.md`
   - Cursor: `.ai/adapters/cursor.md`
   - Claude: `.ai/adapters/claude.md`
   - Codex: `.ai/adapters/codex.md`
   - Other tools: use `.ai/README.md` and `.ai/rules/00-global-rules.md`.
3. Read the registry files:
   - `.ai/registry/triggers.yml`
   - `.ai/registry/skills.yml`
   - `.ai/registry/workflows.yml`
   - `.ai/registry/adapters.yml`
   - `.ai/registry/tool-bootstrap.json`
4. Before doing any coding, documentation, debugging, review, refactor, commit, or analysis task, initialize required MCP/tool runtime when it is not already initialized:
   - Command created on: `2026-06-20`
   - Run: `ai-agent-sync --install-tools --yes`
   - This must create or verify `.ai/runtime/memory/memory.jsonl` for MCP Memory.
   - This must write or verify `.ai/runtime/mcp-servers.json` with an `mcp-memory` server using `MEMORY_FILE_PATH` scoped to the current repository.
   - If `ai-agent-sync` is not in `PATH`, run `bin/ai-agent-sync --install-tools --yes` from the repository root.
   - If automatic initialization fails, record the limitation and ask the user before continuing with weaker memory fallback.
5. Read the core rules:
   - `.ai/rules/00-global-rules.md`
   - `.ai/rules/03-safety-rules.md`
   - `.ai/rules/04-one-command-trigger.md`
   - `.ai/rules/05-workflow-execution-rules.md`
   - `.ai/rules/06-quality-gates.md`
   - `.ai/rules/10-codegraph-first-rules.md`
   - `.ai/rules/12-memory-policy-rules.md`
   - `.ai/rules/13-efficiency-cost-policy-rules.md`
   - `.ai/rules/14-tdd-first-feature-rules.md`
6. Treat `.ai/registry/triggers.yml` as the source of truth for routing user requests.
7. Use `.ai/skills/routing-ai-task/SKILL.md` when the correct specialized skill is not obvious.
8. For any new backend endpoint, new API, new feature, new service behavior, new database-backed flow, webhook, callback, integration flow, or background job, route to:
   - `.ai/skills/developing-backend-feature-tdd/SKILL.md`
   - `.ai/workflows/developing-backend-feature-tdd.md`
9. Do not implement production code for a new feature until these exist:
   - Brainstorm
   - API or behavior contract
   - Acceptance criteria
   - Test plan or failing tests
   - Error cases
   - Data impact
   - Auth/permission impact
   - Backward compatibility impact
10. For source-code analysis, debugging, refactoring, documentation, or API implementation:
   - Run CodeGraph preflight first when the tool is available.
   - If CodeGraph is unavailable and automatic setup fails, stop and ask the user whether to continue without CodeGraph or use another tool.
11. For workflows that list required agents:
   - Do not skip directly to the final artifact.
   - Run each listed agent spec.
   - Use delegated/sub-agent execution only when the user explicitly requested multi-agent/delegated/parallel work and the current runtime supports it.
   - If delegated agents are unavailable, run every agent sequentially in the current session.
   - Write each agent's required output or mark it not applicable with evidence.
   - Record the execution mode in handoff status.
12. For memory:
   - Initialize MCP Memory before the first operation using the command from step 4 when `.ai/runtime/memory/memory.jsonl` or `.ai/runtime/mcp-servers.json` is missing.
   - Retrieve memory before editing or documenting a module.
   - Use project namespace.
   - Store only verified durable facts.
   - Do not store secrets, tokens, passwords, private keys, temporary logs, unverified guesses, large raw source code, or full stack traces.
   - If memory conflicts with current source code, trust current source code and update memory.
13. For efficiency and cost:
   - Do not read the whole repository unless explicitly required.
   - Search memory and read project summary docs first.
   - Prefer `docs/PROJECT_CONTEXT.md`, `docs/FINDINGS.md`, and `docs/DECISIONS.md` before deep source reads.
   - Read only the smallest relevant file set.
   - Use git diff for review/commit tasks.
   - Use small/cheap models for discovery, classification, formatting, checklist generation, and simple summaries.
   - Use stronger models only for difficult debugging, business logic, security-sensitive review, architecture, migration, or multi-file refactoring.
14. For review before commit:
   - Use git diff first.
   - Review only changed files and direct dependencies.
   - Warn if a new endpoint or feature has no tests, failing tests, test plan, or executable regression check.
15. Keep filesystem access scoped to the current project folder only.
16. Do not expose secrets in chat, docs, memory, vectors, or handoff files.
17. Use English for internal operational instructions and generated rule/skill/workflow artifacts.
18. Respond to the user in Vietnamese unless the user explicitly requests another language.

After reading these files, reply in Vietnamese with:

1. Which adapter you selected.
2. Which core rules you loaded.
3. Whether CodeGraph is available.
4. Whether MCP Memory/Git/Filesystem are available.
5. Whether you can persist this framework instruction for future turns in this tool.
6. Any limitation that prevents full compliance.

From this point forward in this repository, always apply the `.ai/` framework before choosing tools or editing files.
```

## Short Prompt

Use this when the agent already knows the repo has `.ai/`:

```text
Đọc `.ai/BOOTSTRAP_ONCE.md`, thực hiện phần "Copy/Paste Prompt", và từ giờ luôn áp dụng framework `.ai/` trong repo này trước khi làm bất kỳ task nào. Trả lời tôi bằng tiếng Việt.
```

## Verification Prompts

Use these prompts to check whether the agent follows the framework.

### New Endpoint TDD Gate

```text
tạo endpoint mới GET /api/v1/health/details, trước hết chỉ brainstorm và lập test plan, chưa implement
```

Expected behavior:

- Route to `developing-backend-feature-tdd`.
- Do not edit production code.
- Return Brainstorm, API Contract, Acceptance Criteria, Test Plan, Implementation Plan, Files to Change, Risks, Done Criteria.

### Existing Endpoint Analysis

```text
phân tích endpoint hiện có /api/v1/health
```

Expected behavior:

- Route to `analyzing-api-endpoint` or existing API analysis behavior.
- Do not route to new-feature TDD.
- Read only relevant files.

### Diff Review

```text
review diff hiện tại trước commit
```

Expected behavior:

- Use git diff first.
- Review changed files and direct dependencies.
- Warn when a new feature or endpoint lacks tests or a test plan.

## Persistence Notes

Different tools persist instructions differently:

- Cline: add this bootstrap prompt to the first message of a new task, or ask Cline to remember it if memory is enabled.
- Cursor: add a short pointer to project rules or ask Cursor to read this file at session start.
- Claude: upload or reference this file at the start of the project/session; use memory only if available.
- Copilot: place a pointer to this file in repo instructions if your Copilot setup supports repository custom instructions.
- Codex: keep this file in the repo and reference it in the first task, or convert the framework into a Codex skill/plugin if needed.

Even if the tool claims it can remember instructions, verify with the smoke tests above after setup.
