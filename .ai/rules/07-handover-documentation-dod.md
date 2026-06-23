# Documentation Definition of Done (DoD)

Một tài liệu bàn giao “đủ” không chỉ là mô tả công nghệ hay liệt kê thư mục. Nó phải giúp developer mới trả lời được, với mỗi thành phần quan trọng:

- Có gì trong hệ thống? — inventory đầy đủ.
- Nó nằm ở đâu trong source? — file/class/method/migration có bằng chứng.
- Nó hoạt động như thế nào? — contract, luồng xử lý, sequence diagram.
- Sửa, chạy, test và vận hành nó thế nào? — runbook thực tế.
- Thông tin này được xác minh ra sao? — evidence, commit, command/test result, limitation.

Mọi agent tham gia quá trình Handover phải tuân thủ nghiêm ngặt chuẩn này.

## 1. Quy tắc chung: mỗi claim phải có Evidence

Mọi tài liệu chuyên sâu cần dùng cùng một format bằng chứng.

- Status: Confirmed | Inferred | Unverified | Conflict | Not Applicable
- Evidence:
  - Source: `src/.../SomeFile.cs:L20-L75`
  - Runtime/Test: `dotnet test ...` — passed on `<date>`
  - Database: schema inspection / migration `<migration-name>`
- Verified at commit: `<git sha>`
- Last verified: `<timestamp>`

Tuyệt đối KHÔNG ĐƯỢC ghi chung chung kiểu "Dự án có Redis". Phải ghi chi tiết có file, dòng, và runtime impact.

## 2. Bộ tài liệu mục tiêu

- `docs/01_PROJECT_HANDOVER_FULL.md`
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

`01_PROJECT_HANDOVER_FULL.md` chỉ là entry point tóm tắt và dẫn link đến các tài liệu chi tiết.

## 3. Definition of Done cho tài liệu Database

### 3.1. Database topology
Bắt buộc có:
- Bảng: `DbContext | Database/Connection Key | Project | Mục đích | Migration Assembly | Evidence | Status`.

### 3.2. Inventory entity, table, migration
- Phải quét DbContext, DbSet, Fluent API, Migrations, Seed data, Raw SQL. Tạo Database Discovery Coverage.

### 3.3. Data dictionary theo bảng/entity
- Mục đích, PK, FK, Index, Audit fields, Soft delete, Sensitive fields.
- Bảng chi tiết: `Field | DB Type | C# Type | Nullable | Default | PK/FK | Index/Unique | Sensitive | Mô tả | Evidence`.

### 3.4. ERD và quan hệ dữ liệu
- Tạo Mermaid ERD cho các module chính. Quan hệ 1-N, N-N, Cascade, Bridge tables.

### 3.5. Migration/seed runbook
- Lệnh cụ thể tạo/apply/rollback migration. Cách tạo tài khoản admin đầu tiên, cách reset DB local.

## 4. Definition of Done cho Background Jobs

### 4.1. Job inventory
- Bảng: `Job ID | Job/Class | Trigger Type | Schedule | Registration Source | Entry Method | Module | Status`.

### 4.2. Job card bắt buộc
- Mục đích, Cron, Dependencies, Retry, Idempotency, Concurrency, Failure behavior, Monitoring, Risks, Evidence.

### 4.3. Sequence diagram
- Phải có diagram cho các job critical.

## 5. Definition of Done cho SignalR / Socket / Realtime

### 5.1. Hub inventory
- Bảng: `Hub ID | Hub Class | Route | Host Application | Auth/Policy | Transport | Evidence | Status`.

### 5.2. Connection contract
- Auth method, URL, CORS, Reconnect policy, Backplane/scale-out, Sticky session.

### 5.3. Event contract hai chiều
- Bảng cho Client->Server và Server->Client với Payload DTO.

### 5.4. Smoke test & Sequence diagrams
- Flow connect, authenticate, multi-instance broadcast. Hướng dẫn test.

## 6. Definition of Done cho API Catalog

### 6.1. Endpoint discovery
- Quét toàn bộ MVC, Minimal, Swagger, OIDC, Webhooks. Tạo API Discovery Coverage.

### 6.2. Endpoint card & Parameters
- Bảng: `API ID | Route | Method | Auth | DTOs | Status codes | Validation | Side effects`.
- Request params: `Parameter | In | Type | Required | Validation | Example | Evidence`.

### 6.3. Sample request/response
- JSON mẫu lấy từ DTO thật. Error format chuẩn.

### 6.4. API flow diagrams
- Diagrams cho security/business critical APIs.

## 7. Definition of Done cho Auth & Security

- Scheme, Issuer, Signing credential source (không lộ key).
- Client inventory, Grant types, Scopes, PKCE, Role->Policy map.
- External providers callback paths, claims mapping.
- Anonymous endpoint inventory, CORS/Rate limit/Password policy.

## 8. Definition of Done cho Configuration & Local Setup

- Configuration Matrix: `Config Key | Project | Local Required | Production Required | Secret | Source/Precedence | Mô tả | Evidence`.
- Local Setup phải có commands copy-paste được, exact versions cho Tools/SDKs, port maps, database seed steps, certificates.

## 9. Definition of Done cho Operations & CI/CD

- Topology Docker/Nginx, Volumes, Healthchecks, Logging sinks.
- Incident runbooks cho DB down, Redis down, Mail failed, Login failed.
- Phải rà soát file CI/CD (GitHub Actions/GitLab/Jenkins). Nếu không có ghi rõ "[CONFIRMED] Không tìm thấy".

## 10. External Integrations & Testing

- Bảng Integration card cho 3rd party APIs (SMTP, Zalo, SMS, Identity).
- Bảng Test Inventory: Unit, Integration, Smoke, Load test commands và expected results.

## 11. Known Risks, Open Questions & Evidence Index

- Risk Register: Phải có Chủ sở hữu (Owner), Tác động (Impact), Tiền đề khai thác (Exploit preconditions), Cách xử lý (Remediation).
- Questions: Gắn Owner, Evidence đã tìm, Mức độ Blocking.
- Evidence Index: Liệt kê chi tiết mọi ID bằng chứng, claim, file source/line.

## 12. Documentation Coverage Manifest (20_DOCUMENTATION_COVERAGE.md)

File bắt buộc phải sinh ra để thống kê % Entity, API, Job, Realtime Hubs đã được document.

## 13. Chuẩn đánh giá Ready / Partial / Blocked

- **Ready**: Phủ 100% components tìm thấy, mọi thứ có source evidence, API/DB/Jobs có contract, Setup runbook thực tế chạy được.
- **Partial**: Phân tích đáng kể nhưng có hạn chế môi trường/runtime, dev chạy được local nhưng chưa đủ tự vận hành prod độc lập.
- **Blocked**: Không tìm thấy entry point/schema, thiếu artifact source.
