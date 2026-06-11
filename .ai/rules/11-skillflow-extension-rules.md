# 11 Skillflow Extension Rules

## Vietnamese User Summary

Rule này chuẩn hóa cách thêm skillflow mới để không ảnh hưởng skill, agent hoặc workflow hiện có.

## Naming

- Use a unique kebab-case `skillflow_id`, such as `source-code-handover`, `security-review`, or `test-generation`.
- Avoid generic names such as `docs`, `agent`, or `workflow`.
- Place the workflow at `.ai/workflows/<skillflow_id>.md`.
- Place dedicated agents under `.ai/agents/<skillflow_id>/` when needed.

## Registry

Every new skillflow must be registered in:

- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`

Do not add a trigger only inside a standalone rule file.

## Output Namespace

New skillflows must not write into another skillflow's output or handoff paths.

Preferred runtime namespace:

```text
.ai/runs/<skillflow_id>/<run_id>/
```

If a workflow writes user-facing output to `docs/` or another public path, it must explicitly list allowed write paths.

## Required Files

A minimal skillflow needs:

- A Superpowers-style `SKILL.md`.
- A workflow file.
- Registry entries.
- Trigger aliases.
- Allowed write paths.
- Quality gates.
- Fallback behavior.

## Superpowers Style

- Do not create a separate `superpower` capability concept.
- Treat Superpowers as a methodology: check available skills, read the selected skill, then follow it.
- A skill may declare `REQUIRED BACKGROUND` or `REQUIRED SKILL`.
- Keep `SKILL.md` concise. Move long details to directly referenced files.
- Frontmatter must contain only `name` and `description`.
- The `description` must start with `Use when...`.

## Isolation

When adding a skillflow:

- Do not modify unrelated agent specs.
- Do not change legacy output paths without a migration.
- Do not delete existing handoff or runtime state unless requested.
- Add shared rules only when they are backward-compatible.

## Required Policies

Source-reading skillflows must follow:

- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Readiness Checklist

- [ ] Skill, workflow, and trigger are registered.
- [ ] Trigger does not conflict with existing workflows.
- [ ] Output namespace is isolated.
- [ ] Skill description starts with `Use when...`.
- [ ] Memory Policy is included when project knowledge is used.
- [ ] Efficiency and Cost Policy is included.
- [ ] Allowed write paths are listed.
- [ ] Quality gates are defined.
- [ ] Fallback behavior is defined.
- [ ] Adapter notes exist when tool behavior differs.
