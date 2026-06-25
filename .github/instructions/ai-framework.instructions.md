---
applyTo: "**"
---

<!-- generated-by: ai-agent-adapter-sync -->
# .ai Framework Instructions for copilot

Generated on: `2026-06-25`
Source of truth: `.ai/`

## Required Startup

Before any coding, documentation, debugging, review, refactor, commit, or analysis task:

1. Verify `.ai/` exists in this repository.
2. Initialize runtime tools when `.ai/runtime/memory/memory.jsonl` or `.ai/runtime/mcp-servers.json` is missing:

   ```bash
   ai-agent-sync --install-tools --yes
   ```

   If `ai-agent-sync` is not in `PATH`, run:

   ```bash
   bin/ai-agent-sync --install-tools --yes
   ```

3. Follow `.ai/registry/triggers.yml` before choosing a skill or workflow.
4. Read the selected `SKILL.md` and workflow before acting.
5. Apply CodeGraph-first, MCP Memory-first, safety, quality gates, and TDD-first rules from `.ai/rules/`.
6. For new backend APIs/features/jobs/webhooks/integration flows, route to `developing-backend-feature-tdd` and define brainstorm, contract, acceptance criteria, and tests before production code.
7. For workflows listing required agents, create every required agent output or mark it not applicable with evidence before final synthesis.
8. Keep chat responses to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## Canonical Files To Read

