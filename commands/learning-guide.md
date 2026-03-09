---
name: learning-guide
description: "Teach programming concepts and explain code with focus on understanding through progressive learning"
category: education
complexity: standard
---

# /kc:learning-guide - Programming Education

> **KC Framework Agent**: Launches the learning-guide agent for programming education and code explanation.

## Triggers
- Programming concept teaching needs
- Code explanation requests
- Progressive learning approach
- Educational explanations

## Usage
```
/kc:learning-guide [topic] [--level beginner|intermediate|advanced]
```

## What It Does
Uses the Task tool to launch the `learning-guide` agent which:
1. Teaches programming concepts clearly
2. Explains code with educational focus
3. Uses progressive learning approaches
4. Provides practical examples
5. Adapts to learner's level

## Example
```
/kc:learning-guide "async/await in Python" --level intermediate
# Explains async programming with progressive examples
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='learning-guide' for programming education
```
