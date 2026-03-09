#!/usr/bin/env python3
"""
View Mermaid diagrams directly in Mermaid Live Editor.

This script encodes a Mermaid diagram file and opens it directly in browser,
no manual pasting required!

Usage:
    python view-mermaid-live.py <path-to-mermaid-file.mmd>
    python view-mermaid-live.py diagram.mmd --copy  # Also copy to clipboard

Examples:
    python view-mermaid-live.py classes.mmd
    python view-mermaid-live.py /path/to/architecture.mmd
"""

import sys
import json
import base64
import zlib
import webbrowser
import subprocess
from pathlib import Path


def ensure_preferred_theme(mermaid_code: str) -> str:
    """
    Ensure the Mermaid code has a theme configuration.

    Injects Klaus' preferred theme config if no theme is specified.
    Keeps existing theme config if present.
    """
    # Klaus preferred theme configuration
    SOLID_THEME = "%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'primaryColor': '#e3f2fd', 'primaryTextColor': '#0d1b2a', 'primaryBorderColor': '#1e88e5', 'secondaryColor': '#e8f5e9', 'secondaryTextColor': '#1b5e20', 'tertiaryColor': '#fff8e1', 'tertiaryTextColor': '#e65100', 'lineColor': '#37474f', 'textColor': '#0d1b2a', 'fontFamily': 'Arial, Helvetica, sans-serif', 'fontSize': '16px'}}}%%"

    lines = mermaid_code.strip().split('\n')

    # Check if first line has %%{init - keep existing theme config
    if lines and lines[0].strip().startswith('%%{init'):
        return '\n'.join(lines)
    else:
        # Inject preferred theme at the beginning
        return SOLID_THEME + '\n\n' + mermaid_code


def encode_for_mermaid_live(mermaid_code: str) -> tuple[str, str]:
    """
    Encode Mermaid code for use in Mermaid Live URL.

    Mermaid Live supports two formats:
    1. pako: (compressed) - shorter URLs but complex encoding
    2. base64: (uncompressed) - longer URLs but reliable

    Returns (encoded_data, format_prefix)
    """
    # Apply preferred theme if not already specified
    mermaid_code = ensure_preferred_theme(mermaid_code)

    # Create the state object that Mermaid Live expects
    state = {
        "code": mermaid_code,
        "mermaid": {"theme": "base"},
        "autoSync": True,
        "updateDiagram": True,
        "updateEditor": True
    }

    # Convert to JSON string
    json_str = json.dumps(state)

    # Use simple base64 encoding (more reliable than pako)
    b64 = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')
    return b64, "base64"


def copy_to_clipboard(text: str) -> bool:
    """Copy text to Windows clipboard from WSL."""
    try:
        process = subprocess.Popen(
            ['/mnt/c/Windows/System32/clip.exe'],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input=text)
        return process.returncode == 0
    except Exception as e:
        print(f"Warning: Could not copy to clipboard: {e}")
        return False


def open_in_browser(url: str) -> bool:
    """Open URL in default browser (handles WSL)."""
    try:
        # Try WSL approach first (opens in Windows browser)
        result = subprocess.run(
            ['powershell.exe', '-Command', f'Start-Process "{url}"'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True
    except:
        pass

    # Fallback to Python's webbrowser
    try:
        webbrowser.open(url)
        return True
    except:
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: Please provide a Mermaid file path")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    copy_flag = '--copy' in sys.argv

    # Handle WSL paths
    if str(file_path).startswith('/mnt/c'):
        # Already a WSL path, use as-is
        pass
    elif not file_path.is_absolute():
        file_path = Path.cwd() / file_path

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    # Read the Mermaid file
    print(f"📄 Reading: {file_path.name}")
    mermaid_code = file_path.read_text(encoding='utf-8')

    # Remove comment lines that might cause issues (lines starting with %%)
    # Keep them for now as Mermaid Live handles them

    # Encode for Mermaid Live
    print("🔧 Encoding diagram...")
    encoded, format_prefix = encode_for_mermaid_live(mermaid_code)

    # Build URL
    url = f"https://mermaid.live/edit#{format_prefix}:{encoded}"
    print(f"   Format: {format_prefix}")

    # Optionally copy to clipboard
    if copy_flag:
        if copy_to_clipboard(mermaid_code):
            print("📋 Copied diagram code to clipboard")

    # Open in browser
    print("🌐 Opening in browser...")
    if open_in_browser(url):
        print("✅ Diagram opened in Mermaid Live!")
        print(f"\n   File: {file_path.name}")
        print(f"   Lines: {len(mermaid_code.splitlines())}")
    else:
        print("❌ Could not open browser automatically")
        print(f"\nManual URL:\n{url[:100]}...")

    return 0


if __name__ == '__main__':
    sys.exit(main())
