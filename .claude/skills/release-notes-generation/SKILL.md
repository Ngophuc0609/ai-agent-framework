---
name: release-notes-generation
description: Use when generating release notes, changelogs, upgrade notes, user-visible change summaries, breaking change notes, migration notes, or deployment summaries from git diff, commits, pull requests, issues, tests, or verification evidence
---

<!-- generated-by: ai-agent-adapter-sync -->


# Release Notes Generation

## Vietnamese User Summary

Skill này tạo release notes/changelog/upgrade notes từ diff, commit, PR, issue, test và bằng chứng verify.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`

## Workflow

1. Identify release scope: current diff, commit range, branch, PR list, issue list, or manual summary.
2. Read git diff/log or provided artifacts first.
3. Group changes by user-visible behavior, API changes, database changes, operations changes, docs, tests, and internal refactors.
4. Highlight breaking changes, migration steps, feature flags, config/env changes, rollback notes, and known risks.
5. Mention validation evidence such as tests, smoke checks, curl/Postman checks, or skipped validation with reason.
6. Produce concise release notes in the requested language; default to Vietnamese for chat output.
7. Do not include raw internal noise unless useful for deployment or support.

## Guardrails

- Do not claim tests passed unless evidence exists.
- Do not expose secrets, private issue details, or sensitive customer data.
- Do not overstate internal refactors as user-facing features.
- Mark uncertain impact as `Need verify`.

## Quality Gates

- [ ] Source scope is explicit.
- [ ] User-visible changes are separated from internal changes.
- [ ] Breaking changes and migration notes are called out.
- [ ] Validation evidence is included or missing validation is noted.
- [ ] Output is concise and release-ready.
