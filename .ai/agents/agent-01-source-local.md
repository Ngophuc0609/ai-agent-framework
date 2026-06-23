# Agent 1: Source And Local Setup

## Vietnamese User Summary

Agent này xây dựng nền tảng: Repository, Local Setup, Configuration Matrix, Deployment/CI/CD và Testing Guide. Yêu cầu chi tiết tuyệt đối, có bằng chứng cho từng dòng lệnh. Viết hoàn toàn bằng tiếng Việt.

## Allowed Write Paths

- `.ai/runs/source-code-handover/<run_id>/findings/agent-01/findings.md`
- `draft-docs/agent-01-findings.md`

## Required Output Details & Definition of Done

Mỗi thành phần phải trả lời đủ 8 câu hỏi cốt lõi: Có gì? Ở đâu? Input? Output? Luồng? Cấu hình/quyền? Test/chạy thế nào? Bằng chứng đâu?

1. **Repository Guide**: 
   - Danh sách Project/Module, Vai trò, Entry point, Dependency chính, Thay đổi thường gặp.
   - Project reference graph, vị trí đặt assets, docker, certs.
2. **Local Setup Runbook**:
   - Version bắt buộc: .NET SDK, Node.js, npm, Gulp, Docker, SQL Server (có dẫn chứng file).
   - Lệnh chạy chính xác cho từng Terminal (copy-pasteable), working directory, expected URLs (HTTP/HTTPS/Swagger).
   - Troubleshooting: Các lỗi cài đặt phổ biến (trust cert, node-sass, port conflict) và cách sửa.
3. **Configuration Matrix**:
   - Bảng: `Key | Project | Local required | Prod required | Secret | Nguồn | Mô tả`.
4. **CI/CD & Deployment**:
   - Tìm kiếm GitHub Actions/Jenkins/GitLab. Nếu không có phải ghi `[CONFIRMED] Không tìm thấy...`.
   - Image registry, deployment approval, secret injection.
5. **Testing Strategy**:
   - Bảng: `Test type | Command | Requirement | Expected result | Evidence`. Unit/Integration/Smoke tests. Known failing tests.
