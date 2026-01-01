# Klaus Claude (KC) Framework

Personal AI development framework and custom agent collection by Klaus.

**Version**: 1.0.0
**Namespace**: KC (Klaus Claude)
**Repository**: `~/klauspython/kc/`

---

## Framework Purpose

KC is Klaus's personal collection of custom agents, skills, and tools that extend Claude Code functionality. Unlike SuperClaude (SC) which is a third-party framework, KC contains only agents and tools developed specifically for Klaus's workflows.

---

## KC Agents

Custom agents built by Klaus for specialized workflows:

### kc-parallel-orchestrator
- **Trigger**: Complex tasks spanning >3 files OR >2 directories OR explicit parallel request
- **Purpose**: Overhead-optimized parallel task execution using git worktrees
- **Location**: `~/klauspython/kc/agents/parallel-orchestrator/`
- **Scripts**: task-splitter.py, setup-worktree.sh, run-parallel.sh, merge-results.sh
- **Status**: ✅ Active

### kc-parallel-tester
- **Trigger**: `/ptest`, `/parallel-test`, "test hypotheses in parallel"
- **Purpose**: Test multiple bug hypotheses in parallel using falsification principle
- **Location**: `~/klauspython/kc/agents/parallel-tester/`
- **Scripts**: Hypothesis testing with git worktrees
- **Status**: ✅ Active

### kc-parallel-debugger
- **Trigger**: Complex debugging scenarios requiring systematic hypothesis testing
- **Purpose**: Full debug pipeline - uses parallel-tester for hypothesis testing, then proposes fixes
- **Location**: `~/klauspython/kc/agents/parallel-debugger/`
- **Scripts**: Debugging workflow orchestration
- **Status**: ✅ Active

### kc-task-velocity-estimator
- **Trigger**: Automatically runs on complex tasks (background agent)
- **Purpose**: Track task completion times and provide data-driven time estimates
- **Location**: `~/klauspython/kc/agents/task-velocity-estimator/`
- **Database**: `data/velocity.db` (SQLite - stores historical task data)
- **Status**: ✅ Active (Background)

### kc-nivametoden
- **Trigger**: Document writing requests, Norwegian "Nivåmetoden" structure
- **Purpose**: Transform documents using Pyramid Principle (MECE, SCQA, BLUF)
- **Location**: `~/klauspython/kc/agents/nivametoden/`
- **Tools**: Document structuring and organization
- **Status**: ✅ Active

---

## KC Skills

Custom skills for Klaus's workflows (invoked via `/kc:skill-name`):

### /kc:md2docx
- **Purpose**: Convert markdown documents to Word (.docx) format with intelligent pre-processing
- **Location**: `~/klauspython/kc/skills/md2docx.md`
- **Tools**: Uses document conversion utilities
- **Status**: ✅ Active

### /kc:parallel
- **Purpose**: Manual parallel orchestration command with overhead optimization
- **Location**: `~/klauspython/kc/skills/parallel.md`
- **Usage**: `/kc:parallel "task description"`, `/kc:parallel --analyze-repo`
- **Modes**: Analysis, quick setup, conflict check, repository analysis
- **Status**: ✅ Active

---

## KC Commands

Custom commands for Klaus's workflows:

*To be added*

---

## Integration with Claude Code

KC agents and skills are symlinked to make them globally available:

### Agent Symlinks
```bash
~/.claude/agents/kc-parallel-orchestrator.md     → ~/klauspython/kc/agents/parallel-orchestrator/agent.md
~/.claude/agents/kc-parallel-tester.md           → ~/klauspython/kc/agents/parallel-tester/agent.md
~/.claude/agents/kc-parallel-debugger.md         → ~/klauspython/kc/agents/parallel-debugger/agent.md
~/.claude/agents/kc-task-velocity-estimator.md   → ~/klauspython/kc/agents/task-velocity-estimator/agent.md
~/.claude/agents/kc-nivametoden.md               → ~/klauspython/kc/agents/nivametoden/agent.md
```

### Skill Symlinks
```bash
~/.claude/skills/kc-md2docx.md    → ~/klauspython/kc/skills/md2docx.md
~/.claude/skills/kc-parallel.md   → ~/klauspython/kc/skills/parallel.md
```

### Framework Reference
KC framework is referenced in `~/.claude/CLAUDE.md`:
```markdown
# ═══════════════════════════════════════════════════
# Klaus Claude (KC) Framework
# ═══════════════════════════════════════════════════
[KC agents and skills documentation]
```

---

## Directory Structure

```
~/klauspython/kc/
├── KC.md                            # This file - framework documentation
├── README.md                        # User-facing documentation
├── agents/                          # Custom agents
│   ├── parallel-orchestrator/
│   │   ├── agent.md                 # Agent definition
│   │   ├── scripts/                 # Supporting tools
│   │   └── README.md
│   ├── analyze-prompt/
│   └── parallel-debugger/
├── skills/                          # Custom skills (/kc:*)
├── commands/                        # Custom commands
│   └── kc/
└── docs/                            # Framework documentation
    └── architecture.md
```

---

## Agent Development Guidelines

When creating KC agents:

1. **Naming**: Prefix with `kc-` to distinguish from SC/plugin agents
2. **Location**: Store in `~/klauspython/kc/agents/[agent-name]/`
3. **Structure**: Follow plugin-dev standards (frontmatter with examples)
4. **Tools**: Use Bash calls to scripts (no MCP needed for personal use)
5. **Symlink**: Link to `~/.claude/agents/` for global availability

---

## KC vs SuperClaude (SC)

| Feature | SuperClaude (SC) | Klaus Claude (KC) |
|---------|------------------|-------------------|
| **Origin** | Third-party framework | Klaus's personal work |
| **Agents** | 14 bundled agents | Custom agents only |
| **Purpose** | General development | Klaus-specific workflows |
| **Namespace** | `/sc:*` commands | `/kc:*` commands |
| **Location** | `~/.claude/` | `~/klauspython/kc/` |
| **Updates** | External updates | Klaus maintains |

Both frameworks work independently and can be used together.

---

## Version History

- **1.0.0** (2025-01-01): Initial KC framework creation
  - Created directory structure
  - Migrated parallel-orchestrator as first KC agent
  - Established KC namespace and conventions

---

## License

MIT - Personal use by Klaus
