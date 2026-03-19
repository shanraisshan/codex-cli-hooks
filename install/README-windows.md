# Installation - Windows

[< Back to Main README](../README.md)

## Prerequisites

- **Python 3**: Required for running the hook script
  - Verify: `python --version`
  - Install: Download from [python.org](https://www.python.org/downloads/) or install via `winget install Python.Python.3`
- **Audio Player**: Built-in `winsound` module (included with Python)

All details are mentioned in [HOOKS-README.md](../.codex/hooks/HOOKS-README.md)

---

## Installation

### Step 1: Copy hooks folder

Open terminal in your project directory and run the following commands:

**PowerShell:**
```powershell
New-Item -ItemType Directory -Force -Path .codex\hooks
git clone https://github.com/shanraisshan/codex-cli-hooks.git temp-hooks
Copy-Item -Recurse -Force temp-hooks\.codex\hooks\* .codex\hooks\
Copy-Item temp-hooks\install\hooks-windows.json .codex\hooks.json
Remove-Item -Recurse -Force temp-hooks
```

**Command Prompt:**
```cmd
if not exist .codex\hooks mkdir .codex\hooks
git clone https://github.com/shanraisshan/codex-cli-hooks.git temp-hooks
xcopy /E /I /Y temp-hooks\.codex\hooks\* .codex\hooks\
copy temp-hooks\install\hooks-windows.json .codex\hooks.json
rmdir /S /Q temp-hooks
```

### Step 2: Copy config.toml into your project

1. If you don't have a `.codex/config.toml` file in your project, create one: `New-Item -Force .codex/config.toml`
2. Open [`install/config-windows.toml`](config-windows.toml) and copy the `notify` line into your `.codex/config.toml`

> **Why separate config files per platform?**
> - Python command: `python3` (macOS/Linux) vs `python` (Windows)
