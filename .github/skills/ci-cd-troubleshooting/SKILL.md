---
name: ci-cd-troubleshooting
description: Use when investigating, reproducing, or fixing CI/CD pipeline failures, build failures, test failures in CI, deployment failures, environment drift, container build issues, or release automation problems
---

<!-- generated-by: ai-agent-adapter-sync -->


# CI CD Troubleshooting

## Vietnamese User Summary

Skill này điều tra lỗi CI/CD, build, test trên CI, deploy, drift môi trường, container build và release automation.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/03-safety-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Workflow

1. Collect the failing pipeline, job name, command, log excerpt, branch/commit, and environment when available.
2. Retrieve memory for build, deploy, environment, and known CI issues.
3. Inspect CI config, scripts, package manager files, Dockerfiles, environment templates, and direct dependencies.
4. Reproduce the failing command locally when feasible and safe.
5. Compare local and CI differences: OS, runtime version, dependency cache, env vars, services, timezone, filesystem case sensitivity, network access, and secrets availability.
6. Identify the smallest fix or configuration change.
7. Run focused validation commands or document why validation is blocked.
8. Record durable CI/deploy conventions or confirmed root cause when memory is available.
9. Respond to the user in Vietnamese with root cause, changed files, validation, and remaining risks.

## Guardrails

- Do not print or persist CI secrets, tokens, deploy keys, or private registry credentials.
- Do not change production deployment targets without explicit approval.
- Do not disable tests, security scans, or deployment checks to make CI pass.
- Do not rewrite pipeline architecture for a narrow failure unless required.

## Quality Gates

- [ ] Failing command or job was identified.
- [ ] Local versus CI differences were considered.
- [ ] Secrets were not exposed.
- [ ] Fix is minimal and tied to the failure evidence.
- [ ] Validation was run or blocker was recorded.
