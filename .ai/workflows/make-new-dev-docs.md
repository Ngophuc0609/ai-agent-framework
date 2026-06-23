# Make New Developer Documentation Workflow

## Vietnamese User Summary

Workflow này tạo tài liệu bàn giao source code cho developer mới, bắt buộc sử dụng các session độc lập cho từng agent và kiểm tra file vật lý.

## Skill

Use `.ai/skills/source-code-handover/SKILL.md`.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/01-documentation-skill.md`
- `.ai/rules/02-multi-agent-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/07-handover-documentation-dod.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`

## Execution Modes

Workflow chỉ được dùng một trong ba mode sau theo thứ tự ưu tiên bắt buộc:

1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

Cấm tuyệt đối các mode/hành vi sau (forbidden legacy modes):
- `single-runtime-sequential-fallback`
- `single-session-multi-role-execution`
- `memory-only-agent-handoff`
- `implicit-agent-output`
- `direct-final-handbook-without-artifacts`

Nếu runtime không thể spawn real sub-agent và cũng không thể tạo session độc lập cho từng agent:
- Dừng trước Agent 1.
- Ghi trạng thái `blocked-no-isolation-capability`.
- Không được tạo `docs/01_PROJECT_HANDOVER_FULL.md`.
- Không được đánh dấu `Ready` hoặc `Partial`.
- Chỉ được tạo báo cáo block có lý do cụ thể và hướng dẫn chạy lại trong môi trường hỗ trợ session isolation.

## Final Documentation Targets

The workflow may produce:

- `docs/01_PROJECT_HANDOVER_FULL.md` (Overview/entry point)
- `docs/02_PROJECT_CONTEXT.md`
- `docs/03_REPOSITORY_GUIDE.md`
- `docs/04_LOCAL_SETUP.md`
- `docs/05_CONFIGURATION_REFERENCE.md`
- `docs/06_ARCHITECTURE.md`
- `docs/07_DATABASE_REFERENCE.md`
- `docs/08_AUTH_AND_SECURITY.md`
- `docs/09_API_CATALOG.md`
- `docs/10_BACKGROUND_JOBS.md`
- `docs/11_REALTIME_SIGNALR_SOCKET.md`
- `docs/12_EXTERNAL_INTEGRATIONS.md`
- `docs/13_FRONTEND_GUIDE.md`
- `docs/14_OPERATIONS_RUNBOOK.md`
- `docs/15_DEPLOYMENT_AND_CICD.md`
- `docs/16_TESTING_GUIDE.md`
- `docs/17_KNOWN_RISKS.md`
- `docs/18_OPEN_QUESTIONS.md`
- `docs/19_EVIDENCE_INDEX.md`
- `docs/20_DOCUMENTATION_COVERAGE.md`

**LANGUAGE REQUIREMENT**: All final markdown files generated in the `docs/` folder MUST be written entirely in Vietnamese (Tiếng Việt). Technical keywords, code snippets, and configuration keys should remain in English, but all prose, explanations, and headers must be in Vietnamese.

## Mode: subagent-isolated-worktrees

Khi runtime hỗ trợ real sub-agent:
- Mỗi Agent 1–5 phải chạy bằng một sub-agent/session riêng.
- Mỗi agent phải có workspace hoặc Git worktree riêng khi khả dụng.
- Agent 1–5 có thể chạy song song chỉ khi không ghi đè cùng file.
- Agent 6 chỉ được chạy sau khi Agent 1–5 đã hoàn tất và artifact gate pass.
- Agent 7 chỉ được chạy sau khi Agent 6 hoàn tất và review gate pass.

## Mode: isolated-sequential-sessions

Khi không thể spawn real sub-agent nhưng có khả năng tạo session độc lập:
- Mỗi Agent 1–7 phải chạy trong một session mới, độc lập với session trước.
- Session coordinator chỉ được quyền:
  - tạo run namespace;
  - khởi tạo trạng thái;
  - khởi chạy từng session agent;
  - kiểm tra artifact gate;
  - truyền path artifact cho agent kế tiếp;
  - ghi execution log;
  - dừng workflow khi gate fail.
- Session coordinator không được tự thực hiện nội dung khảo sát thay Agent 1–6.
- Agent sau chỉ được biết kết quả của agent trước thông qua file artifact trên disk, không thông qua nội dung context nội bộ của coordinator.

Chuỗi chạy bắt buộc:
Session A1 → ghi Agent 1 findings.md → verify gate
Session A2 → ghi Agent 2 findings.md → verify gate
Session A3 → ghi Agent 3 findings.md → verify gate
Session A4 → ghi Agent 4 findings.md → verify gate
Session A5 → ghi Agent 5 findings.md → verify gate
Session A6 → đọc artifact Agent 1–5 từ disk → ghi review.md → verify gate
Session A7 → đọc artifact Agent 1–6 từ disk → tạo final docs → verify final gate

Nếu một session agent không thể khởi tạo hoặc không hoàn thành artifact hợp lệ: Dừng chuỗi, ghi rõ agent nào fail và lý do vào status file. Không tạo final handbook.

## Allowed Write Paths

Agent 1–5 chỉ được ghi vào:
`.ai/runs/source-code-handover/<run_id>/findings/agent-01/`
`.ai/runs/source-code-handover/<run_id>/findings/agent-02/`
`.ai/runs/source-code-handover/<run_id>/findings/agent-03/`
`.ai/runs/source-code-handover/<run_id>/findings/agent-04/`
`.ai/runs/source-code-handover/<run_id>/findings/agent-05/`
`draft-docs/`

Agent 6 chỉ được ghi vào:
`.ai/runs/source-code-handover/<run_id>/review/`
`draft-docs/`

Agent 7 mới có quyền ghi vào:
`docs/`
`draft-docs/`
`.ai/handoff/`
`.ai/runs/source-code-handover/<run_id>/final/`

Không agent nào trong Agent 1–6 được ghi trực tiếp `docs/01_PROJECT_HANDOVER_FULL.md`.

## Mandatory Artifacts and Format

Mỗi agent bắt buộc tạo file Markdown vật lý tại CẢ HAI vị trí (hoặc ghi vào `.ai` rồi copy ra `draft-docs/`):
`.ai/runs/source-code-handover/<run_id>/findings/agent-01/findings.md` VÀ `draft-docs/agent-01-findings.md`
`.ai/runs/source-code-handover/<run_id>/findings/agent-02/findings.md` VÀ `draft-docs/agent-02-findings.md`
`.ai/runs/source-code-handover/<run_id>/findings/agent-03/findings.md` VÀ `draft-docs/agent-03-findings.md`
`.ai/runs/source-code-handover/<run_id>/findings/agent-04/findings.md` VÀ `draft-docs/agent-04-findings.md`
`.ai/runs/source-code-handover/<run_id>/findings/agent-05/findings.md` VÀ `draft-docs/agent-05-findings.md`
`.ai/runs/source-code-handover/<run_id>/review/review.md` VÀ `draft-docs/agent-06-review.md`
`.ai/runs/source-code-handover/<run_id>/final/01_PROJECT_HANDOVER_FULL.md`

Mỗi artifact phải:
- Tồn tại vật lý trên disk.
- Không rỗng.
- Có phần `Status`.
- Có phần `Evidence`.
- Có phần `Open Questions`.
- Có phần `Risks`.
- Có phần `Files Inspected` hoặc `Commands Executed`.
- Có timestamp hoặc run id.
- Không chứa secret thực tế.

Agent 1–5 còn phải có: `Scope`, `Confirmed Findings`, `Evidence`, `Assumptions`, `Open Questions`, `Risks`, `Status`.
Agent 6 phải có: `Inputs Reviewed`, `Completeness Check`, `Conflict Register`, `Unresolved Questions`, `Readiness Assessment`, `Reviewer Decision`, `Status`.
Agent 7 phải có: `Inputs Used`, `Final Documents Created`, `Open Questions Preserved`, `Limitations Preserved`, `Validation Result`, `Status`.

## Mandatory Disk I/O Gate

CRITICAL: An agent is not considered complete until its required Markdown artifact has been physically written to disk and successfully validated.
CRITICAL: Intermediate findings must never exist only in model context, temporary memory, chat history, or coordinator state.
CRITICAL: The next agent must not start until the previous agent artifact gate passes.
CRITICAL: Agent 7 must read Agent 1–6 artifacts from disk. It must not aggregate from hidden session context, remembered summaries, or implicit prior-agent results.

Validation tối thiểu trước khi qua phase tiếp theo:
- File exists.
- File size is greater than zero.
- Required headings exist.
- File contains at least one evidence reference, or an explicit documented Not Applicable reason.
- File path matches the current run_id.
- Status file is updated.

## Structured STATUS.md

Bắt buộc tạo và cập nhật file `.ai/runs/source-code-handover/<run_id>/STATUS.md`:

```md
# Source Code Handover Status

