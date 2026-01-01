# KC Docs - Python Project Documentation Generator

A Claude Code skill for automatically generating comprehensive Python project documentation with UML class diagrams, architecture diagrams, and code analysis.

## ✅ Installation & Status

**Status**: Ready to use ✓
**Location**: `~/.claude/skills/kc-docs/`
**Last tested**: Successfully generated diagrams from test project

### What's Included

```
.claude/skills/kc-docs/
├── SKILL.md                 ← Main skill definition (register with Claude)
├── QUICK_START.md          ← 5-minute getting started guide
├── README.md               ← This file
├── scripts/
│   ├── analyze_project.py   ← Analyze Python codebase
│   ├── generate_diagrams.py ← Create UML and architecture diagrams
│   └── generate_docs.sh     ← Orchestration script
├── templates/
│   ├── PROJECT_README.md    ← Documentation template
│   └── .kc-docs-example.yaml ← Configuration example
└── examples/               ← Sample outputs (to be populated)
```

## 🚀 Quick Start

### 1. Use the Skill

Invoke directly in Claude Code:

```
/kc-docs analyze /path/to/your/project
```

### 2. Generate Documentation

```
/kc-docs generate /path/to/your/project
```

This creates:
- Architecture diagrams (Mermaid)
- Class diagrams (PlantUML)
- API reference
- Analysis report

### 3. View Results

```bash
cd docs/
cat ARCHITECTURE.md         # View in terminal
open ARCHITECTURE.md        # Open in Cursor with Ctrl+Shift+V
```

## 📋 Features

### Analysis Phase
- ✅ Scans Python files for structure
- ✅ Extracts classes, functions, and relationships
- ✅ Detects inheritance and dependencies
- ✅ Recommends appropriate diagrams
- ✅ Generates complexity metrics

### Diagram Generation
- ✅ **Architecture Diagram** - System component overview (Mermaid)
- ✅ **Class Diagram** - OOP structure and inheritance (PlantUML)
- ✅ **Dependency Graph** - Module relationships (Mermaid)
- ✅ **Auto-generated** - Exact code structure (pyreverse)

### Documentation
- ✅ **ARCHITECTURE.md** - System overview
- ✅ **API_REFERENCE.md** - Classes and functions
- ✅ **ANALYSIS_REPORT.md** - Code metrics and insights

## 🧪 Testing

The skill has been tested on a sample Python project:

```python
# Test project structure:
Person (base class)
├── Student (inherits Person)
└── Teacher (inherits Person)
Course (standalone)
```

**Test Results**:
- ✅ Correctly identified 4 classes
- ✅ Detected inheritance relationships
- ✅ Generated PlantUML class diagram
- ✅ Recommended appropriate diagrams
- ✅ Provided code insights

**Generated PlantUML diagram**:
```
class Person {
  __init__()
  get_info()
  is_adult()
}

class Student {
  __init__()
  get_student_info()
}

Student --|> Person
```

## 📦 Dependencies

### Required
- Python 3.8+
- Standard library only (ast, json, pathlib)

### Optional (for diagram rendering)
```bash
# Mermaid CLI (for high-quality Mermaid diagrams)
npm install -g @mermaid-js/mermaid-cli

# PlantUML (for professional UML diagrams)
sudo apt-get install plantuml

# pyreverse (for automatic class diagram extraction)
pip install pylint
```

## 🎯 How to Activate in Claude Code

The skill SKILL.md file is already created. To make it available:

1. **Automatic Discovery** - Claude Code may auto-discover it
2. **Manual Invocation** - Use `/kc-docs` directly
3. **Register** - If needed, copy SKILL.md to Claude Code plugin registry

## 📖 Documentation

- **[QUICK_START.md](./QUICK_START.md)** - Get started in 5 minutes
- **[SKILL.md](./SKILL.md)** - Complete skill reference with all options
- **[templates/](./templates/)** - Configuration and documentation templates

## 💡 Examples

### Analyze Before Generating

```bash
/kc-docs analyze ~/myproject
# Output: 12 modules, 45 classes, MEDIUM complexity
# Recommends: [architecture, class_diagram, dependency_graph]

/kc-docs generate ~/myproject
# Generates diagrams for all recommendations
```

### Configure Specific Behavior

Create `.kc-docs.yaml` in your project:

```yaml
analysis:
  min_classes_for_diagram: 5
  include_private: false

diagrams:
  architecture: true
  class_diagram: true
  dependency_graph: false  # Skip if too many imports
```

Then regenerate:

```bash
/kc-docs generate ~/myproject
```

## 🔧 Advanced Usage

### Limit to Specific Directories

```bash
/kc-docs analyze ~/myproject/src --max-depth 2
```

### Force Regeneration

```bash
/kc-docs generate ~/myproject --force
```

### Generate Specific Diagrams Only

```bash
/kc-docs generate ~/myproject --diagrams architecture,classes
```

## 📊 Output Structure

```
docs/
├── ARCHITECTURE.md
├── API_REFERENCE.md
├── ANALYSIS_REPORT.md
└── diagrams/
    ├── src/
    │   ├── architecture.mmd
    │   └── classes.puml
    └── generated/
        ├── architecture.svg
        ├── classes.svg
        └── dependencies.svg
```

## 🎨 Viewing Diagrams

### In Cursor Editor

1. Open `docs/ARCHITECTURE.md`
2. Press `Ctrl+Shift+V` for markdown preview
3. Click SVG links to view diagrams

**Recommended Cursor Extension**: `jebbs.plantuml` for `.puml` syntax highlighting

### In Browser

```bash
cd docs/diagrams/generated
open architecture.svg
```

Or serve locally:

```bash
cd docs
python3 -m http.server 8000
# Then visit: http://localhost:8000/diagrams/generated/
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No Python files found" | Check project path contains `.py` files |
| "Diagram rendering failed" | Install optional dependencies (see Requirements) |
| "Diagram is cluttered" | Use `--max-classes` to limit diagram complexity |
| "Documentation looks outdated" | Use `--force` to regenerate from scratch |

## 🚦 Next Steps

1. **First time?** Read [QUICK_START.md](./QUICK_START.md)
2. **Ready to use?** Try `/kc-docs analyze /your/project`
3. **Need customization?** Copy `.kc-docs-example.yaml` and edit
4. **Want to extend?** All scripts are modular and editable

---

## 📝 Notes

- **Version Control**: Commit source files (`.mmd`, `.puml`), gitignore generated SVGs
- **Maintenance**: Re-run generation after major refactoring
- **Sharing**: Export to PNG/PDF for non-technical stakeholders
- **Large Projects**: Limit diagram scope to avoid clutter

---

**Created**: January 1, 2026
**Status**: Production Ready ✓
**Last Tested**: Successfully generated UML class diagram from test project

For detailed documentation, see [SKILL.md](./SKILL.md)
