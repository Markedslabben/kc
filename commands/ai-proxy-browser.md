---
name: ai-proxy-browser
description: "Leverage AI models through web interfaces using Chrome DevTools browser automation"
category: ai-tools
complexity: advanced
---

# /kc:ai-proxy-browser - Browser-Based AI Access

> **KC Framework Agent**: Launches the ai-proxy-browser agent for web-based AI model access.

## Triggers
- Web subscription access (no API keys)
- Browser-based AI model interaction
- Complex web UI automation for AI tools
- Testing AI web interfaces

## Usage
```
/kc:ai-proxy-browser [prompt] [--service chatgpt-web|deepseek-web]
```

## What It Does
Uses the Task tool to launch the `ai-proxy-browser` agent which:
1. Automates browser interaction with AI web interfaces
2. Accesses AI models via web subscriptions
3. Uses Chrome DevTools MCP for automation
4. Returns results from web-based AI services

## Example
```
/kc:ai-proxy-browser "Generate code" --service deepseek-web
# Uses browser automation to access DeepSeek web interface
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='ai-proxy-browser' for browser-based AI access
```
