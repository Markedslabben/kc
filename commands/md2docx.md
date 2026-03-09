---
name: md2docx
description: "Convert markdown to professional Word documents with intelligent pre-processing (direct skill)"
category: documentation
complexity: standard
---

# /kc:md2docx - Markdown to Word Conversion (Direct Skill)

> **KC Framework Direct Skill**: Convert markdown files to professional Word documents with automatic enhancement.

## Quick Access
This is a direct skill shortcut. Also available as:
- `/md2docx` - Global skill (same functionality)

## Usage
```
/kc:md2docx [file.md] [--template solkraft|enok|custom]
```

## What It Does
Directly activates the md2docx conversion skill which:
1. **Pre-processes** markdown (removes emojis, fixes tables, converts ASCII diagrams)
2. **Enhances** content (professional tone, proper formatting)
3. **Converts** to Word using templates (Norsk Solkraft default, Norsk ENOK, or custom)
4. **Formats** with Grid Table 4 Accent 5 style
5. **Reports** conversion statistics and enhancements

## Key Features
- **ASCII diagram conversion** - Converts ASCII flow diagrams to tables
- **Professional tone** - Removes casual language, plural pronouns
- **Template support** - Norsk Solkraft, Norsk ENOK, or custom templates
- **Norwegian characters** - Proper handling of æ, ø, å
- **Table enhancement** - Improves formatting and alignment

## Example
```
/kc:md2docx rapport.md --template enok
# Converts with ENOV A template, auto-enhances ASCII diagrams
```

## Templates Available
| Flag | Template |
|------|----------|
| `--solkraft` (default) | Norsk Solkraft |
| `--enok` | Norsk ENOK |
| `--template <path>` | Custom template |

## Template Paths (for pandoc --reference-doc)

```
NORSK SOLKRAFT (default):
/mnt/c/Users/klaus/NorskSolkraft AS/Gruppeområde - Documents/05 Maler/Mal norsk solkraft notat.docx

NORSK ENØK:
/mnt/g/My Drive/000 Norsk ENØK/00 Maler/Rapportmal Norsk ENØK.docx
```

## Conversion Command
```bash
# Med Norsk Solkraft-mal (default)
pandoc input.md -o output.docx \
  --reference-doc="/mnt/c/Users/klaus/NorskSolkraft AS/Gruppeområde - Documents/05 Maler/Mal norsk solkraft notat.docx" \
  --from=markdown+pipe_tables+grid_tables --to=docx

# Med Norsk ENØK-mal
pandoc input.md -o output.docx \
  --reference-doc="/mnt/g/My Drive/000 Norsk ENØK/00 Maler/Rapportmal Norsk ENØK.docx" \
  --from=markdown+pipe_tables+grid_tables --to=docx
```

## See Also
- `/md2docx` - Global skill (identical functionality)