- Run ID: `<run_id>`
- Execution Mode: `subagent-isolated-worktrees | isolated-sequential-sessions | blocked-no-isolation-capability`
- Started At: `<timestamp>`
- Current Phase: `<phase>`

## Agent Status

| Agent | Session Isolation | Artifact Path | Status | Gate |
|---|---|---|---|---|
| Agent 1 | yes | draft-docs/agent-01-findings.md | pending/complete/blocked/not-applicable | pending/pass/fail |
| Agent 2 | yes | draft-docs/agent-02-findings.md | pending/complete/blocked/not-applicable | pending/pass/fail |
| Agent 3 | yes | draft-docs/agent-03-findings.md | pending/complete/blocked/not-applicable | pending/pass/fail |
| Agent 4 | yes | draft-docs/agent-04-findings.md | pending/complete/blocked/not-applicable | pending/pass/fail |
| Agent 5 | yes | draft-docs/agent-05-findings.md | pending/complete/blocked/not-applicable | pending/pass/fail |
| Agent 6 | yes | draft-docs/agent-06-review.md | pending/complete/blocked/not-applicable | pending/pass/fail |
| Agent 7 | yes | final/01_PROJECT_HANDOVER_FULL.md | pending/complete/blocked/not-applicable | pending/pass/fail |

