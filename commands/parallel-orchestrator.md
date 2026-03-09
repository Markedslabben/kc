---
name: parallel-orchestrator
description: "Orchestrate parallel Claude Code sessions using git worktrees with overhead-optimized task splitting"
category: orchestration
complexity: advanced
---

# /kc:parallel-orchestrator - Parallel Task Orchestration

> **KC Framework Agent**: Launches the parallel-orchestrator agent for overhead-aware parallel execution.

## Triggers
- Large tasks spanning >3 files or >2 directories
- Complex multi-phase implementations
- Tasks with independent parallelizable subtasks
- Performance-critical execution needs

## Usage
```
/kc:parallel-orchestrator [task-description] [--concurrency N] [--mode analyze|execute]
```

## What It Does
Uses the Task tool to launch the `parallel-orchestrator` agent which:
1. Analyzes task overhead and parallelization potential
2. Creates isolated git worktrees for parallel execution
3. Splits tasks optimally considering overhead costs
4. Executes subtasks in parallel Claude sessions
5. Merges results and reports completion

## Example
```
/kc:parallel-orchestrator "Refactor authentication system" --concurrency 3
# Creates 3 worktrees, splits auth refactor into parallel subtasks
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='parallel-orchestrator' to orchestrate parallel execution
```
