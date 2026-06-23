# Agent 2: Database And Auth

## Vietnamese User Summary

Agent này đi sâu vào Database (Topology, Schema, Data Dictionary, Migration) và Security (OIDC, Tokens, Clients, Roles). Viết hoàn toàn bằng tiếng Việt.

## Allowed Write Paths

- `.ai/runs/source-code-handover/<run_id>/findings/agent-02/findings.md`
- `draft-docs/agent-02-findings.md`

## Required Output Details & Definition of Done

1. **Database Topology & Inventory**:
   - Bảng: `DbContext | Database | Contains Data | Project | Migration assembly`.
   - Liệt kê toàn bộ Entities, DbSets, Fluent API, Migrations, Seed data, Raw SQL/Dapper.
2. **Data Dictionary**:
   - Với mỗi bảng: Tên entity, Tên DB, Mapping config, Mục đích, PK, FK, Index, Soft delete, Sensitive fields (PII, hash).
   - Bảng field: `Field | DB Type | C# Type | Null | Default | PK/FK | Sensitive | Ý nghĩa`.
3. **ERD & Quan hệ dữ liệu**:
   - ERD tổng thể và chi tiết (bằng Mermaid). Chỉ ra Cascade delete, Bridge tables.
4. **Migration & Seed Runbook**:
   - Lệnh cụ thể: Tạo migration, Apply local/prod, Seed dữ liệu (tạo admin đầu tiên), Reset DB, Rollback.
5. **Auth & Security Contracts**:
   - Token Policy: issuer, authority, scopes, signing key source, token lifetime.
   - Client Config: `Client ID | Grant type | Redirect URI | Allowed scopes | PKCE | Secret req | Owner`.
   - Role/Policy Map: `Role | Policy | Endpoints protected | Quyền thực tế`.
   - Account provisioning flow, external providers (Zalo/GitHub) callback & claims mapping.
