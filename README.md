# Codex CLI Voice Hooks
[![Hooks](https://img.shields.io/badge/supports-3%20hooks-white?style=flat&labelColor=555)](.codex/hooks/HOOKS-README.md) [![Version](https://img.shields.io/badge/updated%20with%20Codex%20CLI-v0.115.0%20(Mar%2017%2C%202026%205%3A00%20PM%20PKT)-white?style=flat&labelColor=555)](https://github.com/openai/codex/releases) <img src="!/beta.svg" alt="Beta" height="20">

<p align="center">
  <img src="!/codex-speaking.svg" alt="Codex CLI mascot speaking" width="176" height="158">
</p>

<p align="center">
  <img src="!/repo-description.svg" alt="Notification on agent-turn-complete, sound on SessionStart and Stop, context injection" height="56">
</p>

## Installation

<p>
  <a href="install/README-mac.md"><img src="!/pill-mac.svg" alt="Mac" height="36"></a>&nbsp;
  <a href="install/README-linux.md"><img src="!/pill-linux.svg" alt="Linux" height="36"></a>&nbsp;
  <a href="install/README-windows.md"><img src="!/pill-windows.svg" alt="Windows" height="36"></a>
</p>

## How It Works

[Codex CLI](https://github.com/openai/codex) fires hooks at key points in the agent lifecycle. This project plays notification sounds and injects session context, so you stay informed without watching the terminal.

### Hooks

| # | Hook | Event | What It Does |
|:-:|------|-------|--------------|
| 1 | `notify` | `agent-turn-complete` | Plays notification sound when agent finishes |
| 2 | `SessionStart` | `session-start` | Injects context (date, git branch, status) + plays sound |
| 3 | `Stop` | `session-stop` | Plays notification sound when session ends |

> Hooks 2 and 3 require **Codex CLI v0.114.0+** with the hooks engine enabled.

See [HOOKS-README.md](.codex/hooks/HOOKS-README.md) for full documentation on configuration, logging, and audio player details.

![How to Use](!/how-to-use.svg)

After [installing](#installation) the hooks:

**Step 1.** Start Codex CLI with the hooks engine <img src="!/beta.svg" alt="Beta" height="16"> enabled:
```bash
codex -c features.codex_hooks=true
```

**Step 2.** Send a prompt (e.g., `Hi`) — you'll hear a sound on session start, agent response, and session stop.

## Links

<p>
  <a href="#"><img src="!/pill-youtube.svg" alt="YouTube" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-linkedin.svg" alt="LinkedIn" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-reddit.svg" alt="Reddit" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-x.svg" alt="X" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-medium.svg" alt="Medium" height="36"></a>
</p>

## Other CLI Voice Hooks

<p><a href="https://github.com/shanraisshan/claude-code-voice-hooks"><img src="https://raw.githubusercontent.com/shanraisshan/claude-code-voice-hooks/main/!/claude-speaking.svg" alt="Claude Code mascot" width="50" height="45" align="middle"></a>&nbsp;&nbsp;<a href="https://github.com/shanraisshan/claude-code-voice-hooks"><b><ins>claude-code-voice-hooks</ins></b></a></p>
