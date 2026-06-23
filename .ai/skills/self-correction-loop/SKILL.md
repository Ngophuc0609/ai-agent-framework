---
name: self-correction-loop
description: Use when you need to review, critique, and correct your own code or a peer's code before finalizing.
---
# Self Correction Loop

## Guidance
1. **Analyze:** Review the target code/document thoroughly. Look for:
   - Security vulnerabilities (e.g., injection risks, leaked secrets).
   - Code smells (e.g., missing error handling, hardcoded values).
   - Requirement mismatches (Did it actually solve the user's prompt?).
2. **Critique:** Output a clear `### Critique` section listing identified issues. If no issues are found, explicitly state "No issues found."
3. **Fix:** Output a `### Fixes` section detailing the changes, and apply them using the appropriate tools.
4. **Loop:** If the fixes introduce new complexity, repeat the cycle (up to 3 times) until the code meets the high-quality standard.
