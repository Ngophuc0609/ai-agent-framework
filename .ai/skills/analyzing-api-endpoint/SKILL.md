---
name: analyzing-api-endpoint
description: Use when analyzing, documenting, tracing, or explaining an existing API endpoint; do not use for creating new endpoints or new API features
---

# Analyzing API Endpoint

## Vietnamese User Summary

Skill này chỉ dùng để phân tích endpoint đã tồn tại. Nếu tạo endpoint mới thì phải chuyển sang `developing-backend-feature-tdd`.

## Routing Guard

If the user asks to create a new endpoint or new API feature, stop and route to `developing-backend-feature-tdd`.

## Workflow

1. Search memory and project docs.
2. Run CodeGraph preflight.
3. Locate the existing route/controller/handler.
4. Trace request model, validation, service, repository, auth, and response mapping.
5. Check tests and API documentation when present.
6. Summarize behavior, risks, and open questions.

## Cost Optimization Checklist

- [ ] Memory was searched before scanning code.
- [ ] `docs/PROJECT_CONTEXT.md` was read when present.
- [ ] Only directly relevant endpoint files were read.
- [ ] Findings were summarized for reuse.
- [ ] Secrets, logs, and large raw code were not stored in memory.
