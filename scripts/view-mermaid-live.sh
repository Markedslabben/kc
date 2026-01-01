#!/bin/bash
#
# view-mermaid-live.sh - View Mermaid diagrams in live editor
#
# Usage:
#   ./view-mermaid-live.sh <path-to-.mmd-file>
#   ./view-mermaid-live.sh architecture.mmd
#   ./view-mermaid-live.sh docs/diagrams/src/classes.mmd
#
# Features:
#   - Reads the .mmd file
#   - Copies content to system clipboard
#   - Opens Mermaid Live in your browser
#   - Ready to paste with Ctrl+V
#

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if file argument provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Please provide a .mmd file path${NC}"
    echo "Usage: $0 <path-to-.mmd-file>"
    echo "Example: $0 docs/diagrams/src/architecture.mmd"
    exit 1
fi

FILE_PATH="$1"

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo -e "${RED}Error: File not found: $FILE_PATH${NC}"
    exit 1
fi

# Check if it's a Mermaid file
if [[ "$FILE_PATH" != *.mmd ]]; then
    echo -e "${RED}Warning: File does not have .mmd extension: $FILE_PATH${NC}"
    echo "Continuing anyway..."
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Mermaid Live Viewer${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "File: ${GREEN}$FILE_PATH${NC}"
echo -e "Size: ${GREEN}$(wc -c < "$FILE_PATH") bytes${NC}"
echo ""

# Read file content
FILE_CONTENT=$(cat "$FILE_PATH")

# Count lines and estimate rendering time
LINE_COUNT=$(echo "$FILE_CONTENT" | wc -l)
echo -e "Lines: ${GREEN}$LINE_COUNT${NC}"
echo ""

# Copy to clipboard
# Try xclip first (most common on Linux)
if command -v xclip &> /dev/null; then
    echo "$FILE_CONTENT" | xclip -selection clipboard
    echo -e "${GREEN}✓${NC} Content copied to clipboard (xclip)"
# Try xsel (alternative)
elif command -v xsel &> /dev/null; then
    echo "$FILE_CONTENT" | xsel --clipboard --input
    echo -e "${GREEN}✓${NC} Content copied to clipboard (xsel)"
# Try pbcopy (macOS)
elif command -v pbcopy &> /dev/null; then
    echo "$FILE_CONTENT" | pbcopy
    echo -e "${GREEN}✓${NC} Content copied to clipboard (pbcopy)"
# Try clip.exe (Windows/WSL)
elif command -v clip.exe &> /dev/null; then
    echo "$FILE_CONTENT" | clip.exe
    echo -e "${GREEN}✓${NC} Content copied to clipboard (clip.exe)"
else
    echo -e "${RED}✗${NC} Clipboard tool not found"
    echo "  Please install one of: xclip, xsel (Linux), pbcopy (macOS), or clip.exe (Windows)"
    exit 1
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Browser opening to ${GREEN}https://mermaid.live${NC}..."
echo "2. Click in the editor area on the left"
echo "3. Press ${GREEN}Ctrl+A${NC} to select all default content"
echo "4. Press ${GREEN}Ctrl+V${NC} to paste your diagram"
echo "5. It will render automatically on the right!"
echo ""

# Open Mermaid Live in browser
# Try different approaches for WSL/Windows/Linux
if command -v powershell.exe &> /dev/null; then
    # Windows/WSL - use powershell to open Windows browser
    powershell.exe -Command "Start-Process 'https://mermaid.live'"
    echo -e "${GREEN}✓${NC} Opening Mermaid Live in Windows browser..."
elif command -v wslview &> /dev/null; then
    # WSL with wslview
    wslview "https://mermaid.live"
    echo -e "${GREEN}✓${NC} Opening Mermaid Live..."
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "https://mermaid.live"
    echo -e "${GREEN}✓${NC} Opening Mermaid Live..."
elif command -v open &> /dev/null; then
    # macOS
    open "https://mermaid.live"
    echo -e "${GREEN}✓${NC} Opening Mermaid Live..."
else
    # Fallback - just show the URL
    echo -e "${BLUE}ℹ${NC} Please manually open: ${GREEN}https://mermaid.live${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "Ready to paste! The diagram content is in your clipboard."
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
