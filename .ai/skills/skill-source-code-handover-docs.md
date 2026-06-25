# Legacy Reference: Source Code Handover Documentation

## Reference Status

This file is a legacy reference only. Do not register it as a standalone skill or workflow.

Load this file only when `.ai/skills/source-code-handover/SKILL.md` or a source-code handover workflow needs expanded agent guidance.

## Vietnamese User Summary

File này là reference legacy chi tiết cho skill tạo tài liệu bàn giao source code.

## Purpose

Use this reference only when the main `source-code-handover` skill or workflow needs expanded agent guidance.

## Required Runtime Rules

- Use English for execution instructions and generated operational notes unless the deliverable explicitly requires Vietnamese.
- Use Vietnamese for chat responses to the user.
- Run CodeGraph preflight before source-code review.
- Retrieve memory before module analysis.
- Trust current source code over memory.
- Store only verified durable findings.
- Never store or expose secrets.

## Documentation Standard

Final documentation should be evidence-backed and useful to a new developer.

Include:

- Repository purpose and system overview.
- Technology stack.
- Local setup.
- Entry points and runtime flow.
- Configuration and environment variables without secret values.
- Module map.
- Database documentation when present.
- Auth and permission documentation when present.
- API documentation when present.
- Business flow documentation when present.
- Frontend documentation when present.
- Background jobs, realtime behavior, integrations, logging, and deployment when present.
- Debugging and smoke-test guide.
- Known risks, limitations, and open questions.

## Agent Expansion

Use the dedicated agent specs under `.ai/agents/` for detailed responsibilities:

- Agent 1: Source and local setup.
- Agent 2: Database and auth.
- Agent 3: API and Postman.
- Agent 4: Business and frontend.
- Agent 5: Operations.
- Agent 6: Source/symbol claim verifier.
- Agent 7: Cross-layer flow and conflict verifier.
- Agent 8: Safety, build/test, runtime, and ops evidence verifier.
- Agent 9: Vietnamese final documentation writer.
- Agent 10: Independent publish validator.

## Evidence Rules

- Cite file paths for important claims.
- Cite commands and outputs for validation.
- Mark inferred behavior as inference.
- Do not invent missing features.
- Record unknowns as open questions.

## Output Rules

- Keep draft findings in assigned output paths.
- Keep final documentation in workflow-approved docs paths.
- Keep runtime state under `.ai/runs/` when possible.
- Do not overwrite unrelated user files.

## Readiness

- `Ready`: complete, evidence-backed, reviewed, and validated.
- `Partial`: useful but incomplete or limited by tooling/evidence.
- `Blocked`: cannot continue without user input or required external capability.
