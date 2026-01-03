#!/bin/bash
#
# View Mermaid diagrams directly in Mermaid Live Editor
# No manual pasting required - diagram loads automatically!
#
# Usage:
#   view-mermaid-live.sh <file.mmd>
#   view-mermaid-live.sh classes.mmd --copy  (also copy to clipboard)
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/view-mermaid-live.py" "$@"