- `.ai/README.md`
- `.ai/BOOTSTRAP_ONCE.md`
- `.ai/registry/triggers.yml`
- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/tool-bootstrap.json`
- `.ai/rules/00-global-rules.md`
- `.ai/rules/05-workflow-execution-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/14-tdd-first-feature-rules.md`
- `.ai/rules/15-agent-runtime-tool-policy.md`

## Materialized .ai Rule Bundle



This section is generated from `.ai/` so native agent rule systems can load the framework without a manual bootstrap prompt.

## Source File: `.ai/README.md`

<!-- BEGIN SOURCE: .ai/README.md -->
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
The MCP Memory bootstrap command was created on `2026-06-20`; agents must run `ai-agent-sync --install-tools --yes` before any work when `.ai/runtime/memory/memory.jsonl` or `.ai/runtime/mcp-servers.json` is missing.
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

Required for source-reading, documentation, debugging, refactoring, and API-creation workflows:

- MCP Memory
- MCP Filesystem
- MCP Git
- CodeGraph or an explicit user-approved fallback

Recommended:

- Vector DB/RAG for large repositories
- `docs/PROJECT_CONTEXT.md`
- `docs/FINDINGS.md`
- `docs/DECISIONS.md`

For multi-agent orchestration:

- LangGraph persistence or another agent framework with session memory.

## Important Rules

- Resolve skills and workflows through `.ai/registry/`; do not hard-code triggers.
- For a new AI tool/session, start by reading `.ai/BOOTSTRAP_ONCE.md`.
- Run CodeGraph preflight before any source-code review.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before shell commands, native agent tool calls, delegated agent actions, or source-code-handover runs.
- Retrieve memory before editing or documenting a module.
- Treat current source code as the source of truth when memory conflicts with code.
- Do not store secrets in memory, docs, vectors, or handoff files.
- Do not grant filesystem access outside the active project folder.
- Write runtime state under `.ai/runs/<skillflow_id>/<run_id>/` whenever possible.
- Do not modify unrelated skillflows while adding or updating one skillflow.
<!-- END SOURCE: .ai/README.md -->


## Source File: `.ai/BOOTSTRAP_ONCE.md`

<!-- BEGIN SOURCE: .ai/BOOTSTRAP_ONCE.md -->
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
<!-- END SOURCE: .ai/BOOTSTRAP_ONCE.md -->


## Source File: `.ai/registry/adapters.yml`

<!-- BEGIN SOURCE: .ai/registry/adapters.yml -->
# Adapter registry.

adapters:
  - id: bootstrap-once
    path: .ai/BOOTSTRAP_ONCE.md
    user_description_vi: "Prompt khởi tạo một lần để agent đọc và áp dụng framework `.ai`."

  - id: codex
    path: .ai/adapters/codex.md
    user_description_vi: "Hướng dẫn chạy framework này trên Codex."

  - id: cursor
    path: .ai/adapters/cursor.md
    user_description_vi: "Hướng dẫn chạy framework này trên Cursor."

  - id: cline
    path: .ai/adapters/cline.md
    user_description_vi: "Hướng dẫn chạy framework này trên Cline."

  - id: cline-rollout-plan
    path: .ai/adapters/cline-rollout-plan.md
    user_description_vi: "Plan chạy thử framework `.ai` trên Cline."

  - id: claude
    path: .ai/adapters/claude.md
    user_description_vi: "Hướng dẫn chạy framework này trên Claude."

  - id: copilot
    path: .ai/adapters/copilot.md
    user_description_vi: "Hướng dẫn chạy framework này trên GitHub Copilot."

  - id: antigravity
    path: .ai/adapters/antigravity.md
    user_description_vi: "Hướng dẫn chạy framework này trên Google Antigravity."
<!-- END SOURCE: .ai/registry/adapters.yml -->


## Source File: `.ai/registry/skills.yml`

<!-- BEGIN SOURCE: .ai/registry/skills.yml -->
# Skill registry. Runtime agents must read this file before choosing a skill.
# Machine-facing metadata is English. Vietnamese fields are user-facing only.

skills:
  - id: source-code-handover
    skill_path: .ai/skills/source-code-handover/SKILL.md
    workflow_id: make-new-dev-docs
    user_description_vi: "Tạo tài liệu bàn giao source code cho developer mới."
    status: active

  - id: routing-ai-task
    skill_path: .ai/skills/routing-ai-task/SKILL.md
    workflow_id: null
    user_description_vi: "Chọn đúng skill/workflow trước khi làm việc."
    status: active

  - id: developing-backend-feature-tdd
    skill_path: .ai/skills/developing-backend-feature-tdd/SKILL.md
    workflow_id: developing-backend-feature-tdd
    user_description_vi: "Tạo endpoint/tính năng backend theo hướng brainstorm, contract và TDD-first."
    status: active

  - id: analyzing-api-endpoint
    skill_path: .ai/skills/analyzing-api-endpoint/SKILL.md
    workflow_id: null
    user_description_vi: "Phân tích endpoint API đã tồn tại."
    status: active

  - id: security-review
    skill_path: .ai/skills/security-review/SKILL.md
    workflow_id: null
    user_description_vi: "Review rủi ro bảo mật backend/API, auth, validation, secrets, config và dependency."
    status: active

  - id: analyzing-auth-permissions
    skill_path: .ai/skills/analyzing-auth-permissions/SKILL.md
    workflow_id: null
    user_description_vi: "Phân tích auth, session/token, role, permission và ownership checks."
    status: active

  - id: reviewing-openapi-contract
    skill_path: .ai/skills/reviewing-openapi-contract/SKILL.md
    workflow_id: null
    user_description_vi: "Đối chiếu OpenAPI/Swagger/Postman/API docs với source code."
    status: active

  - id: database-query-analysis
    skill_path: .ai/skills/database-query-analysis/SKILL.md
    workflow_id: null
    user_description_vi: "Phân tích query database, N+1, index, transaction và rủi ro performance."
    status: active

  - id: ci-cd-troubleshooting
    skill_path: .ai/skills/ci-cd-troubleshooting/SKILL.md
    workflow_id: null
    user_description_vi: "Điều tra lỗi CI/CD, build, test trên CI, deploy và container build."
    status: active

  - id: skill-security-audit
    skill_path: .ai/skills/skill-security-audit/SKILL.md
    workflow_id: null
    user_description_vi: "Audit bảo mật skill, SKILL.md, registry, workflow và script đi kèm."
    status: active

  - id: skill-registry-maintenance
    skill_path: .ai/skills/skill-registry-maintenance/SKILL.md
    workflow_id: null
    user_description_vi: "Bảo trì registry skill/workflow/trigger và kiểm tra consistency."
    status: active

  - id: prompt-injection-review
    skill_path: .ai/skills/prompt-injection-review/SKILL.md
    workflow_id: null
    user_description_vi: "Review rủi ro prompt injection trong agent workflow, tool use, web/email/docs/RAG."
    status: active

  - id: mcp-integration-planning
    skill_path: .ai/skills/mcp-integration-planning/SKILL.md
    workflow_id: null
    user_description_vi: "Lập plan hoặc review tích hợp MCP, quyền tools/resources, auth và sandbox."
    status: active

  - id: agent-workflow-evaluation
    skill_path: .ai/skills/agent-workflow-evaluation/SKILL.md
    workflow_id: null
    user_description_vi: "Thiết kế hoặc review eval/regression cho skill, workflow và routing agent."
    status: active

  - id: release-notes-generation
    skill_path: .ai/skills/release-notes-generation/SKILL.md
    workflow_id: null
    user_description_vi: "Tạo release notes, changelog, upgrade notes hoặc deployment summary."
    status: active

  - id: writing-backend-tests-first
    skill_path: .ai/skills/writing-backend-tests-first/SKILL.md
    workflow_id: null
    user_description_vi: "Viết test backend trước production code."
    status: support

  - id: generating-backend-tests
    skill_path: .ai/skills/generating-backend-tests/SKILL.md
    workflow_id: null
    user_description_vi: "Sinh hoặc cập nhật test backend cho phạm vi đã xác định."
    status: support

  - id: generating-api-test-assets
    skill_path: .ai/skills/generating-api-test-assets/SKILL.md
    workflow_id: null
    user_description_vi: "Tạo curl/Postman/SQL verify cho API."
    status: support

  - id: reviewing-git-diff
    skill_path: .ai/skills/reviewing-git-diff/SKILL.md
    workflow_id: null
    user_description_vi: "Review diff hiện tại trước khi commit."
    status: active

  - id: writing-vietnamese-commit-message
    skill_path: .ai/skills/writing-vietnamese-commit-message/SKILL.md
    workflow_id: null
    user_description_vi: "Viết commit message tiếng Việt dựa trên diff và test."
    status: active

  - id: refactoring-backend-safely
    skill_path: .ai/skills/refactoring-backend-safely/SKILL.md
    workflow_id: null
    user_description_vi: "Refactor backend an toàn, có kiểm soát phạm vi."
    status: active

  - id: debugging-backend-issue
    skill_path: .ai/skills/debugging-backend-issue/SKILL.md
    workflow_id: null
    user_description_vi: "Điều tra và sửa lỗi backend theo hướng evidence-first."
    status: active

  - id: reviewing-sql-migration
    skill_path: .ai/skills/reviewing-sql-migration/SKILL.md
    workflow_id: null
    user_description_vi: "Review migration/schema change trước khi chạy."
    status: support

  - id: analyzing-background-jobs
    skill_path: .ai/skills/analyzing-background-jobs/SKILL.md
    workflow_id: null
    user_description_vi: "Phân tích job nền, scheduler, queue hoặc worker."
    status: active

  - id: docs-merge-handbook
    skill_path: .ai/skills/docs-merge-handbook/SKILL.md
    workflow_id: docs-merge-handbook
    user_description_vi: "Tổng hợp các bản nháp tài liệu thành handbook cuối."
    status: active

  - id: maintaining-existing-apis
    skill_path: .ai/skills/maintaining-existing-apis/SKILL.md
    workflow_id: maintaining-existing-apis
    user_description_vi: "Duy trì hoặc chỉnh API/endpoint/route đã tồn tại."
    status: active

  - id: using-superpowers
    skill_path: .ai/skills/using-superpowers/SKILL.md
    workflow_id: null
    user_description_vi: "Chuẩn nền để agent làm việc theo phương pháp Superpowers."
    status: support

  - id: skill-detector
    skill_path: .ai/skills/skill-detector/SKILL.md
    workflow_id: null
    user_description_vi: "Nhận diện skill phù hợp từ yêu cầu người dùng."
    status: support

  - id: standardizing-ai-agent-framework
    skill_path: .ai/skills/standardizing-ai-agent-framework/SKILL.md
    workflow_id: standardizing-ai-agent-framework
    user_description_vi: "Chuẩn hóa bộ .ai, rule, skill, workflow và adapter native cho nhiều AI agent."
    status: active

  - id: self-correction-loop
    skill_path: .ai/skills/self-correction-loop/SKILL.md
    workflow_id: null
    user_description_vi: "Tự động review và sửa lỗi code trước khi chốt."
    status: active

  - id: human-approval-gate
    skill_path: .ai/skills/human-approval-gate/SKILL.md
    workflow_id: null
    user_description_vi: "Dừng lại chờ người dùng duyệt trước khi chạy lệnh nguy hiểm."
    status: active

  - id: memory-consolidation-cleanup
    skill_path: .ai/skills/memory-consolidation-cleanup/SKILL.md
    workflow_id: memory-consolidation-cleanup
    user_description_vi: "Nén và dọn dẹp bộ nhớ dự án định kỳ."
    status: active
<!-- END SOURCE: .ai/registry/skills.yml -->


## Source File: `.ai/registry/workflows.yml`

<!-- BEGIN SOURCE: .ai/registry/workflows.yml -->
# Workflow registry. Keep workflow instructions in English.

workflows:
  - id: make-new-dev-docs
    path: .ai/workflows/make-new-dev-docs.md
    skill_id: source-code-handover
    user_description_vi: "Workflow tạo tài liệu bàn giao source code."
    default_output_namespace: docs
    status: active

  - id: make-new-dev-docs-model-routing
    path: .ai/workflows/make-new-dev-docs-model-routing.md
    skill_id: source-code-handover
    user_description_vi: "Phần mở rộng chọn model/tier cho workflow tạo tài liệu."
    default_output_namespace: docs
    status: active

  - id: docs-merge-handbook
    path: .ai/workflows/docs-merge-handbook.md
    skill_id: docs-merge-handbook
    user_description_vi: "Workflow tổng hợp handbook cuối từ các draft."
    default_output_namespace: docs
    status: active

  - id: developing-backend-feature-tdd
    path: .ai/workflows/developing-backend-feature-tdd.md
    skill_id: developing-backend-feature-tdd
    user_description_vi: "Workflow tạo endpoint/tính năng backend theo TDD-first."
    default_output_namespace: backend-feature-tdd
    status: active

  - id: maintaining-existing-apis
    path: .ai/workflows/maintaining-existing-apis.md
    skill_id: maintaining-existing-apis
    user_description_vi: "Workflow duy trì hoặc chỉnh API đã tồn tại."
    default_output_namespace: api-changes
    status: active

  - id: standardizing-ai-agent-framework
    path: .ai/workflows/standardizing-ai-agent-framework.md
    skill_id: standardizing-ai-agent-framework
    user_description_vi: "Workflow chuẩn hóa .ai để sinh native rules và Agent Skills cho nhiều AI agent."
    default_output_namespace: ai-agent-framework
    status: active

  - id: memory-consolidation-cleanup
    path: .ai/workflows/memory-consolidation-cleanup.md
    skill_id: memory-consolidation-cleanup
    user_description_vi: "Workflow nén và dọn dẹp bộ nhớ dự án."
    default_output_namespace: memory
    status: active
<!-- END SOURCE: .ai/registry/workflows.yml -->


## Source File: `.ai/registry/triggers.yml`

<!-- BEGIN SOURCE: .ai/registry/triggers.yml -->
# Trigger registry. Runtime agents must resolve user requests through this file.
# English trigger phrases are machine-facing examples.
# Vietnamese trigger phrases are intentional user-facing aliases.

triggers:
  - workflow_id: make-new-dev-docs
    skill_id: source-code-handover
    trigger_phrases_en:
      - create handover documentation
      - create onboarding docs
      - document the source code
      - generate source handover docs
    trigger_phrases_vi:
      - tạo tài liệu
      - làm tài liệu
      - làm tài liệu cho người mới
      - tạo tài liệu cho người mới
      - chạy skill tài liệu
      - chạy skill source handover
      - làm docs bàn giao
      - tạo tài liệu tổng hợp

  - workflow_id: make-new-dev-docs-model-routing
    skill_id: source-code-handover
    trigger_phrases_en:
      - create budget onboarding docs
      - create balanced onboarding docs
      - create high accuracy handover docs
    trigger_phrases_vi:
      - làm tài liệu cho người mới bản tiết kiệm
      - làm tài liệu cho người mới bản cân bằng
      - làm tài liệu cho người mới bản chính xác cao
      - review kỹ source để bàn giao production

  - workflow_id: docs-merge-handbook
    skill_id: docs-merge-handbook
    trigger_phrases_en:
      - merge docs into handbook
      - create final handbook
      - review final documentation
    trigger_phrases_vi:
      - tổng hợp handbook
      - tạo tài liệu tổng hợp từ docs
      - review lại docs bằng model mạnh
      - kiểm tra lại tài liệu cuối

  - workflow_id: null
    skill_id: analyzing-api-endpoint
    trigger_phrases_en:
      - analyze existing api
      - document existing endpoint
      - inspect api route
    trigger_phrases_vi:
      - phân tích api hiện có
      - phân tích endpoint hiện có

  - workflow_id: null
    skill_id: security-review
    trigger_phrases_en:
      - security review
      - review security
      - check backend security
      - inspect secrets exposure
      - review api security
    trigger_phrases_vi:
      - review bảo mật
      - kiểm tra bảo mật
      - kiểm tra security
      - review security
      - kiểm tra lộ secrets

  - workflow_id: null
    skill_id: analyzing-auth-permissions
    trigger_phrases_en:
      - analyze auth permissions
      - inspect authentication flow
      - inspect authorization flow
      - analyze rbac
      - review ownership checks
    trigger_phrases_vi:
      - phân tích auth
      - phân tích phân quyền
      - kiểm tra permission
      - phân tích rbac
      - kiểm tra ownership

  - workflow_id: null
    skill_id: reviewing-openapi-contract
    trigger_phrases_en:
      - review openapi contract
      - compare swagger with code
      - review api documentation contract
      - validate postman collection
      - check api docs mismatch
    trigger_phrases_vi:
      - review openapi
      - kiểm tra swagger
      - đối chiếu api docs
      - kiểm tra postman
      - kiểm tra lệch contract api

  - workflow_id: null
    skill_id: database-query-analysis
    trigger_phrases_en:
      - analyze database query
      - investigate slow query
      - check n plus one
      - review query performance
      - analyze transaction locking
    trigger_phrases_vi:
      - phân tích query
      - phân tích query database
      - kiểm tra query chậm
      - kiểm tra n+1
      - phân tích transaction

  - workflow_id: null
    skill_id: ci-cd-troubleshooting
    trigger_phrases_en:
      - troubleshoot ci
      - fix ci failure
      - investigate pipeline failure
      - debug deployment failure
      - fix docker build failure
    trigger_phrases_vi:
      - debug ci
      - sửa lỗi ci
      - điều tra lỗi pipeline
      - debug deploy
      - sửa lỗi docker build

  - workflow_id: null
    skill_id: skill-security-audit
    trigger_phrases_en:
      - audit agent skill security
      - review skill security
      - audit skill package
      - check skill prompt injection
      - review skill supply chain risk
    trigger_phrases_vi:
      - audit bảo mật skill
      - review bảo mật skill
      - kiểm tra skill độc hại
      - kiểm tra prompt injection trong skill
      - audit skill ai

  - workflow_id: null
    skill_id: skill-registry-maintenance
    trigger_phrases_en:
      - validate skill registry
      - maintain skill registry
      - fix trigger registry
      - check workflow registry
      - repair skill metadata
    trigger_phrases_vi:
      - kiểm tra registry skill
      - bảo trì registry skill
      - sửa trigger registry
      - kiểm tra workflow registry
      - validate registry skill

  - workflow_id: null
    skill_id: prompt-injection-review
    trigger_phrases_en:
      - prompt injection review
      - review indirect prompt injection
      - check agent injection risk
      - review rag prompt injection
      - review tool misuse risk
    trigger_phrases_vi:
      - review prompt injection
      - kiểm tra prompt injection
      - kiểm tra indirect prompt injection
      - review rủi ro tool misuse
      - kiểm tra injection trong rag

  - workflow_id: null
    skill_id: mcp-integration-planning
    trigger_phrases_en:
      - plan mcp integration
      - review mcp server
      - design mcp tools
      - document mcp integration
      - check mcp permissions
    trigger_phrases_vi:
      - lập plan mcp
      - review mcp server
      - thiết kế mcp tools
      - tài liệu tích hợp mcp
      - kiểm tra quyền mcp

  - workflow_id: null
    skill_id: agent-workflow-evaluation
    trigger_phrases_en:
      - evaluate agent workflow
      - create skill eval
      - test skill routing
      - build agent regression suite
      - review workflow evaluation
    trigger_phrases_vi:
      - eval workflow agent
      - tạo eval skill
      - kiểm tra routing skill
      - tạo regression cho agent
      - đánh giá workflow ai

  - workflow_id: null
    skill_id: release-notes-generation
    trigger_phrases_en:
      - generate release notes
      - write changelog
      - create upgrade notes
      - summarize release changes
      - write deployment summary
    trigger_phrases_vi:
      - tạo release notes
      - viết changelog
      - tạo ghi chú nâng cấp
      - tóm tắt thay đổi release
      - viết deployment summary

  - workflow_id: null
    skill_id: routing-ai-task
    trigger_phrases_en:
      - route ai task
      - choose task workflow
      - decide task skill
      - classify user request
    trigger_phrases_vi:
      - định tuyến task ai
      - phân loại yêu cầu
      - chọn workflow xử lý
      - chọn skill xử lý

  - workflow_id: null
    skill_id: analyzing-background-jobs
    trigger_phrases_en:
      - analyze background job
      - inspect scheduler
      - document worker
      - analyze queue processing
    trigger_phrases_vi:
      - phân tích job nền
      - phân tích scheduler
      - phân tích worker
      - phân tích queue
      - tài liệu job nền

  - workflow_id: maintaining-existing-apis
    skill_id: maintaining-existing-apis
    trigger_phrases_en:
      - update existing api
      - change existing endpoint
      - maintain existing api route
    trigger_phrases_vi:
      - sửa api hiện có
      - chỉnh endpoint hiện có

  - workflow_id: null
    skill_id: generating-backend-tests
    trigger_phrases_en:
      - generate backend tests
      - add backend tests
      - update backend tests
      - create service tests
    trigger_phrases_vi:
      - sinh test backend
      - tạo test backend
      - thêm test backend
      - cập nhật test backend

  - workflow_id: null
    skill_id: writing-backend-tests-first
    trigger_phrases_en:
      - write backend tests first
      - write failing backend tests
      - create tests before implementation
      - add regression test first
    trigger_phrases_vi:
      - viết test trước
      - viết test backend trước
      - tạo test fail trước
      - thêm regression test trước

  - workflow_id: null
    skill_id: generating-api-test-assets
    trigger_phrases_en:
      - generate api test assets
      - create curl examples
      - create postman requests
      - generate sql verification
    trigger_phrases_vi:
      - tạo curl kiểm thử api
      - tạo postman kiểm thử api
      - tạo sql verify
      - tạo tài sản test api

  - workflow_id: developing-backend-feature-tdd
    skill_id: developing-backend-feature-tdd
    trigger_phrases_en:
      - create new api
      - add new api
      - create endpoint
      - add endpoint
      - create new backend feature
      - add backend feature
      - create feature
      - add business flow
      - add service method
      - add webhook
      - add callback
      - add background job
    trigger_phrases_vi:
      - tạo api mới
      - thêm api mới
      - tạo endpoint mới
      - thêm endpoint
      - tạo route mới
      - thêm route api
      - tạo controller action
      - tạo tính năng mới
      - thêm tính năng mới
      - thêm flow mới
      - tạo webhook
      - thêm webhook
      - tạo job mới

  - workflow_id: null
    skill_id: reviewing-git-diff
    trigger_phrases_en:
      - review current diff
      - review git diff
      - review changes before commit
    trigger_phrases_vi:
      - review diff hiện tại
      - review trước commit
      - kiểm tra diff trước commit

  - workflow_id: null
    skill_id: reviewing-sql-migration
    trigger_phrases_en:
      - review sql migration
      - review database migration
      - review schema change
      - inspect migration rollback
    trigger_phrases_vi:
      - review migration
      - review sql migration
      - kiểm tra migration
      - kiểm tra thay đổi schema

  - workflow_id: null
    skill_id: writing-vietnamese-commit-message
    trigger_phrases_en:
      - write commit message
      - write vietnamese commit message
    trigger_phrases_vi:
      - viết commit message
      - viết commit message tiếng việt

  - workflow_id: null
    skill_id: debugging-backend-issue
    trigger_phrases_en:
      - debug backend issue
      - fix backend bug
      - investigate backend error
    trigger_phrases_vi:
      - debug lỗi backend
      - sửa lỗi backend
      - điều tra lỗi backend

  - workflow_id: null
    skill_id: refactoring-backend-safely
    trigger_phrases_en:
      - refactor backend safely
      - refactor backend code
    trigger_phrases_vi:
      - refactor backend
      - refactor code backend

  - workflow_id: null
    skill_id: skill-detector
    trigger_phrases_en:
      - detect skill
      - choose skill
      - select workflow
      - identify matching skill
    trigger_phrases_vi:
      - chọn skill
      - xác định skill
      - chọn workflow
      - nhận diện skill phù hợp

  - workflow_id: standardizing-ai-agent-framework
    skill_id: standardizing-ai-agent-framework
    trigger_phrases_en:
      - standardize ai agent framework
      - standardize agent skills
      - create cross agent rules
      - generate native agent adapters
      - review agent framework structure
    trigger_phrases_vi:
      - chuẩn hóa ai agent
      - chuẩn hóa bộ .ai
      - chuẩn hóa skill flow
      - tạo skill flow ai agent
      - tạo rule cho nhiều agent
      - sinh cấu trúc riêng cho từng agent
      - phân tích cấu trúc và skill agent

  - workflow_id: null
    skill_id: self-correction-loop
    trigger_phrases_en:
      - self correct
      - peer review code
      - critique code
    trigger_phrases_vi:
      - tự sửa lỗi
      - tự review code
      - critique code

  - workflow_id: null
    skill_id: human-approval-gate
    trigger_phrases_en:
      - request human approval
      - pause for approval
      - wait for human
    trigger_phrases_vi:
      - chờ duyệt
      - chờ con người duyệt
      - xin phép chạy

  - workflow_id: memory-consolidation-cleanup
    skill_id: memory-consolidation-cleanup
    trigger_phrases_en:
      - consolidate memory
      - clean up project memory
      - compress memory
    trigger_phrases_vi:
      - dọn dẹp bộ nhớ
      - nén bộ nhớ
      - tổng hợp memory
<!-- END SOURCE: .ai/registry/triggers.yml -->


## Source File: `.ai/registry/tool-bootstrap.json`

<!-- BEGIN SOURCE: .ai/registry/tool-bootstrap.json -->
{
  "codegraph": {
    "commands": [
      "codegraph",
      "codegraph-mcp",
      "codegraph-cli",
      "codegraph-daemon"
    ],
    "install_command": "npm install -g @astudioplus/codegraph-mcp",
    "init_command": "codegraph-mcp --workspace {repo} --graph-only --run-tool codegraph_index_directory --tool-args {repo_tool_args}"
  },
  "mcp-memory": {
    "created_at": "2026-06-20",
    "purpose": "Initialize repo-local MCP Memory storage before agents read, edit, document, debug, review, refactor, or commit.",
    "commands": [
      "mcp-server-memory"
    ],
    "install_command": "npm install -g @modelcontextprotocol/server-memory",
    "init_command": "python3 -c 'from pathlib import Path; p=Path({repo_json}) / \".ai/runtime/memory/memory.jsonl\"; p.parent.mkdir(parents=True, exist_ok=True); p.touch()'"
  },
  "mcp-filesystem": {
    "commands": [
      "mcp-server-filesystem"
    ],
    "install_command": "npm install -g @modelcontextprotocol/server-filesystem",
    "init_command": ""
  },
  "mcp-git": {
    "commands": [
      "git-mcp-server"
    ],
    "install_command": "npm install -g @cyanheads/git-mcp-server",
    "init_command": ""
  }
}
<!-- END SOURCE: .ai/registry/tool-bootstrap.json -->


## Source File: `.ai/registry/tool-candidates.json`

<!-- BEGIN SOURCE: .ai/registry/tool-candidates.json -->
{
  "purpose": "Optional tool candidates for evidence-backed source-code handover and framework workflows. These are not mandatory bootstrap installs.",
  "local_required": {
    "ripgrep": {
      "commands": ["rg"],
      "role": "Fast physical file discovery for routes, configs, Redis keys, SQL, and identifiers."
    },
    "git": {
      "commands": ["git"],
      "role": "Repository status, history, blame, changed files, and provenance."
    },
    "language_build_tool": {
      "commands": ["dotnet", "npm", "mvn", "gradle", "go", "cargo"],
      "role": "Build/test verification when applicable to the repository stack."
    },
    "semgrep": {
      "commands": ["semgrep"],
      "role": "Pattern scanning for auth bypass, raw SQL, secret exposure, risky legacy code, and framework-specific hazards."
    },
    "sql_metadata_export": {
      "commands": ["sqlcmd", "psql", "mysql", "sqlite3"],
      "role": "Database schema extraction for tables, columns, constraints, indexes, procedures, triggers, and views."
    },
    "openapi_postman_parser": {
      "commands": ["jq", "yq", "node", "python3"],
      "role": "Parse Swagger/OpenAPI/Postman collections into endpoint inventory, request schema, response schema, and examples."
    }
  },
  "large_repo_recommended": {
    "sourcegraph_mcp": {
      "role": "Large or multi-repo search, symbol navigation, references, ownership, history, and cross-repository evidence.",
      "installation_policy": "Configure only when available/trusted; do not auto-install by default."
    },
    "github_mcp": {
      "role": "Repository, commit, pull request, issue, CI, and security evidence from GitHub.",
      "installation_policy": "Use official GitHub MCP configuration when the user grants repository access."
    },
    "codeql": {
      "commands": ["codeql"],
      "role": "Semantic query and data-flow analysis for high-risk modules.",
      "installation_policy": "Use for high-risk flows; building CodeQL databases can be expensive."
    },
    "scip_lsp_index": {
      "commands": ["scip", "lsif", "clangd", "typescript-language-server", "omnisharp"],
      "role": "Go-to-definition, references, implementations, and symbol graph evidence."
    },
    "sqlite_duckdb": {
      "commands": ["sqlite3", "duckdb"],
      "role": "Persist evidence graph, inventory coverage, and asset-level documentation metrics."
    },
    "diagram_generator": {
      "commands": ["mmdc", "plantuml"],
      "role": "Generate or validate Mermaid/PlantUML diagrams for architecture, jobs, realtime, and request lifecycles."
    }
  },
  "runtime_optional": {
    "opentelemetry_or_log_parser": {
      "role": "Confirm runtime behavior, request flow, errors, and integration behavior from logs/traces."
    },
    "hangfire_dashboard_export": {
      "role": "Confirm background jobs, schedules, retry, and failed job behavior."
    },
    "redis_snapshot": {
      "role": "Confirm Redis key patterns, TTLs, data types, and real cache usage."
    },
    "api_traffic_sample": {
      "role": "Confirm real client request/response contracts and legacy quirks."
    }
  }
}
<!-- END SOURCE: .ai/registry/tool-candidates.json -->


## Source File: `.ai/rules/00-global-rules.md`

<!-- BEGIN SOURCE: .ai/rules/00-global-rules.md -->
# 00 Global Rules

## Summary

This rule defines the baseline for `.ai`: use registries for skill/workflow selection, use English for agent-facing instructions, and use Vietnamese only for final chat responses to the Vietnamese-speaking user unless another language is requested.

## Language Policy

- Write all machine-facing rules, workflows, skill bodies, agent specs, templates, and operational notes in English.
- Vietnamese is allowed only in user-facing chat responses, explicit Vietnamese trigger aliases, or final developer-facing deliverables that explicitly require Vietnamese.
- Final chat responses to the user must be in Vietnamese unless the user requests another language.
- Do not mix Vietnamese into execution instructions.

## Registry First

- Read `.ai/registry/triggers.yml` before choosing a workflow.
- Read `.ai/registry/skills.yml` before loading a skill.
- Read `.ai/registry/workflows.yml` before loading a workflow.
- Do not hard-code trigger phrases in isolated rule files.

## Skill First

- If a request matches a registered skill, read that skill's `SKILL.md` before taking action.
- If the skill declares required background or a required supporting skill, read it before execution.
- Keep loaded context minimal; load references only when needed.
- Use `.ai/skills/routing-ai-task/SKILL.md` for skill selection when the request could match multiple skills or when no specialized skill is obvious.

## CodeGraph First

Before any source-code review, source-code documentation, debugging, refactor planning, or API implementation:

1. Check whether CodeGraph is available for the current project.
2. If unavailable, try the approved local setup command from `.ai/rules/10-codegraph-first-rules.md`.
3. If setup fails, stop and ask the user whether to continue without CodeGraph or use another tool.
4. Record any fallback in the run status and final response.

## Memory First

Before editing or documenting a module:

1. Retrieve memory for the current project namespace and target module.
2. Scan current source code.
3. Compare memory with source code.
4. Trust source code when memory conflicts with code.
5. Write or update the deliverable.
6. Store only verified, durable findings back to memory.

Never store secrets, tokens, passwords, private keys, temporary logs, unverified guesses, large raw source code, or full stack traces in memory.

## Evidence

- Every important claim must cite file paths, commands, tests, or observed runtime evidence.
- If a conclusion is inferred, label it as inference.
- If evidence is missing, mark the item as uncertain and add an open question.

## Efficiency

- Follow `.ai/rules/13-efficiency-cost-policy-rules.md`.
- Do not read the whole repository unless the task explicitly requires it.
- Use memory and project summary docs before detailed source reads.
- Use small or cheap models for discovery, classification, summarization, formatting, and checklist generation.
- Use strong models only for difficult reasoning, debugging, architecture, security, or multi-file refactoring.

## Write Scope

- Keep writes inside the project folder.
- Prefer run-scoped output under `.ai/runs/<skillflow_id>/<run_id>/`.
- Write public deliverables only to paths explicitly allowed by the selected workflow.
- Do not modify unrelated skillflows, rules, agents, or docs unless the user requests it.

## Safety

- Do not expose secrets in memory, docs, handoff files, vector stores, or chat responses.
- Mask secrets when referencing their existence.
- Do not grant filesystem access outside the active project folder.
- Do not run destructive commands unless explicitly requested and confirmed.
<!-- END SOURCE: .ai/rules/00-global-rules.md -->


## Source File: `.ai/rules/01-documentation-skill.md`

<!-- BEGIN SOURCE: .ai/rules/01-documentation-skill.md -->
# 01 Documentation Skill Rules

## Summary

This rule describes how to trigger and control the source-code handover documentation workflow.

## Trigger Resolution

When the user asks for source-code handover documentation, onboarding documentation, or equivalent Vietnamese trigger phrases, resolve the request through `.ai/registry/triggers.yml` and run workflow `make-new-dev-docs`.

Do not run the full documentation workflow when the user only asks to edit rules, review docs, or discuss the framework.

## Required Inputs

Before generating documentation, read:

- `.ai/README.md`
- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`
- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/07-handover-documentation-dod.md`
- `.ai/rules/08-source-code-handover-quality-checklist.md`
- The selected skill and workflow files.

If a required file is missing, record the limitation and continue only with the safe subset of the workflow.

## Documentation Goals

The final documentation must help a new developer understand:

- What the system is.
- How to run it locally.
- Which files to read first.
- Runtime configuration and environment requirements.
- Main modules, APIs, database, auth, integrations, jobs, and deployment behavior when present.
- Debugging, logging, and smoke-test paths.
- Unknowns that require maintainer confirmation.

## Output Policy

The current legacy documentation workflow may write to:

- `draft-docs/`
- `docs/`
- `.ai/handoff/`

New skillflows must use isolated namespaces as defined in `.ai/rules/11-skillflow-extension-rules.md`.

The final chat response must summarize changed files, conflicts, open questions, and readiness. Do not paste full generated documentation into chat.

## Missing Areas

Each repository may omit database, frontend, background jobs, realtime features, or deployment config.

When an area is not detected:

1. Do not invent content.
2. State that it was not found in the current source.
3. Add an open question when the area is operationally important.
4. Complete all evidence-backed sections.
<!-- END SOURCE: .ai/rules/01-documentation-skill.md -->


## Source File: `.ai/rules/02-multi-agent-rules.md`

<!-- BEGIN SOURCE: .ai/rules/02-multi-agent-rules.md -->
# 02 Multi-Agent Rules

## Summary

This rule standardizes how work is divided across multiple agents for documentation or source review.

## Coordination

- Use the workflow file as the source of truth for agent order, responsibilities, and output paths.
- Each agent must write only to its assigned files.
- Each agent must include evidence paths for important findings.
- Agents must write open questions instead of guessing.
- Agent 6 is responsible for source/symbol verification, Agent 7 for cross-layer flow/conflict verification, Agent 8 for safety/build/test/runtime/ops evidence, Agent 9 for final documentation, and Agent 10 for independent publish validation.

## Execution Contract

When a workflow lists required agents, the runtime must not skip directly to the final output.

Required behavior:

1. Execute every listed agent unless the workflow explicitly marks it optional or not applicable.
2. Prefer real delegated/sub-agent execution only when the current AI runtime supports it and the user explicitly requested multi-agent, delegated, or parallel agent work.
3. If real delegated agents are unavailable, run the same agent specs sequentially as a fallback.
4. Preserve each agent boundary even in sequential fallback.
5. Write or update the required output file for each agent.
6. Record the execution mode in handoff status:
   - `delegated-parallel`
   - `delegated-sequential`
   - `single-runtime-sequential-fallback`
7. Do not generate the final handbook until Agent 1-5 discovery outputs and Agent 6-8 verification outputs exist, or the missing outputs are explicitly marked not applicable with a reason.

## Handoff

Use handoff files only for coordination facts that other agents need:

- `.ai/handoff/STATUS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/handoff/CONFLICTS.md`
- `.ai/handoff/DECISIONS.md`

For new workflows, prefer `.ai/runs/<skillflow_id>/<run_id>/handoff/`.

## Parallel Work

Agents may run in parallel only when their output paths do not conflict and their inputs are stable.

If parallel execution is unavailable:

1. Run agents sequentially.
2. Preserve each agent's output boundary.
3. Record the fallback in status.

## Conflict Handling

When two agents disagree:

1. Compare the evidence.
2. Trust current source code over memory or prior notes.
3. Prefer direct runtime/config evidence over inference.
4. Record unresolved conflicts for reviewer or human confirmation.

## Completion

A multi-agent workflow is complete only when:

- Required agent outputs exist or are explicitly marked not applicable.
- The execution mode is recorded.
- Open questions are listed.
- Conflicts are resolved or documented.
- Readiness is assigned.
- Final response summarizes status in Vietnamese.
<!-- END SOURCE: .ai/rules/02-multi-agent-rules.md -->


## Source File: `.ai/rules/03-safety-rules.md`

<!-- BEGIN SOURCE: .ai/rules/03-safety-rules.md -->
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
<!-- END SOURCE: .ai/rules/03-safety-rules.md -->


## Source File: `.ai/rules/04-one-command-trigger.md`

<!-- BEGIN SOURCE: .ai/rules/04-one-command-trigger.md -->
# 04 One-Command Trigger Rules

## Vietnamese User Summary

Rule này cho phép người dùng dùng một câu ngắn như `tạo tài liệu` hoặc `tạo api mới` để kích hoạt workflow đúng.

## Trigger Flow

When the user gives a short command:

1. Read `.ai/registry/triggers.yml`.
2. Match both English and Vietnamese trigger aliases.
3. Resolve to one workflow or one skill-only task.
4. Load the matching skill and workflow when a workflow exists.
5. Apply required global rules.

## Ambiguous Trigger

If multiple workflows or skills match:

1. Prefer the most specific trigger.
2. Prefer exact phrase matches over broad semantic matches.
3. If still ambiguous, ask one concise clarification question in Vietnamese.

## No Match

If no workflow matches:

1. Do not invent a workflow.
2. Explain in Vietnamese that no matching workflow exists.
3. Offer the closest existing workflow only when the match is safe.

## Execution Language

- Internal execution instructions remain English.
- Chat responses to the user remain Vietnamese.
<!-- END SOURCE: .ai/rules/04-one-command-trigger.md -->


## Source File: `.ai/rules/05-workflow-execution-rules.md`

<!-- BEGIN SOURCE: .ai/rules/05-workflow-execution-rules.md -->
# 05 Workflow Execution Rules

## Vietnamese User Summary

Rule này quy định thứ tự chạy workflow, preflight, output và fallback.

## Standard Execution Sequence

1. Resolve the trigger through `.ai/registry/triggers.yml`.
2. Use `routing-ai-task` when the correct specialized skill is not obvious.
3. Read the selected skill.
4. Read the selected workflow.
5. Read referenced rules.
6. Create or select a run namespace.
7. Search memory and project summary docs before detailed source reads.
8. Run CodeGraph preflight when source code is involved.
9. Limit file reads to the smallest useful scope.
10. Execute the workflow.
11. Run validation and quality gates.
12. Save confirmed memory findings when memory tools are available.
13. Respond to the user in Vietnamese.

## Run Namespace

New workflows should write runtime state to:

```text
.ai/runs/<skillflow_id>/<run_id>/
```

Suggested subdirectories:

```text
handoff/
findings/
artifacts/
logs/
```

## Fallbacks

If an expected tool is unavailable:

1. Record the limitation.
2. Use an approved fallback only when the workflow allows it.
3. Ask the user before continuing when the fallback weakens correctness materially.

## Validation

Before completion:

- Check output files exist.
- Check evidence exists for important claims.
- Check open questions are recorded.
- Check secrets are not exposed.
- Check memory writes are logged or explicitly skipped.
- Check the cost optimization checklist from `.ai/rules/13-efficiency-cost-policy-rules.md`.
- Check final response does not include full generated documentation.
<!-- END SOURCE: .ai/rules/05-workflow-execution-rules.md -->


## Source File: `.ai/rules/06-quality-gates.md`

<!-- BEGIN SOURCE: .ai/rules/06-quality-gates.md -->
# 06 Quality Gates

## Summary

This rule defines mandatory conditions before a workflow can be considered complete.

## General Gates

Before finishing any workflow, verify:

- The selected skill and workflow were resolved through the registry.
- Required rules were applied.
- Allowed write paths were respected.
- Runtime limitations are documented.
- User-facing chat response is in Vietnamese.
- The cost optimization checklist was applied.

## Source-Code Gates

For source-code reading, documentation, debugging, refactoring, or API creation:

- CodeGraph preflight was attempted.
- If CodeGraph was unavailable, user-approved fallback was used.
- Memory was retrieved before module analysis when memory tools were available.
- Project summary docs were read before deeper source reads when present.
- File reads were narrowed to the current task scope.
- Current source code was treated as the source of truth.
- Important claims include file or command evidence.
- Inferences are labeled.
- Unknowns are listed as open questions.

## Memory Gates

- Project namespace is used.
- No secrets are stored.
- No large raw source code is stored.
- Only verified durable findings are saved.
- Memory writes are logged.
- Conflicting memory is updated or flagged for review/delete.

## Documentation Gates

- The documentation covers only evidence-backed areas.
- Missing areas are marked as not detected instead of fabricated.
- Final output includes readiness.
- Final response summarizes files and status rather than pasting full docs.

## API Gates

For API changes:

- Existing route/controller/service patterns were checked.
- Auth, validation, middleware, and error conventions were preserved.
- Request/response contracts were confirmed or documented.
- Tests or smoke checks were added or updated when feasible.
- API docs/OpenAPI/Postman files were updated when the repo already maintains them.

## Cost Gates

- Memory was searched before scanning code.
- `docs/PROJECT_CONTEXT.md` was read when present.
- Whole-repository reading was avoided unless necessary.
- Git diff was used for review or commit tasks involving existing changes.
- Strong reasoning was reserved for difficult analysis, security, architecture, debugging, or multi-file refactoring.
- Reusable findings were summarized into memory or project docs.

## Readiness Levels

- `Ready`: All required outputs exist, evidence is sufficient, and no blocking unknowns remain.
- `Partial`: Useful output exists but some evidence, validation, or tool support is incomplete.
- `Blocked`: Execution cannot continue without user input or missing external capability.
<!-- END SOURCE: .ai/rules/06-quality-gates.md -->


## Source File: `.ai/rules/07-agent-review-rules.md`

<!-- BEGIN SOURCE: .ai/rules/07-agent-review-rules.md -->
# 07 Agent Review Rules

## Vietnamese User Summary

Rule này hướng dẫn agent reviewer kiểm tra lại kết quả của các agent khác.

## Review Stance

The reviewer must prioritize:

- Incorrect claims.
- Missing evidence.
- Cross-file inconsistencies.
- Security risks.
- Missing tests or validation.
- Unclear ownership or unresolved open questions.

## Review Method

1. Read the workflow and assigned outputs.
2. Check whether each agent stayed within scope.
3. Compare claims against source evidence.
4. Check handoff questions and conflicts.
5. Assign readiness.
6. Write a concise review summary.

## Findings Format

For each issue, include:

- Severity.
- File path and line when available.
- Claim or behavior under review.
- Evidence.
- Recommended correction.

## Reviewer Boundaries

- Do not silently rewrite another agent's findings unless the workflow assigns synthesis to the reviewer.
- Do not fabricate missing evidence.
- Do not downgrade security concerns without evidence.
- Do not mark `Ready` when critical checks were skipped.
<!-- END SOURCE: .ai/rules/07-agent-review-rules.md -->


## Source File: `.ai/rules/08-model-routing-rules.md`

<!-- BEGIN SOURCE: .ai/rules/08-model-routing-rules.md -->
# 08 Model Routing Rules

## Vietnamese User Summary

Rule này quy định cách chọn model/tier cho từng agent để cân bằng chi phí và độ chính xác.

## Model Classes

- `FAST_CHEAP`: Use for broad scans, file inventory, simple extraction, and low-risk summaries.
- `BALANCED`: Use for normal reasoning, moderate cross-file analysis, and most implementation work.
- `REASONING_STRONG`: Use for synthesis, conflict resolution, security-sensitive analysis, production-critical decisions, and final review.
- `LONG_CONTEXT_STRONG`: Use when the task needs large context plus strong synthesis.

## Routing Principles

- Use the cheapest model that can satisfy the required correctness.
- Use small or cheap models for discovery, file classification, keyword search, summarization, formatting, checklist generation, simple edits, simple curl generation, and commit message drafting.
- Use strong models only after the relevant scope has been narrowed.
- Escalate when evidence is conflicting, source is large, behavior is critical, or reasoning depends on multiple modules.
- Final reviewer and final handbook writer should use `REASONING_STRONG` or `LONG_CONTEXT_STRONG` when available.
- If the runner does not support per-agent model selection, record the limitation.

## Antigravity Gemini-Only Rule

For Google Antigravity runs, route `source-code-handover` and `make-new-dev-docs` through Gemini models only.

- Do not use `Claude Opus 4.6 Thinking`.
- Do not use `Claude Sonnet 4.6 Thinking`.
- Prefer `Gemini 3.5 Flash (Medium)` for normal discovery/findings after deterministic tools narrow the scope.
- Prefer `Gemini 3.5 Flash (High)` for Agents 2, 3, 5, 6, 7, 8, 9, and 10, and for high-risk business/auth/API/Redis/job/migration evidence.
- Use `Gemini 3.5 Flash (Low)` only for low-risk inventory classification, formatting, and checklist normalization.
- Use `Gemini 3.1 Pro (High)` only as a Gemini-family fallback for complex synthesis/review when `Gemini 3.5 Flash (High)` is unavailable or performs poorly.
- Use `Gemini 3.1 Pro (Low)` only for low-risk helper tasks; it is not acceptable for final synthesis or final validation on non-trivial repositories.

If an Antigravity runner proposes a non-Gemini model, override it to the closest Gemini tier and record the override in `STATUS.md`.

## Required Logging

Each agent should record:

- Requested model class.
- Actual model used when known.
- Reason for escalation or downgrade.
- Impact on readiness.

## Readiness Constraint

If critical review or final synthesis cannot be run with a sufficiently capable model, final readiness must not exceed `Partial` unless the source evidence is simple and fully verified.
<!-- END SOURCE: .ai/rules/08-model-routing-rules.md -->


## Source File: `.ai/rules/09-model-trigger-rules.md`

<!-- BEGIN SOURCE: .ai/rules/09-model-trigger-rules.md -->
# 09 Model Trigger Rules

## Vietnamese User Summary

Rule này cho phép người dùng chọn chế độ tiết kiệm, cân bằng hoặc chính xác cao khi chạy workflow.

## Trigger Modes

Trigger phrases may request one of these modes:

- `LOW_COST`: prioritize cost savings.
- `BALANCED_BUDGET`: default mode.
- `HIGH_ACCURACY`: prioritize correctness and stronger review.

Vietnamese trigger aliases may appear in `.ai/registry/triggers.yml`; keep the routing instructions here in English.

## Selection

- If the user explicitly asks for a mode, use it.
- If no mode is specified, use `BALANCED_BUDGET`.
- If the requested mode conflicts with safety or correctness requirements, escalate to the safer model class and record why.

## Output

Record the selected mode in workflow status and final summary.
<!-- END SOURCE: .ai/rules/09-model-trigger-rules.md -->


## Source File: `.ai/rules/10-codegraph-first-rules.md`

<!-- BEGIN SOURCE: .ai/rules/10-codegraph-first-rules.md -->
# 10 CodeGraph-First Rules

## Summary

This rule requires checking and using CodeGraph before source-code review. If CodeGraph is unavailable and cannot be initialized, the agent must ask before using a weaker fallback.

## Requirement

For any task that scans, documents, debugs, refactors, or changes source code, run CodeGraph preflight before broad source-code review.

## Preflight

1. Check whether CodeGraph tooling is available in the current agent environment.
2. Check whether the project has an initialized CodeGraph index.
3. If the index is missing, initialize it using the available CodeGraph setup command.
4. If initialization succeeds, use CodeGraph exploration/search before raw file search for architecture and symbol-level understanding.
5. If CodeGraph is unavailable or initialization fails, stop and ask the user whether to continue without CodeGraph or use another tool.

## Approved Fallback Behavior

Only use `rg`, language server search, IDE search, or manual file reads as a replacement after:

- CodeGraph was attempted, and
- The limitation was recorded, and
- The user approved continuing without CodeGraph when correctness may be affected.

## Documentation Integrity

When CodeGraph is unavailable:

- Mark the output as having reduced confidence.
- Cite the fallback tools used.
- Avoid broad architecture claims unless independently verified from source.

## Do Not

- Do not pretend CodeGraph was used when it was not.
- Do not fabricate symbol relationships.
- Do not skip CodeGraph because `rg` is faster.
- Do not continue silently after automatic CodeGraph setup fails.
<!-- END SOURCE: .ai/rules/10-codegraph-first-rules.md -->


## Source File: `.ai/rules/11-skillflow-extension-rules.md`

<!-- BEGIN SOURCE: .ai/rules/11-skillflow-extension-rules.md -->
# 11 Skillflow Extension Rules

## Vietnamese User Summary

Rule này chuẩn hóa cách thêm skillflow mới để không ảnh hưởng skill, agent hoặc workflow hiện có.

## Naming

- Use a unique kebab-case `skillflow_id`, such as `source-code-handover`, `security-review`, or `test-generation`.
- Avoid generic names such as `docs`, `agent`, or `workflow`.
- Place the workflow at `.ai/workflows/<skillflow_id>.md`.
- Place dedicated agents under `.ai/agents/<skillflow_id>/` when needed.

## Registry

Every new skillflow must be registered in:

- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`

