---
name: backend-architect
description: "Design reliable backend systems with focus on data integrity, security, and fault tolerance"
category: architecture
complexity: advanced
---

# /kc:backend-architect - Backend System Design

> **KC Framework Agent**: Launches the backend-architect agent for backend architecture design.

## Triggers
- Backend system design needs
- API architecture planning
- Database schema design
- Backend infrastructure decisions

## Usage
```
/kc:backend-architect [system-description] [--pattern microservices|monolith|serverless]
```

## What It Does
Uses the Task tool to launch the `backend-architect` agent which:
1. Designs backend architectures with data integrity
2. Plans API structures and patterns
3. Ensures security and fault tolerance
4. Optimizes database schemas
5. Documents backend design decisions

## Example
```
/kc:backend-architect "Payment processing system" --pattern microservices
# Designs secure, fault-tolerant payment backend
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='backend-architect' for backend system design
```
