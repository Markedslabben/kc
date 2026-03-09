---
name: performance-engineer
description: "Optimize system performance through measurement-driven analysis and bottleneck elimination"
category: performance
complexity: standard
---

# /kc:performance-engineer - Performance Optimization

> **KC Framework Agent**: Launches the performance-engineer agent for performance analysis and optimization.

## Triggers
- Performance bottleneck identification
- System optimization needs
- Slow response time investigation
- Resource usage optimization

## Usage
```
/kc:performance-engineer [scope] [--metric latency|throughput|memory|cpu]
```

## What It Does
Uses the Task tool to launch the `performance-engineer` agent which:
1. Profiles system performance
2. Identifies bottlenecks through measurement
3. Optimizes algorithms and data structures
4. Reduces resource consumption
5. Provides performance improvement recommendations

## Example
```
/kc:performance-engineer "Database queries" --metric latency
# Analyzes query performance, suggests indexes and optimizations
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='performance-engineer' for performance optimization
```
