---
name: frontend-architect
description: "Create accessible, performant user interfaces with focus on user experience and modern frameworks"
category: architecture
complexity: advanced
---

# /kc:frontend-architect - Frontend System Design

> **KC Framework Agent**: Launches the frontend-architect agent for frontend architecture design.

## Triggers
- Frontend system design needs
- UI/UX architecture planning
- Component architecture design
- Frontend framework decisions

## Usage
```
/kc:frontend-architect [app-description] [--framework react|vue|svelte]
```

## What It Does
Uses the Task tool to launch the `frontend-architect` agent which:
1. Designs accessible, performant UI architectures
2. Plans component hierarchies and state management
3. Ensures modern framework best practices
4. Optimizes for user experience
5. Documents frontend design decisions

## Example
```
/kc:frontend-architect "Dashboard application" --framework react
# Designs React component architecture with state management
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='frontend-architect' for frontend system design
```