## Blocking Reasons

- None / list concrete reason.

## Validation Summary

- Artifact gate: pass/fail
- Isolation gate: pass/fail
- Final documentation gate: pass/fail
```

Không được ghi `Session Isolation: yes` nếu thực tế agent chỉ là một role trong cùng context/session.

## Evidence Policy & Source of Truth

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`.
Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory is supplementary context only. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Agents

### Agent 1: Source And Local Setup

Use `.ai/agents/agent-01-source-local.md`.

### Agent 2: Database And Auth

Use `.ai/agents/agent-02-database-auth.md`.

### Agent 3: API And Postman

Use `.ai/agents/agent-03-api-postman.md`.

### Agent 4: Business And Frontend

Use `.ai/agents/agent-04-business-frontend.md`.

### Agent 5: Operations

Use `.ai/agents/agent-05-operation.md`.

### Agent 6: Coordinator Reviewer

Use `.ai/agents/agent-06-coordinator-reviewer.md`.

Agent 6 phải đọc trực tiếp file Agent 1–5 từ disk.
Agent 6 không được dựa vào summary trong chat, context của coordinator, mô tả không có artifact, kết quả được nói là đã hoàn thành nhưng không có file.
Nếu bất kỳ artifact Agent 1–5 thiếu hoặc gate fail: Agent 6 không được viết review hoàn chỉnh, chỉ được ghi trạng thái blocked (nêu chính xác artifact thiếu), và Agent 7 không được chạy.

### Agent 7: Single Handbook Aggregator

Use `.ai/agents/agent-07-single-handbook-aggregator.md`.

Agent 7 chỉ được chạy khi:
- Agent 1–5 artifact gate đều pass hoặc có `Not Applicable` hợp lệ.
- `review/review.md` tồn tại và gate pass.
- STATUS.md xác nhận isolation gate pass.
- Không có blocking conflict chưa được Agent 6 ghi nhận.

Agent 7 chỉ được tổng hợp từ artifact trên disk và không được thêm claim kỹ thuật mới nếu không có evidence trong Agent 1–6 outputs.

## Readiness

### Ready

Chỉ hợp lệ khi đáp ứng TẤT CẢ Definition of Done của handbook:
- Trả lời đầy đủ clone từ đâu, version tool chính xác là gì.
- Lệnh chạy local, URL/port, cấu hình secret cụ thể.
- Request đi qua những project nào, data flow/auth flow rõ ràng.
- Danh sách DbContext, cách chạy migration/seed data.
- API catalog chi tiết, test nào đã pass.
- Đã xác nhận Docker/Nginx topology, cấu hình log/Redis.
- Có Evidence Index với path/line/commit cụ thể.
- Mọi risk có bằng chứng và owner rõ ràng.
- Execution mode là `subagent-isolated-worktrees` hoặc `isolated-sequential-sessions`.
- Artifact gate của Agent 1–7 đều pass.
- Agent 6 review đã hoàn thành.
- Validation cuối pass.
- Không có conflict critical chưa xử lý.

### Partial

Chỉ hợp lệ khi:
- Session isolation vẫn được đảm bảo.
- Có một số giới hạn evidence, runtime access hoặc tool access.
- Agent outputs bắt buộc vẫn tồn tại và hợp lệ.
- Các giới hạn được nêu rõ trong final handbook.

### Blocked

Bắt buộc dùng khi:
- Không có sub-agent và cũng không có session isolation.
- Một artifact bắt buộc thiếu hoặc không hợp lệ.
- Agent 6 không thể review do thiếu input.
- Agent 7 bị chặn bởi gate.
- Có critical conflict không thể xác minh.

Không được đánh dấu `Ready` hoặc `Partial` trong mode `blocked-no-isolation-capability`.

## Final Validation

Final validation must include:
- git diff --check
- markdown link validation where available
- required output existence check
- STATUS.md consistency check
- no secret scan
- no unresolved conflict omitted from final handbook
- stack-appropriate build or test commands when environment permits.