Do not add a trigger only inside a standalone rule file.

## Output Namespace

New skillflows must not write into another skillflow's output or handoff paths.

Preferred runtime namespace:

```text
.ai/runs/<skillflow_id>/<run_id>/
```

If a workflow writes user-facing output to `docs/` or another public path, it must explicitly list allowed write paths.

## Required Files

A minimal skillflow needs:

- A Superpowers-style `SKILL.md`.
- A workflow file.
- Registry entries.
- Trigger aliases.
- Allowed write paths.
- Quality gates.
- Fallback behavior.

## Superpowers Style

- Do not create a separate `superpower` capability concept.
- Treat Superpowers as a methodology: check available skills, read the selected skill, then follow it.
- A skill may declare `REQUIRED BACKGROUND` or `REQUIRED SKILL`.
- Keep `SKILL.md` concise. Move long details to directly referenced files.
- Frontmatter must contain only `name` and `description`.
- The `description` must start with `Use when...`.

## Isolation

When adding a skillflow:

- Do not modify unrelated agent specs.
- Do not change legacy output paths without a migration.
- Do not delete existing handoff or runtime state unless requested.
- Add shared rules only when they are backward-compatible.

## Required Policies

Source-reading skillflows must follow:

- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Readiness Checklist

- [ ] Skill, workflow, and trigger are registered.
- [ ] Trigger does not conflict with existing workflows.
- [ ] Output namespace is isolated.
- [ ] Skill description starts with `Use when...`.
- [ ] Memory Policy is included when project knowledge is used.
- [ ] Efficiency and Cost Policy is included.
- [ ] Allowed write paths are listed.
- [ ] Quality gates are defined.
- [ ] Fallback behavior is defined.
- [ ] Adapter notes exist when tool behavior differs.
<!-- END SOURCE: .ai/rules/11-skillflow-extension-rules.md -->


