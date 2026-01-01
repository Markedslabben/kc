# KC Docs - Quick Start Guide

Get project documentation generated in 5 minutes.

## Installation

The skill is already installed at `~/.claude/skills/kc-docs/`

### Check Dependencies

```bash
# Check if Python 3.8+ is available
python3 --version

# Optional: Install Mermaid CLI (for better diagram rendering)
npm install -g @mermaid-js/mermaid-cli

# Optional: Install PlantUML (for detailed class diagrams)
sudo apt-get install plantuml
```

## Usage

### 1. Analyze Your Project

First, let's analyze what diagrams your project needs:

```bash
/kc-docs analyze /path/to/your/project
```

This will show:
- Number of modules and classes
- Project complexity
- Recommended diagrams for your codebase

**Example output:**
```
Project Analysis Results:
- Total modules: 8
- Total classes: 24
- Total functions: 156
- Complexity: MEDIUM
- Recommended diagrams: [architecture, class_diagram, dependency_graph]
```

### 2. Generate Documentation

Once you understand your project structure, generate full documentation:

```bash
/kc-docs generate /path/to/your/project
```

This creates:
```
docs/
├── ARCHITECTURE.md           ← Start here
├── API_REFERENCE.md
├── ANALYSIS_REPORT.md
└── diagrams/
    ├── src/                  (source diagram definitions)
    │   ├── architecture.mmd
    │   └── classes.puml
    └── generated/            (rendered SVG/PNG)
        ├── architecture.svg
        └── classes.svg
```

### 3. View Your Documentation

Open the generated files:

```bash
# In Cursor: Open docs/ARCHITECTURE.md
# Press: Ctrl+Shift+V to preview

# Or in browser:
open docs/ARCHITECTURE.md
```

## Examples

### Small Project (< 5 classes)

```bash
/kc-docs analyze ~/myproject
# → Recommends: architecture only

/kc-docs generate ~/myproject
# → Creates simple architecture diagram
```

### Medium Project (5-30 classes)

```bash
/kc-docs analyze ~/myproject
# → Recommends: architecture, class_diagram, dependency_graph

/kc-docs generate ~/myproject
# → Creates detailed diagrams and documentation
```

### Large Project (> 30 classes)

```bash
/kc-docs analyze ~/myproject --limit-classes 30
# → Analyzes top 30 classes to avoid clutter

/kc-docs generate ~/myproject
# → Creates focused diagrams highlighting main components
```

## Viewing Diagrams

### In Cursor

1. Open `docs/ARCHITECTURE.md`
2. Press `Ctrl+Shift+V` for markdown preview
3. Click diagram links to view SVGs

**Install PlantUML extension for better preview:**
- Extension: `jebbs.plantuml`
- Provides syntax highlighting and preview for `.puml` files

### In Browser

SVG files open in any modern browser:

```bash
# Direct file open
open docs/diagrams/generated/architecture.svg

# Or serve with Python
cd docs && python3 -m http.server 8000
# Then visit: http://localhost:8000/diagrams/generated/
```

## Configuration

For fine-tuned control, create `.kc-docs.yaml` in your project:

```yaml
# .kc-docs.yaml
analysis:
  min_classes_for_diagram: 3
  max_depth: 3

diagrams:
  architecture: true
  class_diagram: true
  dependency_graph: false  # Skip if too many imports
```

## Troubleshooting

### "No Python files found"

Check that your project path contains `.py` files:

```bash
find /your/project -name "*.py" | head -5
```

### "Diagrams failed to render"

Rendering requires optional tools. Install them:

```bash
# For Mermaid diagrams
npm install -g @mermaid-js/mermaid-cli

# For PlantUML diagrams
sudo apt-get install plantuml

# Test installation
mmdc --version
plantuml -version
```

### "Diagram is too complex"

Large codebases with 50+ classes create cluttered diagrams. Limit the analysis:

```bash
/kc-docs analyze /path --max-classes 20
```

## Tips

- **First time?** Start with `analyze` to understand your project structure
- **Large projects?** Commit source files (`.mmd`, `.puml`), gitignore generated diagrams
- **Keep updated?** Re-run after major refactoring to keep diagrams synced
- **Share with non-tech?** Export diagrams to PNG or PDF

## Next Steps

- Read [SKILL.md](./SKILL.md) for full reference
- View [examples](./examples/) for sample output
- Check [templates](./templates/) for customization

---

**Need help?** Edit the skill or check documentation in `~/.claude/skills/kc-docs/`
