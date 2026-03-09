---
name: devops-architect
description: "Automate infrastructure and deployment processes with focus on reliability and observability"
category: architecture
complexity: advanced
---

# /kc:devops-architect - DevOps Infrastructure Design

> **KC Framework Agent**: Launches the devops-architect agent for infrastructure automation.

## Triggers
- Infrastructure automation needs
- CI/CD pipeline design
- Deployment strategy planning
- Observability and monitoring setup

## Usage
```
/kc:devops-architect [infrastructure-needs] [--platform aws|gcp|azure]
```

## What It Does
Uses the Task tool to launch the `devops-architect` agent which:
1. Designs automated infrastructure
2. Plans CI/CD pipelines
3. Ensures reliability and observability
4. Optimizes deployment processes
5. Documents infrastructure decisions

## Example
```
/kc:devops-architect "Kubernetes deployment" --platform gcp
# Designs GKE infrastructure with monitoring and automated deployments
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='devops-architect' for DevOps infrastructure design
```