## Source File: `.ai/rules/12-memory-policy-rules.md`

<!-- BEGIN SOURCE: .ai/rules/12-memory-policy-rules.md -->
# 12 Memory Policy Rules

## Summary

This rule defines memory usage: store only durable, verified, project-namespaced information and never store secrets.

## Core Policy

Use memory tools only for durable, reusable, verified information.

Do not use memory as a temporary log, source-code cache, secret store, or place for unverified guesses.

## Required Flow

For source reading, documentation, debugging, refactoring, and API creation:

1. Initialize MCP Memory before the first operation when runtime memory state is missing.
2. Retrieve memory.
3. Scan current source code.
4. Compare memory with code.
5. Use code as the source of truth.
6. Write or update docs/code.
7. Store confirmed findings back to memory.

## MCP Memory Bootstrap

The default MCP Memory bootstrap command was created on `2026-06-20`.

Agents must run or verify this command before any coding, documentation, debugging, review, refactor, commit, or analysis task when `.ai/runtime/memory/memory.jsonl` or `.ai/runtime/mcp-servers.json` is missing:

```bash
ai-agent-sync --install-tools --yes
```

If `ai-agent-sync` is not in `PATH`, run this from the repository root:

```bash
bin/ai-agent-sync --install-tools --yes
```

The command must:

