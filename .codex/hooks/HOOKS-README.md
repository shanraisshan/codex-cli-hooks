# HOOKS-README
Contains all the details, scripts, and instructions for the Codex CLI notify hook.

## Hook Events Overview

Codex CLI provides **1 hook** that runs when the agent completes a turn:

| # | Hook | Event Type | Description |
|:-:|------|------------|-------------|
| 1 | `notify` | `agent-turn-complete` | Runs when the Codex agent finishes responding |

### JSON Payload Structure

Codex CLI passes a JSON payload as a **CLI argument** (`sys.argv[1]`) to the hook script:

```json
{
  "type": "agent-turn-complete"
}
```

> **Key difference from Claude Code:** Claude Code passes JSON via **stdin**, while Codex CLI passes it as a **CLI argument**.

## Prerequisites

Before using hooks, ensure you have **Python 3** installed on your system.

### Required Software

#### All Platforms (Windows, macOS, Linux)
- **Python 3**: Required for running the hook script
- Verify installation: `python3 --version`

**Installation Instructions:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/) or install via `winget install Python.Python.3`
- **macOS**: Install via `brew install python3` (requires [Homebrew](https://brew.sh/))
- **Linux**: Install via `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (RHEL/CentOS)

### Audio Players (Automatically Detected)

The hook script automatically detects and uses the appropriate audio player for your platform:

- **macOS**: Uses `afplay` (built-in, no installation needed)
- **Linux**: Uses `paplay` from `pulseaudio-utils` - install via `sudo apt install pulseaudio-utils`
- **Windows**: Uses built-in `winsound` module (included with Python)

### How the Hook Is Executed

The hook is configured in `.codex/config.toml`:

```toml
notify = ["python3", ".codex/hooks/scripts/hooks.py"]
```

When the agent completes a turn, Codex CLI runs:
```
python3 .codex/hooks/scripts/hooks.py '{"type":"agent-turn-complete"}'
```

## Configuring the Hook (Enable/Disable)

### Disable the Notify Hook

Edit `.codex/hooks/config/hooks-config.json`:
```json
{
  "disableNotifyHook": true,
  "disableLogging": true
}
```

### Configuration Files

There are two configuration files:

1. **`.codex/hooks/config/hooks-config.json`** - The shared/default configuration that is committed to git
2. **`.codex/hooks/config/hooks-config.local.json`** - Your personal overrides (git-ignored)

The local config file (`.local.json`) takes precedence over the shared config, allowing each developer to customize their hook behavior without affecting the team.

#### Shared Configuration

Edit `.codex/hooks/config/hooks-config.json` for team-wide defaults:

```json
{
  "disableNotifyHook": false,
  "disableLogging": true
}
```

**Configuration Options:**
- `disableNotifyHook`: Set to `true` to disable the notification sound
- `disableLogging`: Set to `true` to disable logging hook events to `.codex/hooks/logs/hooks-log.jsonl`

#### Local Configuration (Personal Overrides)

Create or edit `.codex/hooks/config/hooks-config.local.json` for personal preferences:

```json
{
  "disableNotifyHook": true,
  "disableLogging": true
}
```

In this example, both the notification sound and logging are disabled locally. The shared configuration values are used for any keys not present in the local config.

### Logging

When logging is enabled (`"disableLogging": false`), hook events are logged to `.codex/hooks/logs/hooks-log.jsonl` in JSON Lines format. Each entry contains the full JSON payload received from Codex CLI.

## Future Extensibility

Codex CLI currently supports only the `notify` hook with the `agent-turn-complete` event. If OpenAI adds more hooks in the future, this project can be extended by:

1. Adding new entries to `HOOK_SOUND_MAP` in `hooks.py`
2. Adding corresponding sound files in `.codex/hooks/sounds/`
3. Adding toggle keys in `hooks-config.json`
