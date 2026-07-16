# Strict Parity Rules

These rules MUST be enforced across all phases of the migration:

1. **Exact Casing & Formatting:** If the legacy response uses `PascalCase` or starts with a capital letter, the .NET 8 API MUST return the exact same casing. No exceptions.
2. **Zero Architecture Modernization:** Do not add CQRS, MediatR, or new patterns unless they existed in the legacy codebase.
3. **Bug Preservation:** Legacy bugs, performance smells, or "bad practices" found in the logic MUST be preserved to maintain 1:1 parity. Log them in the deferred issues report, do not fix them.
4. **Data Integrity:** Any mock data captured during Phase 1 must be reproducible via the tests in Phase 3.