- Install or verify `mcp-server-memory`.
- Create or verify `.ai/runtime/memory/memory.jsonl`.
- Write or verify `.ai/runtime/mcp-servers.json`.
- Configure the `mcp-memory` server with `MEMORY_FILE_PATH` pointing to `.ai/runtime/memory/memory.jsonl` inside the current repository.

If automatic initialization fails, record the limitation in run status and final response, then ask the user before continuing with repo-local docs as a weaker fallback.

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
<!-- END SOURCE: .ai/rules/12-memory-policy-rules.md -->


## Source File: `.ai/rules/13-efficiency-cost-policy-rules.md`

<!-- BEGIN SOURCE: .ai/rules/13-efficiency-cost-policy-rules.md -->
# 13 Efficiency And Cost Policy Rules

## Vietnamese User Summary

Rule này giúp giảm chi phí và token: không đọc lại toàn bộ repo mỗi lần, dùng model nhỏ cho bước đơn giản, model mạnh chỉ cho phần khó.

## Core Principle

Minimize token usage and avoid repeated full-repository scans.

Use this flow by default:

```text
User request
  -> Skill Router
  -> Memory Search
  -> Narrow Code/File Search
  -> Small model for classification or preliminary analysis
  -> Strong model only for difficult reasoning
  -> Save verified findings or decisions to memory
  -> Update docs or code
```

