# Installation - macOS

[< Back to Main README](../README.md)

## Prerequisites

- **Python 3**: Required for running the hook script
  - Verify: `python3 --version`
  - Install: `brew install python3` (requires [Homebrew](https://brew.sh/))
- **Audio Player**: `afplay` (built-in, no installation needed)

All details are mentioned in [HOOKS-README.md](../.codex/hooks/HOOKS-README.md)

---

## Installation

### Step 1: Copy hooks folder

```bash
cd your-project
mkdir -p .codex/hooks
git clone https://github.com/shanraisshan/codex-cli-voice-hooks.git temp-hooks
cp -r temp-hooks/.codex/hooks/* .codex/hooks/
rm -rf temp-hooks
```

### Step 2: Copy config.toml into your project

1. If you don't have a `.codex/config.toml` file in your project, create one
2. Open [`install/config-mac.toml`](config-mac.toml) and copy the `notify` line into your `.codex/config.toml`

> **Why separate config files per platform?**
> - Python command: `python3` (macOS/Linux) vs `python` (Windows)
