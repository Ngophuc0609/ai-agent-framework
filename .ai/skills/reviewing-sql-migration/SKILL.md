---
name: reviewing-sql-migration
description: Use when reviewing database migrations, schema changes, data migrations, rollback plans, indexes, constraints, or compatibility risks
---

# Reviewing SQL Migration

## Vietnamese User Summary

Skill này review migration/schema change trước khi chạy hoặc merge.

## Workflow

1. Read migration and related model/entity changes.
2. Check backward compatibility.
3. Check indexes, constraints, defaults, nullability, and data volume risks.
4. Check rollback strategy.
5. Check tests and SQL verification queries.
6. Record risks and `Need verify` items.
