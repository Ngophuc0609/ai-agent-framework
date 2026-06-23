---
name: skill-detector
description: Use when determining which registered skill or workflow should handle a user request
---

<!-- generated-by: ai-agent-adapter-sync -->


# Skill Detector

## Vietnamese User Summary

Skill này dùng để nhận diện yêu cầu của bạn nên chạy skill/workflow nào.

## Instructions

1. Read `.ai/registry/triggers.yml`.
2. Match exact trigger phrases first.
3. Match semantic intent second.
4. If multiple workflows match, choose the most specific workflow.
5. If ambiguity remains, ask one concise clarification question in Vietnamese.
6. Load the selected skill before taking action.
