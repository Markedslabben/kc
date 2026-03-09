---
name: system-architect
description: "Design scalable system architecture with focus on maintainability and long-term technical decisions"
category: architecture
complexity: advanced
---

# /kc:system-architect - System Architecture Design

> **KC Framework Agent**: Launches the system-architect agent for comprehensive system design.

## Triggers
- System architecture design needs
- Scalability planning
- Long-term technical decision-making
- Infrastructure architecture

## Usage
```
/kc:system-architect [project-description] [--scale small|medium|large|enterprise]
```

## What It Does
Uses the Task tool to launch the `system-architect` agent which:
1. Analyzes requirements and constraints
2. Designs scalable, maintainable architectures
3. Makes informed technology stack decisions
4. Plans for long-term evolution and growth
5. Documents architectural decisions (ADRs)

## Example
```
/kc:system-architect "E-commerce platform" --scale enterprise
# Designs microservices architecture with proper boundaries
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='system-architect' to design scalable system architecture
```
