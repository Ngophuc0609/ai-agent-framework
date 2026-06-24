# Source Code Handover Final Document Template

Agent 7 MUST use this template for every final document in:

```text
.ai/runs/source-code-handover/<run_id>/final/
```

Do not remove sections. If a section has no content, write `Không có.` or a valid `[NOT_APPLICABLE]` block with negative evidence.

This template defines the developer-facing final document body. Rendered final documents MUST be written in Vietnamese, while technical identifiers, paths, commands, config keys, API routes, JSON keys, database names, Evidence IDs, code blocks, stack traces, and Mermaid syntax keywords remain unchanged.

```md
---
document_id: "DOC-NN"
title: "<Vietnamese title>"
run_id: "<run_id>"
source_commit: "<git_sha>"
source_branch: "<branch>"
status: "Ready | Partial | Blocked | Not Applicable"
primary_owner_agent: "agent-XX"
evidence_ids:
  - "EV-XXX-001"
last_verified_at: "<ISO-8601 timestamp>"
---

# <Vietnamese document title>

## Phạm vi

| Hạng mục | Nội dung |
|---|---|
| Tài liệu | `<NN_doc_name.md>` |
| Repository | `<repo-name>` |
| Source commit | `<git_sha>` |
| Agent phụ trách chính | `agent-XX` |
| Phạm vi | `<what this document covers>` |
| Ngoài phạm vi | `<what this document does not cover>` |

## Trạng thái

| Mục | Giá trị |
|---|---|
| Readiness | Ready / Partial / Blocked / Not Applicable |
| Lý do | `<short reason>` |
| Coverage liên quan | `<summary from 20_documentation_coverage.md>` |

## Nguồn dữ liệu / Evidence

| Evidence ID | Claim | Source path | Line/method | Verification type | Status |
|---|---|---|---|---|---|
| EV-XXX-001 | `<claim>` | `<path>` | `<line/method>` | Source / Config / Runtime / Negative evidence | [CONFIRMED] |

## Nội dung chính

### <Section title>

[CONFIRMED] <Evidence-backed content written for a new developer.>

Evidence:
- EV-XXX-001

<Use tables, cards, runbooks, and diagrams required by `.ai/rules/08-source-code-handover-quality-checklist.md`.>

### Hành vi nghiệp vụ và compatibility

| Hạng mục | Nội dung | Evidence | Trạng thái |
|---|---|---|---|
| Business rule | `<rule summary or BR-ID>` | EV-XXX-001 | [CONFIRMED] / [UNVERIFIED] / [CONFLICT] / [DECISION] |
| Data read/write | `<tables/columns/cache/jobs/external systems>` | EV-XXX-001 | [CONFIRMED] |
| Auth/permission | `<where auth or authorization is checked>` | EV-XXX-001 | [CONFIRMED] |
| Behavior phải giữ | `<migration compatibility requirement>` | EV-XXX-001 | [DECISION] |

### Migration / Rollback Notes

| Behavior / Module | Must not change | Baseline proof | .NET 8 target risk | Rollback plan | Owner | Evidence | Status |
|---|---|---|---|---|---|---|---|
| `<module>` | `<behavior>` | `<test/smoke/data comparison>` | `<risk>` | `<rollback action>` | `<owner>` | EV-XXX-001 | [CONFIRMED] / [UNVERIFIED] / [DECISION] |

## Hạn chế

| Hạn chế | Tác động | Evidence | Trạng thái |
|---|---|---|---|
| `<limitation>` | `<impact>` | EV-XXX-001 | [UNVERIFIED] / [BLOCKED] |

## Câu hỏi mở

Không có.

<!-- Or use this table when questions exist:
| Question ID | Câu hỏi | Tại sao quan trọng | Evidence đã tìm | Suggested owner | Blocking level | Status | Next action |
|---|---|---|---|---|---|---|---|
| Q-XXX-001 | `<question>` | `<impact>` | EV-XXX-001 | `<owner>` | Critical / High / Medium / Low | Open | `<next action>` |
-->

## Rủi ro

Không có rủi ro riêng ngoài các mục đã ghi trong `17_known_risks.md`.

<!-- Or use this table when risks exist:
| Risk ID | Severity | Status | Evidence | Impact | Exploit/failure precondition | Owner | Remediation | Target/next step |
|---|---|---|---|---|---|---|---|---|
| RISK-XXX-001 | High | [CONFIRMED] | EV-XXX-001 | `<impact>` | `<precondition>` | `<owner>` | `<remediation>` | `<next step>` |
-->
```

## Pass Criteria

- Front matter is complete and `document_id` matches the filename number.
- The seven common sections exist in order.
- Required document-specific tables/cards/diagrams from the checklist are present.
- No example value remains.
- Every Evidence ID exists in `19_evidence_index.md`.
- Missing components use negative evidence, not vague prose.
