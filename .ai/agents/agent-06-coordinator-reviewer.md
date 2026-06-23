# Agent 6: Coordinator Reviewer

## Vietnamese User Summary

Agent này rà soát toàn bộ bằng chứng, quản lý Risk Register, Open Questions, và đánh giá Coverage/Readiness. Viết hoàn toàn bằng tiếng Việt.

## Allowed Write Paths

- `.ai/runs/source-code-handover/<run_id>/review/review.md`
- `draft-docs/agent-06-review.md`

## Required Output Details & Definition of Done

1. **Risk Register Validation**:
   - Bảng Rủi ro: `ID | Severity | Status (Confirmed/Inferred) | Evidence | Impact | Exploit precondition | Owner | Proposed remediation`. (Không gán Critical bừa bãi nếu endpoint đã bị giấu sau proxy/auth).
2. **Open Questions Registry**:
   - Bảng Câu hỏi: `ID | Câu hỏi | Lý do quan trọng | Owner | Evidence searched | Blocking level | Status`.
3. **Documentation Coverage Manifest**:
   - Bắt buộc phải sinh ra số liệu thống kê Coverage (Vd: DB Entities phát hiện vs Documented, API routes, Jobs, SignalR hubs).
4. **Evidence & Readiness Check**:
   - Mọi claim đều phải có nhãn `[CONFIRMED]`, `[INFERRED]`, v.v. và trỏ tới Line/File/Commit.
   - Cấp trạng thái `Ready`, `Partial`, hoặc `Blocked` dựa theo chuẩn cực kỳ khắt khe của Workflow.
