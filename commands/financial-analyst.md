---
name: financial-analyst
description: "Expert financial analysis and business intelligence for spreadsheet analysis, modeling, budgeting, and forecasting"
category: analysis
complexity: advanced
---

# /kc:financial-analyst - Financial Analysis

> **KC Framework Agent**: Launches the financial-analyst agent for comprehensive financial analysis.

## Triggers
- Financial data analysis needs
- Budget planning and forecasting
- Investment evaluation
- Business intelligence reporting

## Usage
```
/kc:financial-analyst [analysis-type] [--focus budget|forecast|investment|scenario]
```

## What It Does
Uses the Task tool to launch the `financial-analyst` agent which:
1. Analyzes financial data and spreadsheets
2. Creates financial models and forecasts
3. Evaluates investment opportunities
4. Provides data-driven business recommendations
5. Generates financial reports and insights

## Example
```
/kc:financial-analyst "Q1 budget review" --focus budget
# Analyzes Q1 financial data and provides budget insights
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='financial-analyst' for financial analysis
```
