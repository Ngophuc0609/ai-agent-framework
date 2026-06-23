# Agent 3: API And Postman

## Vietnamese User Summary

Agent này thiết lập API Catalog chuẩn xác từ source, cùng hướng dẫn Smoke Test. Viết hoàn toàn bằng tiếng Việt.

## Allowed Write Paths

- `.ai/runs/source-code-handover/<run_id>/findings/agent-03/findings.md`
- `draft-docs/agent-03-findings.md`

## Required Output Details & Definition of Done

1. **API Endpoint Catalog**:
   - Bảng đầy đủ mọi endpoint: `Area | Method | Route | Auth policy | Request DTO | Response DTO | Error codes | Side effects`.
   - Request parameter contract (Type, Validation, Required).
   - Response contract: JSON format lấy từ DTO/Swagger. KHÔNG ĐƯỢC TỰ BỊA. Error format chuẩn.
2. **Anonymous Endpoint Inventory**:
   - Lọc riêng các endpoint không cần auth: `Route | Method | Lý do | Rate limit | Caller | Security review`.
3. **API Flow & Conventions**:
   - Versioning, Base paths, Pagination conventions, Idempotency.
   - Flow diagram cho endpoint quan trọng.
4. **API Coverage Gate**:
   - Thống kê: Số Controller, Actions, Minimal APIs, Health routes, Endpoints đã document, Endpoints chưa rõ.
5. **Smoke Testing**:
   - Hướng dẫn lấy token (client credentials/password).
   - Expected status code/body. URL, Port thực tế.
