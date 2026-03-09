---
name: chatgpt-proxy
description: "Leverage ChatGPT capabilities for tasks that benefit from OpenAI's models"
category: ai-tools
complexity: standard
---

# /kc:chatgpt-proxy - ChatGPT Access

> **KC Framework Agent**: Launches the chatgpt-proxy agent for ChatGPT-specific capabilities.

## Triggers
- ChatGPT-specific model requests
- GPT-4 reasoning capabilities needed
- Comparison with Claude's approach
- Creative writing or technical explanations

## Usage
```
/kc:chatgpt-proxy [prompt] [--model gpt-4|gpt-3.5] [--temperature N]
```

## What It Does
Uses the Task tool to launch the `chatgpt-proxy` agent which:
1. Routes prompts to ChatGPT models
2. Supports GPT-4 and GPT-3.5-turbo
3. Provides ChatGPT-specific perspectives
4. Returns results for comparison or integration

## Example
```
/kc:chatgpt-proxy "Explain quantum entanglement" --model gpt-4
# Uses GPT-4 for detailed physics explanation
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='chatgpt-proxy' to access ChatGPT models
```
