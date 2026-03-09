---
name: root-cause-analyst
description: "Systematically investigate complex problems to identify underlying causes through evidence-based analysis"
category: analysis
complexity: advanced
---

# /kc:root-cause-analyst - Root Cause Analysis

> **KC Framework Agent**: Launches the root-cause-analyst agent for systematic problem investigation.

## Triggers
- Complex problem investigation
- Recurring issues needing deep analysis
- Evidence-based troubleshooting
- Hypothesis testing for problems

## Usage
```
/kc:root-cause-analyst [problem-description] [--method 5-whys|fishbone|fault-tree]
```

## What It Does
Uses the Task tool to launch the `root-cause-analyst` agent which:
1. Systematically investigates problems
2. Identifies underlying root causes
3. Uses evidence-based analysis methods
4. Tests hypotheses methodically
5. Provides actionable recommendations

## Example
```
/kc:root-cause-analyst "System crashes intermittently" --method 5-whys
# Uses 5 Whys methodology to find root cause
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='root-cause-analyst' for root cause analysis
```
