---
name: analyzing-background-jobs
description: Use when analyzing, creating, changing, or documenting background jobs, schedulers, queues, workers, recurring tasks, or async processing flows
---

# Analyzing Background Jobs

## Vietnamese User Summary

Skill này phân tích job nền, scheduler, queue, worker hoặc async flow.

## Workflow

1. Search memory and `docs/JOBS_SUMMARY.md`.
2. Run CodeGraph preflight.
3. Identify trigger, schedule, queue/topic, handler, retries, idempotency, locking, and failure behavior.
4. For new jobs, route through `developing-backend-feature-tdd` first.
5. Add tests or executable verification for job behavior when possible.
6. Update job docs and memory with confirmed behavior.
