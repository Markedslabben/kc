---
name: parallel
description: "Parallel orchestrator with overhead-aware task splitting (direct skill)"
category: orchestration
complexity: advanced
---

# /kc:parallel - Parallel Task Orchestration (Direct Skill)

> **KC Framework Direct Skill**: Mode: analyze (default), execute, or dry-run

## Quick Access
This is a direct skill shortcut. For the full KC parallel orchestrator agent, use:
- `/kc:parallel-orchestrator` - Full agent with Task tool integration

## Usage
```
/kc:parallel [mode] [task-description]
```

Modes:
- `analyze` (default) - Analyze task for parallelization potential
- `execute` - Execute parallel orchestration
- `dry-run` - Simulate without execution

## What It Does
Directly activates the parallel orchestration skill which:
1. Analyzes tasks for overhead-optimized parallelization
2. Creates git worktrees for isolated execution
3. Splits tasks considering overhead costs
4. Executes in parallel when beneficial
5. Merges results systematically

## Example
```
/kc:parallel analyze "Refactor authentication system"
# Analyzes refactoring task for parallel execution potential
```

## See Also
- `/kc:parallel-orchestrator` - Full agent version
- `/parallel` - Global parallel skill (same functionality)
