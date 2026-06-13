---
name: analyzing-background-jobs
description: Use when analyzing or documenting existing background jobs, schedulers, queues, workers, recurring tasks, or async processing flows; route new jobs or production behavior changes through developing-backend-feature-tdd
---

# Analyzing Background Jobs

## Vietnamese User Summary

Skill này phân tích hoặc tài liệu hóa job nền, scheduler, queue, worker hoặc async flow đã tồn tại. Nếu tạo job mới hoặc đổi behavior production, agent phải chuyển sang `developing-backend-feature-tdd`.

## Workflow

1. Search memory and `docs/JOBS_SUMMARY.md`.
2. Run CodeGraph preflight.
3. Identify trigger, schedule, queue/topic, handler, retries, idempotency, locking, and failure behavior.
4. For new jobs or production behavior changes, route through `developing-backend-feature-tdd` first.
5. Add tests or executable verification for job behavior when possible.
6. Update job docs and memory with confirmed behavior.
