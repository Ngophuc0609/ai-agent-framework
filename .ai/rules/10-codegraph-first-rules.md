# 10 CodeGraph Risk-Based Rules

## Summary

This rule scales CodeGraph usage to task risk. Graph evidence is mandatory only when the selected workflow or breadth of analysis requires it.

## Requirement Matrix

- Required first attempt: architecture analysis, source handover, cross-module flows, broad refactors, dependency tracing, and workflows that explicitly require graph evidence.
- Preferred but non-blocking: localized bug fixes, targeted endpoint analysis, single-module edits, focused test changes, and diff reviews.
- Not required: documentation formatting, registry-only edits, generated-file checks, or tasks that do not inspect source relationships.

## Preflight

1. Check whether CodeGraph is available and indexed for the current project.
2. When graph evidence is required and the index is missing, initialize it only when the setup is local and does not install packages or require unapproved network access.
3. Use CodeGraph before raw search for architecture and symbol-relationship claims.
4. If CodeGraph is unavailable, follow the fallback policy below.

## Fallback Policy

For preferred/non-blocking tasks, continue with `rg`, language-server or IDE references, tests, git diff, and narrow source slices. Record the limitation, fallback, and confidence/readiness impact.

For required graph tasks, block only when the selected workflow explicitly requires graph evidence or the requested claim cannot be supported reliably with available source evidence. Otherwise continue with reduced confidence/readiness and state the limitation.

## Documentation Integrity

- Cite the fallback tools and physical source slices used.
- Avoid broad architecture or dependency-completeness claims from text search alone.
- Never pretend CodeGraph was used when it was unavailable.
- Never install CodeGraph or another package without runtime-appropriate approval.
