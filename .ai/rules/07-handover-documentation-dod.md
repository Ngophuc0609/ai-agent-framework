# Developer Handover Documentation Definition of Done

## Audience

Published handover documentation is for developers who need to understand and work on the current system. It is not an analysis report or an audit trail.

## Published Set

The final and published directories contain exactly documents `01` through `20` defined in `.ai/rules/08-source-code-handover-quality-checklist.md`.

Documents `17` through `20` centralize risks, open questions, evidence mapping, and coverage. Documents `01` through `16` must not repeat those sections.

## Content Standard

- Explain the current system from verified source facts.
- Cover setup, repository map, architecture, important business flows, data stores, auth, APIs, jobs, realtime, integrations, frontend, operations, deployment, and testing when present.
- Show where developers start for common changes.
- Include executable commands with working directory and expected result.
- Use real paths, symbols, routes, configuration keys, schemas, and examples.
- Omit subjects that cannot be verified from topic documents instead of publishing uncertainty commentary.
- Keep Evidence IDs, claim labels, readiness/coverage, risks, limitations, and open questions out of documents `01` through `16`.

## Publish Gate

- Exactly 20 expected files exist.
- Current source commit is recorded in front matter.
- Technical content matches current source and internal evidence.
- Vietnamese prose is clear and developer-oriented.
- Links and commands are valid.
- Secret scan passes.
- Deterministic quality validation and Agent 10 verdict pass.
