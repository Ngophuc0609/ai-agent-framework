# Sub-skill: 01 Baseline Capture

## Purpose
Perform Static and Dynamic analysis to capture 100% of the legacy behavior.

## Static Analysis
1. Read the legacy code (Controllers, Services, Background Jobs, Realtime/SignalR).
2. Generate **Sequence Diagrams** using Mermaid syntax to map the exact data flow.
3. Document the business logic rules clearly.

## Dynamic Capture (Co-pilot Mode)
1. Ask the human developer to start the legacy application locally.
2. Ask for the localhost port.
3. Use `curl` or terminal commands to hit the local endpoints using mock data.
4. Capture the exact Request and Response payloads down to the exact casing (e.g., camelCase vs PascalCase).

## Output
Fill out `templates/endpoint-contract.template.md` containing the static logic, sequence diagrams, and dynamic I/O captures. Show it to the user for approval.
