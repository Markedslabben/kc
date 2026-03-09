---
name: task-velocity-estimator
description: "Track task completion times and provide data-driven time estimates for comprehensive tasks"
category: productivity
complexity: standard
---

# /kc:task-velocity-estimator - Task Time Estimation

> **KC Framework Agent**: Launches the task-velocity-estimator agent for data-driven task estimation.

## Triggers
- Task time estimation needs
- Historical velocity tracking
- Data-driven time predictions
- Task complexity analysis

## Usage
```
/kc:task-velocity-estimator [task-description] [--track] [--estimate]
```

## What It Does
Uses the Task tool to launch the `task-velocity-estimator` agent which:
1. Tracks task completion times
2. Builds historical velocity data
3. Provides data-driven time estimates
4. Analyzes task complexity
5. Improves estimation accuracy over time

## Example
```
/kc:task-velocity-estimator "Implement user dashboard" --estimate
# Provides time estimate based on historical velocity data
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='task-velocity-estimator' for task estimation
```
