---
name: security-engineer
description: "Identify security vulnerabilities and ensure compliance with security standards and best practices"
category: security
complexity: standard
---

# /kc:security-engineer - Security Analysis & Hardening

> **KC Framework Agent**: Launches the security-engineer agent for comprehensive security review.

## Triggers
- Security vulnerability assessment needs
- OWASP compliance checking
- Code security review
- Security best practices enforcement

## Usage
```
/kc:security-engineer [scope] [--focus auth|data|api|infrastructure]
```

## What It Does
Uses the Task tool to launch the `security-engineer` agent which:
1. Scans for common vulnerabilities (OWASP Top 10)
2. Reviews authentication and authorization
3. Checks data encryption and protection
4. Validates input sanitization and output encoding
5. Provides security recommendations

## Example
```
/kc:security-engineer "Review API endpoints" --focus api
# Analyzes API security: auth, rate limiting, injection risks
```

## Behind the Scenes
This command executes:
```
Use the Task tool with subagent_type='security-engineer' for security analysis
```
