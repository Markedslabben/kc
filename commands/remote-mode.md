# /remote-mode - Toggle remote mode for Claude Code sessions

Prevents Windows from going to sleep and enables TTS (text-to-speech) for Claude responses when using Claude Code remotely from mobile.

## Invocation

```bash
/kc:remote-mode          # Show current status
/kc:remote-mode on       # Sleep never, screen off 5 min, TTS on
/kc:remote-mode off      # Restore defaults, TTS off
```

## Workflow

### Step 1: Parse argument

- No argument → Status mode
- `on` → Enable remote mode
- `off` → Disable remote mode

### Step 2: Execute

**Status mode** (no argument):
```bash
powershell.exe -Command "powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE"
ls -la ~/.claude/remote-mode-on 2>/dev/null
```
Parse output: if standby timeout is 0 → remote mode is ON, otherwise OFF.
Check if `~/.claude/remote-mode-on` flag exists → TTS is ON/OFF.
Report to user in plain language.

**ON mode**:
```bash
# Power settings
powershell.exe -Command "powercfg /change standby-timeout-ac 0; powercfg /change standby-timeout-dc 0; powercfg /change monitor-timeout-ac 5; powercfg /change monitor-timeout-dc 5"

# Enable TTS flag
touch ~/.claude/remote-mode-on
```
Confirm: "Remote mode ON — sleep disabled, TTS with Sonia enabled."

**OFF mode**:
```bash
# Power settings
powershell.exe -Command "powercfg /change standby-timeout-ac 30; powercfg /change standby-timeout-dc 15; powercfg /change monitor-timeout-ac 10; powercfg /change monitor-timeout-dc 5"

# Disable TTS flag
rm -f ~/.claude/remote-mode-on
```
Confirm: "Remote mode OFF — standard power settings restored, TTS disabled."

### Step 3: Verify

After ON or OFF, run the status query to confirm the change took effect.
