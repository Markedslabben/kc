---
name: ai-proxy
description: "Leverage multiple AI models (ChatGPT, DeepSeek, Claude variants) for tasks with flexible model selection"
category: ai-tools
complexity: standard
---

# /kc:ai-proxy - Multi-Model AI Access

> **KC Framework Agent**: Launches the ai-proxy agent for accessing multiple AI models.

## Triggers
- Need to compare AI model outputs
- Leverage specific model capabilities (DeepSeek for coding, GPT-4 for reasoning)
- Control model parameters (temperature, max_tokens)
- Access models beyond Claude

## Usage
```
/kc:ai-proxy [prompt] [--model chatgpt|deepseek|claude] [--temperature N]
```

## What It Does
Uses the Task tool to launch the `ai-proxy` agent which:
1. Routes prompts to specified AI models
2. Supports parameter control (temperature, tokens, top_p)
3. Enables comparative analysis across models
4. Returns results for integration

## Example
```
/kc:ai-proxy "Optimize this algorithm" --model deepseek --temperature 0.3
# Uses DeepSeek with low temperature for deterministic coding
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='ai-proxy' to access multiple AI models
```
