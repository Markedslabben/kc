---
name: socratic-mentor
description: "Educational guide using Socratic method for programming knowledge through strategic questioning"
category: education
complexity: standard
---

# /kc:socratic-mentor - Socratic Learning

> **KC Framework Agent**: Launches the socratic-mentor agent for Socratic method learning.

## Triggers
- Discovery learning needs
- Deep understanding through questioning
- Critical thinking development
- Programming concept exploration

## Usage
```
/kc:socratic-mentor [topic] [--focus concept|problem-solving|debugging]
```

## What It Does
Uses the Task tool to launch the `socratic-mentor` agent which:
1. Uses Socratic questioning method
2. Guides discovery through strategic questions
3. Develops critical thinking skills
4. Encourages deep understanding
5. Helps learners discover solutions

## Example
```
/kc:socratic-mentor "Why is my code slow?" --focus debugging
# Guides learner to discover performance issues through questioning
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='socratic-mentor' for Socratic learning
```
