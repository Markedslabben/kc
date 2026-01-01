# KC Framework - Setup & Discovery Guide

Your personal Claude Code tools framework is now fully configured for automatic discovery.

## ✅ Framework Setup Complete

### Directory Structure

```
~/klauspython/kc/
├── plugin.json                    ← Plugin registration
├── .claude-config.json            ← Discovery configuration
├── README.md                       ← Framework overview
├── SETUP_GUIDE.md                 ← This file
│
├── agents/                         ← Autonomous agents
│   ├── parallel-orchestrator.md    ✅ Parallel task execution
│   ├── parallel-debugger.md        ✅ Multi-hypothesis testing
│   ├── parallel-tester.md          ✅ Concurrent test execution
│   ├── task-velocity-estimator.md  ✅ Time estimation
│   └── nivametoden.md              ✅ Document reorganization
│
├── skills/                         ← Reusable skills
│   └── kc-docs/                    ✅ Documentation generator
│       ├── SKILL.md
│       ├── scripts/
│       └── templates/
│
├── commands/                       ← Custom commands
│   └── kc/                         ← Main KC command
│
└── docs/                           ← Framework documentation
```

## 🔍 Claude Code Discovery

Claude Code will now discover your KC framework through:

### 1. Automatic Discovery
- Scans `~/klauspython/kc/agents/` for `*.md` files
- Loads agent definitions with YAML frontmatter
- Registers skills from `skills/*/SKILL.md`
- Makes tools available via `kc-` namespace

### 2. Manual Registration (if needed)
Add to your Claude Code settings:

```json
{
  "pluginPaths": [
    "~/.claude/plugins",
    "~/klauspython/kc"
  ],
  "frameworks": ["kc"]
}
```

### 3. Usage
All tools are automatically available:

```bash
/kc-docs analyze ~/your/project
/kc-docs generate ~/your/project

# Agents are triggered automatically when appropriate:
# - User: "Can you debug this bug with multiple hypotheses?"
# → Triggers: parallel-debugger agent

# - User: "How long will this 5-part feature take?"
# → Triggers: task-velocity-estimator agent
```

## 📋 Available Tools

### Agents (Autonomous)

These agents are triggered automatically when Claude Code detects relevant conditions:

| Agent | Trigger Condition | Purpose |
|-------|-------------------|---------|
| **parallel-orchestrator** | Need parallel task execution | Orchestrate multi-worktree development |
| **parallel-debugger** | Testing multiple bug hypotheses | Investigate root causes in parallel |
| **parallel-tester** | Running comprehensive tests | Execute independent tests concurrently |
| **task-velocity-estimator** | Need time estimates | Provide data-driven estimates |
| **nivametoden** | Complex document organization | Restructure into clear hierarchies |

### Skills (On-Demand)

These are invoked explicitly:

| Skill | Command | Purpose |
|-------|---------|---------|
| **kc-docs** | `/kc-docs` | Generate Python project documentation |

## 🚀 Next Steps

### 1. Test Agent Discovery

Try phrases that should trigger agents:

```
"I have a bug with 3 possible causes - can you investigate all of them?"
→ Triggers: parallel-debugger

"Can you estimate how long this feature will take?"
→ Triggers: task-velocity-estimator

"I need to parallelize these 4 independent refactoring tasks"
→ Triggers: parallel-orchestrator
```

### 2. Use Skills Directly

```bash
/kc-docs analyze ~/your/project
/kc-docs generate ~/your/project
```

### 3. Extend KC Framework

To add new agents:
1. Create `agents/my-agent.md` with proper frontmatter
2. Update `plugin.json` to register
3. Agent is auto-discovered

To add new skills:
1. Create `skills/kc-newskill/SKILL.md`
2. Update `plugin.json` to register
3. Skill is auto-discovered

## 📚 Documentation

- **KC Overview**: `README.md`
- **Agent Development**: Reference from Claude Code
- **Skill Reference**: `skills/kc-docs/SKILL.md`
- **This Guide**: `SETUP_GUIDE.md`

## ✨ Framework Benefits

✅ Personal tools separate from SuperClaude
✅ All tools use consistent `kc-*` namespace  
✅ Auto-discovery by Claude Code
✅ Easy to extend with new agents/skills
✅ Proper plugin structure for future distribution
✅ Version controlled with project

## 🔧 Troubleshooting

**Agent not triggering?**
- Check the triggering examples in agent frontmatter
- Use very similar phrasing to examples
- Agent requires exact conditions to be met

**Skill not found?**
- Verify `skills/kc-docs/SKILL.md` exists
- Check `.claude-config.json` is correct
- Restart Claude Code if needed

**Discovery not working?**
- Verify `plugin.json` is valid JSON
- Check `.claude-config.json` exists
- Ensure directory structure matches

---

**Framework Version**: 0.1.0
**Last Updated**: January 1, 2026
**Status**: ✅ Production Ready
