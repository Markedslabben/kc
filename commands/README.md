# KC Commands

Custom commands for Klaus Claude framework.

Commands are typically shell scripts or executables invoked via Claude Code.

## Available Commands

*No commands defined yet*

## Adding New Commands

1. Create command script in `kc/` subdirectory
2. Make executable: `chmod +x command-name.sh`
3. Document usage in this README
4. Optionally add to PATH or create wrapper skill

## Command Organization

```
commands/
└── kc/                  # KC namespace for commands
    ├── parallel.sh     # Example command
    └── ...
```
