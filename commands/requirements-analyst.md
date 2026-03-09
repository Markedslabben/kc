---
name: requirements-analyst
description: "Transform ambiguous project ideas into concrete specifications through systematic requirements discovery"
category: development
complexity: standard
---

# /kc:requirements-analyst - Requirements Discovery

> **KC Framework Agent**: Launches the requirements-analyst agent for requirements gathering.

## Triggers
- Vague project ideas needing clarification
- Requirements discovery needs
- Specification documentation
- Ambiguous feature requests

## Usage
```
/kc:requirements-analyst [project-idea] [--format prd|user-stories|specs]
```

## What It Does
Uses the Task tool to launch the `requirements-analyst` agent which:
1. Clarifies ambiguous requirements
2. Asks probing discovery questions
3. Documents specifications systematically
4. Creates structured requirement documents
5. Ensures completeness and clarity

## Example
```
/kc:requirements-analyst "Build e-commerce platform" --format prd
# Generates comprehensive Product Requirements Document
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='requirements-analyst' for requirements discovery
```
