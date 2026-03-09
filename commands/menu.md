---
name: menu
description: "Klaus Claude (KC) Framework - Main Menu"
category: meta
complexity: simple
---

# /kc:menu - Klaus Claude Framework

**Klaus Claude Framework** - Personal agent collection with 26 specialized agents and overhead-optimized parallel execution.

## 🚀 Quick Access Commands

### Direct Skills
- `/kc:parallel` - Parallel orchestrator with overhead-aware task splitting
- `/kc:md2docx` - Convert markdown to professional Word documents

### Architecture (4 agents)
- `/kc:system-architect` - Design scalable system architecture
- `/kc:backend-architect` - Backend systems with data integrity and security
- `/kc:frontend-architect` - Accessible, performant user interfaces
- `/kc:devops-architect` - Infrastructure automation and deployment

### Development (3 agents)
- `/kc:python-expert` - Production-ready Python with SOLID principles
- `/kc:refactoring-expert` - Code quality and technical debt reduction
- `/kc:requirements-analyst` - Transform ideas into specifications

### Quality & Security (3 agents)
- `/kc:quality-engineer` - Comprehensive testing strategies
- `/kc:security-engineer` - Security vulnerabilities and compliance
- `/kc:performance-engineer` - Performance optimization and bottlenecks

### AI Model Proxies (4 agents)
- `/kc:ai-proxy` - Multi-model access (ChatGPT, DeepSeek, Claude)
- `/kc:ai-proxy-browser` - Browser-based AI model access
- `/kc:chatgpt-proxy` - ChatGPT-specific capabilities
- `/kc:gemini-proxy` - Google Gemini multimodal access

### Analysis & Documentation (4 agents)
- `/kc:analyze-prompt` - Prompt optimization and tool selection
- `/kc:root-cause-analyst` - Systematic problem investigation
- `/kc:technical-writer` - Professional technical documentation
- `/kc:financial-analyst` - Financial analysis and business intelligence

### Testing & Debugging (1 agent - CONSOLIDATED)
- `/kc:parallel-debugger` - Complete debugging pipeline (Bug → Verified Fix)
  - **Modes**: `--test-only`, `--analyze`, `--full` (default)
  - **Built-in**: Parallel hypothesis testing engine
  - **Replaces**: ~~parallel-test~~, ~~parallel-tester~~ (deprecated)

### Learning (2 agents)
- `/kc:learning-guide` - Programming education and code explanation
- `/kc:socratic-mentor` - Socratic method learning through questioning

### Productivity (1 agent)
- `/kc:task-velocity-estimator` - Data-driven task time estimation

## Using KC Agents

**Direct Skills**: Type `/kc:parallel` or `/kc:md2docx` directly

**Agents**: Commands automatically launch agents via Task tool

**Example**:
```
/kc:python-expert "Create data processing pipeline" --focus performance
# Launches python-expert agent for production-ready Python code
```

## Integration with SC Framework

KC Framework works alongside SuperClaude (SC) Framework:
- **KC**: Personal agents and specialized tools
- **SC**: Workflow orchestration and system management

Use both frameworks together for comprehensive development support.

---

**Klaus Claude Framework** - 24 active agents + 2 skills (2 deprecated)
**Location**: `~/.claude/commands/kc/` and `~/.claude/agents/`

**Recent Changes:**
- ✅ **Consolidated** parallel-test, parallel-tester → parallel-debugger
- 🎯 **One Agent** for all parallel debugging needs
- ⚡ **More Efficient** - No delegation overhead

For individual agent help: `/kc:[agent-name] --help`
