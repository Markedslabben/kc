---
name: analyze-prompt
description: "Analyze user prompts and recommend optimal agents, tools, and improvements based on Anthropic best practices"
category: analysis
complexity: standard
---

# /kc:analyze-prompt - Prompt Optimization

> **KC Framework Agent**: Launches the analyze-prompt agent for prompt analysis and optimization.

## Triggers
- Vague or unclear prompts
- Prompt optimization requests
- Best practices application
- Tool/agent selection guidance

## Usage
```
/kc:analyze-prompt [prompt-text] [--suggest-improvements]
```

## What It Does
Uses the Task tool to launch the `analyze-prompt` agent which:
1. Analyzes prompt quality and clarity
2. Recommends optimal agents and tools
3. Suggests improvements based on Anthropic best practices
4. Provides optimized prompt alternatives
5. Identifies missing context or requirements

## Example
```
/kc:analyze-prompt "Make the code better" --suggest-improvements
# Analyzes vague prompt, suggests specific improvements
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='analyze-prompt' for prompt optimization
```
