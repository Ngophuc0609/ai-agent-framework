# 10 CodeGraph-First Rules

## Summary

This rule requires checking and using CodeGraph before source-code review. If CodeGraph is unavailable and cannot be initialized, the agent must ask before using a weaker fallback.

## Requirement

For any task that scans, documents, debugs, refactors, or changes source code, run CodeGraph preflight before broad source-code review.

## Preflight

1. Check whether CodeGraph tooling is available in the current agent environment.
2. Check whether the project has an initialized CodeGraph index.
3. If the index is missing, initialize it using the available CodeGraph setup command.
4. If initialization succeeds, use CodeGraph exploration/search before raw file search for architecture and symbol-level understanding.
5. If CodeGraph is unavailable or initialization fails, stop and ask the user whether to continue without CodeGraph or use another tool.

## Approved Fallback Behavior

Only use `rg`, language server search, IDE search, or manual file reads as a replacement after:

- CodeGraph was attempted, and
- The limitation was recorded, and
- The user approved continuing without CodeGraph when correctness may be affected.

## Documentation Integrity

When CodeGraph is unavailable:

- Mark the output as having reduced confidence.
- Cite the fallback tools used.
- Avoid broad architecture claims unless independently verified from source.

## Do Not

- Do not pretend CodeGraph was used when it was not.
- Do not fabricate symbol relationships.
- Do not skip CodeGraph because `rg` is faster.
- Do not continue silently after automatic CodeGraph setup fails.
