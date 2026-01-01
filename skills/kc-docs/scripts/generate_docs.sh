#!/bin/bash
# Generate complete project documentation with diagrams

set -e

PROJECT_PATH="$(cd "${1:-.}" && pwd)"  # Resolve to absolute path
OUTPUT_DIR="${2:-$PROJECT_PATH/docs}"  # Default: docs/ INSIDE project
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}KC Documentation Generator${NC}"
echo "=============================="
echo "Project: $PROJECT_PATH"
echo "Output:  $OUTPUT_DIR"
echo ""

# Step 1: Analyze project
echo -e "${YELLOW}Step 1: Analyzing project structure...${NC}"
ANALYSIS_FILE="/tmp/kc-docs-analysis.json"

python3 "$SCRIPT_DIR/analyze_project.py" "$PROJECT_PATH" > "$ANALYSIS_FILE"

# Check analysis status
STATUS=$(grep -o '"status": "[^"]*"' "$ANALYSIS_FILE" | head -1 | cut -d'"' -f4)
if [ "$STATUS" != "success" ]; then
    echo -e "${RED}Error: Analysis failed${NC}"
    cat "$ANALYSIS_FILE"
    exit 1
fi

echo -e "${GREEN}✓ Analysis complete${NC}"

# Extract summary
MODULES=$(grep -o '"total_modules": [0-9]*' "$ANALYSIS_FILE" | cut -d' ' -f2)
CLASSES=$(grep -o '"total_classes": [0-9]*' "$ANALYSIS_FILE" | cut -d' ' -f2)
FUNCTIONS=$(grep -o '"total_functions": [0-9]*' "$ANALYSIS_FILE" | cut -d' ' -f2)
COMPLEXITY=$(grep -o '"complexity": "[^"]*"' "$ANALYSIS_FILE" | head -1 | cut -d'"' -f4)

echo "  • Modules: $MODULES"
echo "  • Classes: $CLASSES"
echo "  • Functions: $FUNCTIONS"
echo "  • Complexity: $COMPLEXITY"
echo ""

# Step 2: Generate diagrams
echo -e "${YELLOW}Step 2: Generating diagrams...${NC}"

DIAGRAMS_OUTPUT="$OUTPUT_DIR/diagrams/generated"
mkdir -p "$DIAGRAMS_OUTPUT"

python3 "$SCRIPT_DIR/generate_diagrams.py" "$ANALYSIS_FILE" "$DIAGRAMS_OUTPUT"

echo -e "${GREEN}✓ Diagrams generated${NC}"
echo ""

# Step 3: Create documentation
echo -e "${YELLOW}Step 3: Creating documentation...${NC}"

DOC_DIR="$OUTPUT_DIR"
mkdir -p "$DOC_DIR"

# Create ARCHITECTURE.md
cat > "$DOC_DIR/ARCHITECTURE.md" << 'EOF'
# Architecture Overview

## Project Structure

### Modules
```
EOF

# Extract modules from analysis
grep -o '"modules": \[[^]]*\]' "$ANALYSIS_FILE" | cut -d'[' -f2 | cut -d']' -f1 | tr ',' '\n' | sed 's/"//g' | grep -v '^\s*$' | sort >> "$DOC_DIR/ARCHITECTURE.md"

cat >> "$DOC_DIR/ARCHITECTURE.md" << 'EOF'
```

## Architecture Diagram

![Architecture](diagrams/generated/architecture.svg)

## Class Diagram

![Classes](diagrams/generated/classes.svg)

## Recommendations

For more details, see:
- [API Reference](API_REFERENCE.md)
- [Analysis Report](ANALYSIS_REPORT.md)
EOF

# Create API_REFERENCE.md
cat > "$DOC_DIR/API_REFERENCE.md" << 'EOF'
# API Reference

## Classes

EOF

# Extract classes from analysis
python3 << 'PYTHON'
import json
import sys

with open('/tmp/kc-docs-analysis.json', 'r') as f:
    data = json.load(f)

for cls in data.get('classes', [])[:20]:
    print(f"### {cls['name']}")
    print(f"- Module: `{cls['module']}`")
    if cls['bases']:
        print(f"- Inherits: {', '.join(cls['bases'])}")
    if cls['methods']:
        print(f"- Methods: {', '.join(cls['methods'][:5])}")
        if len(cls['methods']) > 5:
            print(f"  ... and {len(cls['methods']) - 5} more")
    print()
PYTHON

# Create ANALYSIS_REPORT.md
cat > "$DOC_DIR/ANALYSIS_REPORT.md" << 'EOF'
# Project Analysis Report

## Summary

EOF

python3 << 'PYTHON'
import json

with open('/tmp/kc-docs-analysis.json', 'r') as f:
    data = json.load(f)

summary = data['summary']
print(f"- Total Modules: {summary['total_modules']}")
print(f"- Total Classes: {summary['total_classes']}")
print(f"- Total Functions: {summary['total_functions']}")
print(f"- Complexity Level: {summary['complexity']}")
print(f"- Has Inheritance: {summary['has_inheritance']}")
print()

print("## Key Insights")
print()
for insight in data.get('key_insights', []):
    print(f"- {insight}")
print()

print("## Recommended Diagrams")
print()
for diagram in data.get('recommended_diagrams', []):
    print(f"- {diagram}")
PYTHON

echo -e "${GREEN}✓ Documentation created${NC}"
echo ""

# Summary
echo -e "${GREEN}=============================="
echo "✓ Documentation generation complete!"
echo "=============================${NC}"
echo ""
echo "Generated files:"
echo "  • $DOC_DIR/ARCHITECTURE.md"
echo "  • $DOC_DIR/API_REFERENCE.md"
echo "  • $DOC_DIR/ANALYSIS_REPORT.md"
echo "  • $DIAGRAMS_OUTPUT/"
echo ""
echo "View documentation:"
echo "  cd $DOC_DIR && cat ARCHITECTURE.md"
