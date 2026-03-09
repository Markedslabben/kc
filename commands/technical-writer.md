---
name: technical-writer
description: "Create clear, comprehensive technical documentation tailored to specific audiences with focus on usability"
category: documentation
complexity: standard
---

# /kc:technical-writer - Technical Documentation

> **KC Framework Agent**: Launches the technical-writer agent for professional documentation creation.

## Triggers
- Documentation creation needs
- API documentation requirements
- User guide development
- Technical specification writing

## Usage
```
/kc:technical-writer [topic] [--audience developer|user|admin] [--format markdown|html]
```

## What It Does
Uses the Task tool to launch the `technical-writer` agent which:
1. Creates clear, comprehensive documentation
2. Tailors content to specific audiences
3. Ensures usability and accessibility
4. Structures information logically
5. Includes examples and best practices

## Example
```
/kc:technical-writer "API authentication" --audience developer --format markdown
# Creates developer-focused API auth documentation
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='technical-writer' for documentation creation
```
