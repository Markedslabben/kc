---
name: quality-engineer
description: "Ensure software quality through comprehensive testing strategies and systematic edge case detection"
category: quality
complexity: standard
---

# /kc:quality-engineer - Quality Assurance

> **KC Framework Agent**: Launches the quality-engineer agent for comprehensive quality assurance.

## Triggers
- Testing strategy development
- Quality gate implementation
- Edge case identification
- Test coverage improvement

## Usage
```
/kc:quality-engineer [scope] [--focus unit|integration|e2e|all]
```

## What It Does
Uses the Task tool to launch the `quality-engineer` agent which:
1. Develops comprehensive testing strategies
2. Identifies edge cases and boundary conditions
3. Ensures quality gates and standards
4. Improves test coverage systematically
5. Provides quality metrics and reports

## Example
```
/kc:quality-engineer "payment module" --focus integration
# Creates integration test suite for payment processing
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='quality-engineer' for quality assurance
```
