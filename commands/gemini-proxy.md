---
name: gemini-proxy
description: "Leverage Google Gemini capabilities for multimodal tasks and Google's knowledge integration"
category: ai-tools
complexity: standard
---

# /kc:gemini-proxy - Google Gemini Access

> **KC Framework Agent**: Launches the gemini-proxy agent for Gemini-specific capabilities.

## Triggers
- Gemini-specific model requests
- Multimodal analysis needs
- Google knowledge integration
- Scientific reasoning tasks

## Usage
```
/kc:gemini-proxy [prompt] [--model gemini-pro|gemini-ultra]
```

## What It Does
Uses the Task tool to launch the `gemini-proxy` agent which:
1. Routes prompts to Google Gemini models
2. Supports multimodal capabilities
3. Leverages Google's knowledge integration
4. Returns results for comparison or integration

## Example
```
/kc:gemini-proxy "Analyze scientific papers on AI" --model gemini-pro
# Uses Gemini for research analysis
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='gemini-proxy' to access Google Gemini models
```