## Before Reading Files

1. Search memory for existing project facts.
2. Read `docs/PROJECT_CONTEXT.md` if it exists.
3. Read `docs/FINDINGS.md` and `docs/DECISIONS.md` if relevant.
4. Identify the smallest set of files needed for the current task.

## File Reading Rules

Do not read the whole repository unless explicitly required.

Prefer this order:

1. Entry point files.
2. Routing/controller files.
3. Service/use-case files.
4. Repository/database files.
5. Config files.
6. Tests and logs only when needed.

## Model Usage Rules

Use cheaper or smaller reasoning for:

- File discovery.
- File classification.
- Keyword search.
- Summarization.
- Formatting.
- Checklist generation.
- Simple code edits.
- Simple curl generation.
- Commit message drafting.
- Filename normalization.

Use stronger reasoning only for:

- Complex business logic analysis.
- Difficult debugging.
- Architecture decisions.
- Multi-file refactoring.
- Security-sensitive review.
- Legacy vs new-code comparison.
- Race condition, cache, queue, or background-job analysis.
- Safe migration design.

## Scope Strategy

Use a small model or deterministic tool to find the relevant scope first. Use a stronger model only on that narrowed scope.

## Memory Rules

Store only verified reusable facts:

- Architecture decisions.
- Database meanings.
- API flow summaries.
- Background job behavior.
- Known bugs and root causes.
- Naming conventions.
- Migration rules.

