# KC Framework Architecture

## Overview

Klaus Claude (KC) is a personal AI development framework built as a parallel system to SuperClaude (SC). It contains only custom agents, skills, and tools developed specifically for Klaus's workflows.

## Design Principles

### 1. Independence
- KC operates independently from SuperClaude
- Can be used with or without SC
- No dependencies on third-party frameworks

### 2. Simplicity
- No MCP overhead for personal tools
- Direct Bash calls to scripts
- Minimal abstraction layers

### 3. Clear Ownership
- All KC components prefixed with `kc-`
- Clear separation from SC and plugin agents
- Easy to identify custom vs. bundled components

## Directory Structure

```
~/klauspython/kc/
├── KC.md                            # Framework documentation
├── README.md                        # User guide
├── agents/                          # Custom agents
│   └── [agent-name]/
│       ├── agent.md                 # Agent definition (frontmatter + system prompt)
│       ├── scripts/                 # Supporting tools (Bash callable)
│       ├── shared/                  # Python utilities
│       └── README.md                # Agent-specific docs
├── skills/                          # Custom skills (/kc:*)
│   └── [skill-name].md
├── commands/                        # Custom commands
│   └── kc/
│       └── [command-name].sh
└── docs/                            # Framework documentation
    └── architecture.md              # This file
```

## Integration Points

### Symlinks to Claude Code
```
~/.claude/agents/kc-[agent-name].md → ~/klauspython/kc/agents/[agent-name]/agent.md
```

### CLAUDE.md Reference
```markdown
# ═══════════════════════════════════════════════════
# Klaus Claude (KC) Framework
# ═══════════════════════════════════════════════════
[KC framework section...]
```

## Agent Architecture

### Agent Definition (agent.md)
```markdown
---
name: kc-[agent-name]
description: Use this agent when... Examples: <example>...</example>
model: inherit
color: [color]
tools: ["Read", "Write", "Bash", "Grep", "Glob"]
---

You are [agent description]...
[System prompt following plugin-dev standards]
```

### Supporting Scripts
- Located in `agents/[agent-name]/scripts/`
- Called via Bash tool from agent
- No MCP wrapper needed for personal use
- Can be Python, shell, or any executable

### Shared Utilities
- Located in `agents/[agent-name]/shared/`
- Reusable Python modules
- Imported by scripts as needed

## Tool Execution Pattern

```
Agent receives task
  ↓
Analyzes requirements
  ↓
Calls script via Bash tool:
  bash /home/klaus/klauspython/kc/agents/[agent]/scripts/tool.py --args
  ↓
Script executes (uses shared utilities if needed)
  ↓
Returns results to agent
  ↓
Agent processes and responds to user
```

**No MCP needed** - direct Bash execution with absolute paths.

## Comparison: KC vs SC vs Plugins

| Aspect | SuperClaude (SC) | Claude Plugins | Klaus Claude (KC) |
|--------|------------------|----------------|-------------------|
| **Origin** | Third-party framework | Anthropic/marketplace | Klaus personal |
| **Purpose** | General development | Specific capabilities | Klaus workflows |
| **Components** | 14+ agents, modes, rules | Agents, skills, commands | Custom agents only |
| **Namespace** | `/sc:*` | Plugin-specific | `/kc:*` |
| **Location** | `~/.claude/` | `~/.claude/plugins/` | `~/klauspython/kc/` |
| **Updates** | External | Marketplace | Klaus maintains |
| **Complexity** | Full framework | Variable | Minimal |

All three systems coexist independently in Claude Code.

## Development Workflow

### Adding New KC Agent

1. **Create directory structure**:
   ```bash
   mkdir -p ~/klauspython/kc/agents/[agent-name]/{scripts,shared}
   ```

2. **Create agent.md** with proper frontmatter (plugin-dev standards)

3. **Add supporting scripts**:
   ```bash
   touch ~/klauspython/kc/agents/[agent-name]/scripts/tool.py
   chmod +x ~/klauspython/kc/agents/[agent-name]/scripts/tool.py
   ```

4. **Create symlink**:
   ```bash
   ln -s ~/klauspython/kc/agents/[agent-name]/agent.md \
         ~/.claude/agents/kc-[agent-name].md
   ```

5. **Update KC.md** with agent documentation

6. **Test**: Invoke agent and verify functionality

### Agent Best Practices

- ✅ Prefix name with `kc-` for clarity
- ✅ Use absolute paths in scripts (not relative)
- ✅ Include 2-4 examples in description frontmatter
- ✅ Follow plugin-dev standards for triggering
- ✅ Document scripts and tools in agent's README.md
- ✅ Keep tools simple - direct Bash calls
- ❌ Don't add MCP complexity unless distributing
- ❌ Don't mix KC and SC conventions

## Version Control

KC framework is version-controlled separately:
- Location: `~/klauspython/kc/.git`
- Independent from `~/.claude/` (SuperClaude)
- Can be backed up, shared, or forked independently

## Future Enhancements

Planned KC components:
- `kc-analyze-prompt`: Prompt optimization agent
- `kc-parallel-debugger`: Parallel hypothesis testing
- `/kc:*` skills for common workflows
- Custom commands for automation

## Summary

KC framework provides Klaus with:
- **Clear ownership**: All custom work in one place
- **Simple architecture**: No unnecessary complexity
- **Independence**: Works with or without SuperClaude
- **Maintainability**: Easy to update and extend
- **Organization**: Clear separation from bundled components

This architecture enables rapid development of personal tools while maintaining clean separation from third-party frameworks.
