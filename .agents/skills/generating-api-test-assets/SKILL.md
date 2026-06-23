---
name: generating-api-test-assets
description: Use when creating curl examples, Postman requests, API regression checks, SQL verification queries, or OpenAPI notes for a scoped API behavior
---

<!-- generated-by: ai-agent-adapter-sync -->


# Generating API Test Assets

## Vietnamese User Summary

Skill này tạo curl/Postman/SQL verify để kiểm thử API.

## Workflow

1. Read the API contract and auth requirements.
2. Generate curl or Postman examples using placeholders for secrets.
3. Add SQL verification queries when database side effects exist.
4. Add OpenAPI/Swagger notes only when the project maintains them.
5. Mark any environment-specific value as `Need verify`.

## Safety

- Never include real tokens, passwords, API keys, or connection strings.
- Use placeholders such as `<ACCESS_TOKEN>` and `<BASE_URL>`.
