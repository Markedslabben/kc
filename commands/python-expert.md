---
name: python-expert
description: "Deliver production-ready, secure, high-performance Python code following SOLID principles and modern best practices"
category: development
complexity: standard
---

# /kc:python-expert - Production Python Development

> **KC Framework Agent**: Launches the python-expert agent for professional-grade Python development.

## Triggers
- Python code implementation needs
- Production-ready Python development
- SOLID principles and best practices
- Secure, high-performance Python code

## Usage
```
/kc:python-expert [task-description] [--focus performance|security|testing]
```

## What It Does
Uses the Task tool to launch the `python-expert` agent which:
1. Implements Python code following SOLID principles
2. Applies modern best practices and type hints
3. Ensures security and performance optimization
4. Includes comprehensive error handling
5. Provides production-ready, tested code

## Example
```
/kc:python-expert "Create data processing pipeline" --focus performance
# Generates optimized Python code with proper architecture
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='python-expert' to implement production-ready Python code
```
