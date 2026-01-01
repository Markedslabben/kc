# Mermaid Live Viewer Tool

Quick tool to view and edit Mermaid diagrams in the live editor at https://mermaid.live

## Usage

### Via Claude Code Command

```bash
/view-mermaid docs/diagrams/src/architecture.mmd
```

### Via Direct Script

```bash
./kc/scripts/view-mermaid-live.sh docs/diagrams/src/architecture.mmd
```

### Via Bash

```bash
bash /home/klaus/klauspython/kc/scripts/view-mermaid-live.sh <path-to-file>
```

## What It Does

1. **Reads** your Mermaid diagram file
2. **Copies** the entire content to your system clipboard
3. **Opens** https://mermaid.live in your default browser
4. **Shows** clear instructions for pasting

## Quick Workflow

```
/view-mermaid architecture.mmd
  ↓ (Browser opens to Mermaid Live)
  ↓ Click in the left editor panel
  ↓ Ctrl+A (select all default content)
  ↓ Ctrl+V (paste your diagram)
  ↓ (Rendered instantly on the right side!)
```

## Examples

### View Architecture Diagram
```bash
/view-mermaid docs/diagrams/src/architecture.mmd
```

### View Class Diagram
```bash
/view-mermaid docs/diagrams/src/classes.mmd
```

### View Dependencies Diagram
```bash
/view-mermaid docs/diagrams/src/dependencies.mmd
```

### From Any Directory
```bash
cd ~/projects/solkraftahlsell
/view-mermaid docs/diagrams/src/architecture.mmd
```

## Features

✅ Automatic clipboard copying
✅ Cross-platform support (Windows/WSL, Linux, macOS)
✅ Browser auto-launch
✅ Color-coded output for easy reading
✅ File validation
✅ Line/byte counting

## Supported Platforms

| Platform | Status | Method |
|----------|--------|--------|
| **Windows (via WSL)** | ✓ | powershell.exe / clip.exe |
| **Linux** | ✓ | xclip / xsel |
| **macOS** | ✓ | pbcopy |
| **Browser** | ✓ | Any (Firefox, Chrome, Edge) |

## Troubleshooting

### "Clipboard tool not found"
Install one of these depending on your platform:

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
```

**macOS:**
- `pbcopy` is built-in

**Windows (WSL):**
- `clip.exe` is built-in
- Or install `xclip`: `apt-get install xclip`

### Browser Doesn't Open
The script attempts to auto-open your browser. If it fails:
1. Manually open https://mermaid.live
2. Your diagram is already in your clipboard
3. Paste with Ctrl+V

### Clipboard Not Working
Try these alternatives:

**Option 1: Display the content**
```bash
cat docs/diagrams/src/architecture.mmd
```
Then copy manually from the terminal.

**Option 2: Use a different clipboard tool**
```bash
cat docs/diagrams/src/architecture.mmd | xsel --clipboard --input
# or
cat docs/diagrams/src/architecture.mmd | pbcopy
```

## Tips & Tricks

### Quick Edit Loop
1. `/view-mermaid architecture.mmd` - View in live editor
2. Edit in the live editor (on the right side)
3. When satisfied, copy the new version from Mermaid Live
4. Paste into your `architecture.mmd` file
5. Commit to git

### Comparing Versions
Open multiple Mermaid Live tabs to compare:
```bash
# Terminal 1
/view-mermaid architecture.mmd

# Terminal 2 (new terminal)
/view-mermaid classes.mmd
```

### Integration with Development

**VS Code + Mermaid Extension:**
1. Install "Markdown Preview Mermaid Support"
2. Preview `.md` files with diagrams
3. Use `/view-mermaid` for live editing

**Commit Workflow:**
```bash
# View your diagram
/view-mermaid docs/diagrams/src/architecture.mmd

# Make edits in live editor if needed
# Copy updated content and save to file

# Commit
git add docs/diagrams/src/architecture.mmd
git commit -m "docs: update architecture diagram"
```

## Files

- **Script**: `/home/klaus/klauspython/kc/scripts/view-mermaid-live.sh`
- **Command**: `/home/klaus/.claude/commands/view-mermaid.md`
- **Docs**: This file

## Requirements

- Bash 4.0+
- One of: xclip, xsel, pbcopy, or clip.exe
- A web browser (Firefox, Chrome, Edge, Safari)
- Internet connection (Mermaid Live is a web app)
