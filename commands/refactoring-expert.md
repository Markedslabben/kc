---
name: refactoring-expert
description: "Improve code quality and reduce technical debt through systematic refactoring and clean code principles"
category: development
complexity: standard
---

# /kc:refactoring-expert - Code Refactoring

> **KC Framework Agent**: Launches the refactoring-expert agent for systematic code improvement.

## Triggers
- Code quality improvement needs
- Technical debt reduction
- Refactoring legacy code
- Clean code principles application

## Usage
```
/kc:refactoring-expert [scope] [--pattern extract-method|simplify|reduce-complexity]
```

## What It Does
Uses the Task tool to launch the `refactoring-expert` agent which:
1. Identifies code smells and technical debt
2. Applies systematic refactoring patterns
3. Improves code maintainability
4. Ensures clean code principles
5. Maintains functionality while improving structure

## Example
```
/kc:refactoring-expert "auth module" --pattern simplify
# Refactors authentication code for better readability
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='refactoring-expert' for code refactoring
```
