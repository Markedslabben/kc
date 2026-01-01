# KC Framework - Klaus Claude Personal Tools

Personal agent framework and custom tools developed by Klaus.

**Namespace**: `kc-*` (Klaus Claude)
**Location**: `~/klauspython/kc/`
**Scope**: Personal tools, agents, and skills (separate from SuperClaude framework)

---

## Directory Structure

```
kc/
├── README.md                    ← This file
├── skills/
│   └── kc-docs/                 ← Python project documentation skill
│       ├── SKILL.md
│       ├── README.md
│       ├── scripts/
│       └── templates/
├── agents/                      ← Custom agents (when created)
├── commands/                    ← Custom slash commands (when created)
└── tools/                       ← Utility scripts and tools (when created)
```

---

## Installed Skills

### `kc-docs` - Python Project Documentation Generator

Automatically generates comprehensive Python project documentation with UML class diagrams, architecture diagrams, and code analysis.

**Location**: `~/klauspython/kc/skills/kc-docs/`
**Status**: ✅ Ready to use
**Invocation**: `/kc-docs`

**Features**:
- Analyzes Python codebase structure
- Generates UML class diagrams (PlantUML)
- Creates architecture diagrams (Mermaid)
- Auto-generates API documentation
- Provides code complexity metrics

**Quick Start**:
```bash
/kc-docs analyze ~/your/project
/kc-docs generate ~/your/project
```

**Documentation**:
- See: `~/klauspython/kc/skills/kc-docs/README.md`
- Quick start: `~/klauspython/kc/skills/kc-docs/QUICK_START.md`
- Full reference: `~/klauspython/kc/skills/kc-docs/SKILL.md`

---

## Framework Integration

### How Claude Code Finds Your Skills

Claude Code searches for skills in:
1. Global SuperClaude: `~/.claude/skills/`
2. Project-specific: `.claude/skills/`
3. **Personal KC**: `~/klauspython/kc/skills/` (optional)

**Note**: You may need to explicitly register the KC skills path with Claude Code.

### Naming Convention

All KC personal tools use the `kc-` prefix:
- `kc-docs` - Documentation generator
- `kc-*` - (future tools)

This distinguishes them from SuperClaude tools (`sc-*`) and others.

---

## Development Guidelines

When adding new tools to KC framework:

1. **Use `kc-` prefix** in the name
2. **Document thoroughly** - README.md, QUICK_START.md
3. **Place in appropriate subdirectory**:
   - Skills → `skills/kc-toolname/`
   - Agents → `agents/kc-toolname/`
   - Commands → `commands/kc-toolname/`
4. **Update this README** with tool description
5. **Test locally** before marking as ready

---

**Last Updated**: January 1, 2026
**Framework Status**: ✅ Active and expanding
