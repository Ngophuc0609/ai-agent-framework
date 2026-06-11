# 04 One-Command Trigger Rules

## Vietnamese User Summary

Rule này cho phép người dùng dùng một câu ngắn như `tạo tài liệu` hoặc `tạo api mới` để kích hoạt workflow đúng.

## Trigger Flow

When the user gives a short command:

1. Read `.ai/registry/triggers.yml`.
2. Match both English and Vietnamese trigger aliases.
3. Resolve to one workflow or one skill-only task.
4. Load the matching skill and workflow when a workflow exists.
5. Apply required global rules.

## Ambiguous Trigger

If multiple workflows or skills match:

1. Prefer the most specific trigger.
2. Prefer exact phrase matches over broad semantic matches.
3. If still ambiguous, ask one concise clarification question in Vietnamese.

## No Match

If no workflow matches:

1. Do not invent a workflow.
2. Explain in Vietnamese that no matching workflow exists.
3. Offer the closest existing workflow only when the match is safe.

## Execution Language

- Internal execution instructions remain English.
- Chat responses to the user remain Vietnamese.
