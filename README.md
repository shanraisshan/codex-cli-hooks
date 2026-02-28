# Codex CLI Voice Hooks
[![Hooks](https://img.shields.io/badge/supports-1%20hook-white?style=flat&labelColor=555)](.codex/hooks/HOOKS-README.md) [![Version](https://img.shields.io/badge/updated%20with%20Codex%20CLI-v0.106.0%20(Feb%2028%2C%202026%2011%3A32%20AM%20PKT)-white?style=flat&labelColor=555)](https://github.com/openai/codex/releases)

<p align="center">
  <img src="!/codex-speaking.svg" alt="Codex CLI mascot speaking" width="176" height="158">
</p>

<p align="center">
  <img src="!/ding.svg" alt="Notification on agent turn complete" height="48">
</p>

<p align="center">
  <img src="!/tagline.svg" alt="Voice notification for agent-turn-complete events" height="40">
</p>

## Installation

<p>
  <a href="install/README-mac.md"><img src="!/pill-mac.svg" alt="Mac" height="36"></a>&nbsp;
  <a href="install/README-linux.md"><img src="!/pill-linux.svg" alt="Linux" height="36"></a>&nbsp;
  <a href="install/README-windows.md"><img src="!/pill-windows.svg" alt="Windows" height="36"></a>
</p>

## How It Works

[Codex CLI](https://github.com/openai/codex) supports a `notify` hook that fires when the agent completes a turn. This project plays a notification sound when that happens, so you know when Codex is done — without watching the terminal.

1. Codex CLI fires the `notify` hook with a JSON payload: `{"type": "agent-turn-complete"}`
2. The hook script (Python) receives the payload as a CLI argument
3. The script detects your OS and plays the notification sound using the native audio player

### Hook

| # | Hook | Event | Sound |
|:-:|------|-------|-------|
| 1 | `notify` | `agent-turn-complete` | `codex-notification.mp3` |

See [HOOKS-README.md](.codex/hooks/HOOKS-README.md) for full documentation on configuration, logging, and audio player details.

## Links

<p>
  <a href="#"><img src="!/pill-youtube.svg" alt="YouTube" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-linkedin.svg" alt="LinkedIn" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-reddit.svg" alt="Reddit" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-x.svg" alt="X" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-medium.svg" alt="Medium" height="36"></a>
</p>

## Other CLI Voice Hooks

- [Claude Code Voice Hooks](https://github.com/shanraisshan/claude-code-voice-hooks)
- [Codex CLI Voice Hooks](https://github.com/shanraisshan/codex-cli-voice-hooks)
