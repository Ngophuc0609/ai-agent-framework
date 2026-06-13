---
name: database-query-analysis
description: Use when analyzing database query behavior, slow queries, N+1 patterns, indexes, transaction boundaries, locking, pagination, ORM queries, repository methods, or runtime database performance risks
---

# Database Query Analysis

## Vietnamese User Summary

Skill này phân tích query database, query chậm, N+1, index, transaction, locking, pagination, ORM/repository và rủi ro performance runtime.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Workflow

1. Define the target query, endpoint, repository method, job, report, or performance symptom.
2. Retrieve database-related memory and docs such as `docs/DATABASE_SUMMARY.md` when present.
3. Run CodeGraph preflight.
4. Trace call sites, ORM/query builder usage, filters, joins, pagination, ordering, transaction boundaries, and write paths.
5. Check indexes, constraints, nullability, expected cardinality, N+1 behavior, lock duration, and batch size.
6. Use tests, seed data, SQL explain output, logs, or query traces when available; mark missing runtime evidence as `Need verify`.
7. Recommend scoped fixes such as eager loading, index changes, pagination, batching, query shape changes, or transaction narrowing.
8. Route schema changes to `reviewing-sql-migration` before merge or execution.
9. Respond to the user in Vietnamese.

## Guardrails

- Do not run destructive SQL.
- Do not assume production data volume without evidence.
- Do not recommend indexes without identifying read/write tradeoffs and migration risk.
- Do not mix large refactors into query fixes unless required.

## Quality Gates

- [ ] Query path and call sites were identified.
- [ ] Index, N+1, pagination, transaction, and locking risks were considered.
- [ ] Runtime evidence is cited or marked `Need verify`.
- [ ] Schema changes are routed through migration review.
- [ ] Recommendations are scoped and testable.