Do not store:

- Secrets.
- Raw source code.
- Temporary logs.
- Unverified guesses.
- Large stack traces.

## Context Compression Rules

After analyzing a module, write a short reusable summary:

- What was analyzed.
- Important files.
- Confirmed behavior.
- Risks.
- What still needs verification.

Reuse this summary in later steps instead of rereading all files.

## Diff-Based Review

For code review before commit:

1. Use git diff first.
2. Read only changed files.
3. Read directly dependent files only when needed.
4. Review logic, security, performance, and tests.
5. Draft the commit message in Vietnamese when requested by the user.

Do not review the whole repository unless the change requires it.

## Large Refactor Strategy

For large refactors:

1. Inventory all usages.
2. Create a checklist.
3. Apply changes in small groups.
4. Test each group.
5. Update memory and docs.

Do not refactor the entire repository in one uncontrolled pass.

## Recommended Project Docs

Each project should maintain:

- `docs/PROJECT_CONTEXT.md`
- `docs/ARCHITECTURE_SUMMARY.md`
- `docs/DATABASE_SUMMARY.md`
- `docs/API_SUMMARY.md`
- `docs/JOBS_SUMMARY.md`
- `docs/DEBUG_PLAYBOOK.md`
- `docs/DECISIONS.md`
- `docs/FINDINGS.md`

## Done Rule

At the end of the task, update memory or project docs with reusable findings so future tasks start faster.

## Cost Optimization Checklist

- [ ] Memory was searched before scanning code.
- [ ] `docs/PROJECT_CONTEXT.md` was read when present.
- [ ] The whole repository was not read for a module-scoped task.
- [ ] File reading was limited to the smallest useful set.
- [ ] Git diff was used when the task involved existing code changes.
- [ ] Findings were summarized for reuse.
- [ ] Durable information was written to memory or docs.
- [ ] Secrets, logs, and large raw code were not stored in memory.
- [ ] Strong models were not used for simple formatting or summarization steps.
<!-- END SOURCE: .ai/rules/13-efficiency-cost-policy-rules.md -->


## Source File: `.ai/rules/14-tdd-first-feature-rules.md`

<!-- BEGIN SOURCE: .ai/rules/14-tdd-first-feature-rules.md -->
# 14 TDD-First Feature Rules

## Vietnamese User Summary

Rule này bắt buộc mọi endpoint/tính năng backend mới phải brainstorm, chốt contract và có test plan trước khi implement.

## Mandatory Gate

For every new backend feature, endpoint, service method, database-backed flow, integration flow, callback, webhook, job, or business capability:

```text
No brainstorm + no contract + no test plan = no production implementation.
```

## Required Sequence

1. Brainstorm feature behavior.
2. Define the API or behavior contract.
3. Define acceptance criteria.
4. Create a test matrix.
5. Write failing tests first when test infrastructure exists.
6. Implement minimal production code.
7. Refactor safely.
8. Review the diff.
9. Update docs and memory.

## Production Code Restriction

Do not edit production code for a new feature until these items are defined:

- Feature goal.
- API or behavior contract.
- Acceptance criteria.
- Test scenarios.
- Failure cases.
- Data impact.
- Authentication and permission impact.
- Backward compatibility impact.

If the repository has no automated test framework, create an executable regression plan with curl/Postman examples, SQL verification queries, or equivalent project-native checks before implementation.

## Routing

Requests containing intent such as new endpoint, add API, create feature, add flow, backend feature, service method, webhook, callback, integration flow, or equivalent Vietnamese trigger phrases must route to `developing-backend-feature-tdd`.

Do not route new-feature work directly to API analysis, refactoring, or implementation-only skills.

## Refactor Boundary

Do not perform broad refactoring while implementing a new feature. Refactor only when required to pass tests, preserve the contract, or remove duplication introduced by the feature.

## Review Requirement

When reviewing a diff that adds a new feature or endpoint, warn if there is no automated test, test plan, or executable regression check.
<!-- END SOURCE: .ai/rules/14-tdd-first-feature-rules.md -->


## Source File: `.ai/rules/15-agent-runtime-tool-policy.md`

<!-- BEGIN SOURCE: .ai/rules/15-agent-runtime-tool-policy.md -->
# 15 Agent Runtime Tool Policy

## Vietnamese User Summary

Rule này khóa cách agent dùng tool/runtime để tránh lỗi gọi tool sai schema, scan quá rộng, tự retry vô hạn, hoặc tạo tài liệu từ context thay vì source vật lý.

## Universal Tool-Call Contract

Before calling any tool, the agent MUST know the exact schema required by the active runtime.

If the runtime exposes a shell/command tool, the agent MUST provide every required field in one valid call. Do not emit partial, empty, or placeholder tool calls.

If a tool call fails because of malformed arguments:

1. Retry at most once with the complete required schema.
2. If the retry fails, stop that action.
3. Record the limitation in the workflow artifact.
4. Continue only with a documented fallback that does not pretend the failed tool succeeded.

Do not loop on the same malformed tool call.

## Command Safety Defaults

Safe local read/setup commands may run without user approval when the runtime permits it:

- `pwd`
- `ls`
- `rg`
- `rg --files`
- `git status`
- `git rev-parse`
- bounded `find <path> -maxdepth N`
- validation scripts under `.ai/scripts/`
- run initialization under `.ai/runs/`

High-risk commands require explicit user approval or an approved workflow gate:

- destructive git commands
- deploy/release commands
- database migration or data mutation commands
- production credentials or secret access
- external network operations that upload code or data
- package install commands when the environment policy requires approval

## Search And Scan Limits

Do not start with unbounded repository scans such as `find .` without exclusions or max depth.

Prefer:

```bash
rg --files
rg --files .ai/workflows
find .ai/workflows -maxdepth 1 -type f -name "*.md"
```

For large repositories, exclude generated/vendor/build folders before broad discovery:

```bash
rg --files -g '!bin/' -g '!obj/' -g '!node_modules/' -g '!dist/' -g '!build/'
```

## Source-Code Handover Minimum Tool Behavior

When running `source-code-handover` or `make-new-dev-docs`:

1. Initialize the run with `.ai/scripts/init-source-code-handover-run.sh`.
2. Agents 1-5 MUST discover from physical files and write inventory/findings artifacts.
3. Agents 6-8 MUST re-open physical source slices and tool outputs before verifying claims.
4. Agent 9 MUST write final docs from frozen evidence, not from vague model memory.
5. Agent 10 MUST audit evidence coverage and mark weak sections `REJECT`, `PARTIAL`, or `NOT_VERIFIED`.

## Runtime Limitation Recording

Every workflow that depends on tools MUST record missing or failed tools in a limitation artifact such as:

- `.ai/runs/<skillflow_id>/<run_id>/evidence/tool-limitations.json`
- `.ai/runs/<skillflow_id>/<run_id>/validation/tool-orchestration-validation.md`
- `.ai/runs/<skillflow_id>/<run_id>/STATUS.md`

The limitation record MUST include:

- tool name
- expected role
- attempted command or tool action
- error/failure mode
- impact on evidence quality
- fallback used

## Do Not

- Do not claim a tool was used when it was skipped or failed.
- Do not treat model context as evidence.
- Do not mark generated docs `Ready` when build/test/runtime evidence is missing.
- Do not publish final docs when required agent artifacts are absent.
- Do not broaden filesystem or network access to compensate for poor prompt routing.
<!-- END SOURCE: .ai/rules/15-agent-runtime-tool-policy.md -->


## Source File: `.ai/adapters/copilot.md`

<!-- BEGIN SOURCE: .ai/adapters/copilot.md -->
# GitHub Copilot Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` với GitHub Copilot Chat, Copilot code review và Copilot coding agent.

## Runtime Instructions

- Use generated repository instructions from `.github/copilot-instructions.md` when present.
- Use generated path-specific instructions from `.github/instructions/ai-framework.instructions.md` when present.
- Treat `.ai/registry/` as the source of truth for skill and workflow routing.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before workspace edits, terminal suggestions, pull request comments, or coding-agent actions.
- For Copilot coding agents that support `AGENTS.md`, also follow the repository root `AGENTS.md`.
- Run or verify `ai-agent-sync --install-tools --yes` before source-reading or code-changing tasks when runtime state is missing.
- Keep secrets out of generated instructions, chat responses, docs, memory, and pull request comments.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## Optimization Profile

- Best fit: inline coding help, pull request review, CI-aware suggestions, GitHub issue/PR context, and small scoped edits.
- Use `.github/instructions/ai-framework.instructions.md` as the deep framework bundle for Copilot contexts that support path-specific instructions.
- For broad documentation or multi-agent workflows, Copilot should create or update artifacts but must not claim build/test/runtime verification unless it has real command or CI evidence.
- Prefer GitHub-native evidence when available: commit, PR, workflow run, code scanning, Dependabot, and issue links.
- Do not expose secrets in PR comments or generated docs; redact values while preserving key names.
<!-- END SOURCE: .ai/adapters/copilot.md -->
