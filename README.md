# Codex CLI Hooks
[![Hooks](https://img.shields.io/badge/supports-5%20hooks-white?style=flat&labelColor=555)](.codex/hooks/HOOKS-README.md) [![Version](https://img.shields.io/badge/updated%20with%20Codex%20CLI-v0.118.0%20(Apr%204%2C%202026%2012%3A01%20AM%20PKT)-white?style=flat&labelColor=555)](https://github.com/openai/codex/releases) [![Stars](https://img.shields.io/github/stars/shanraisshan/codex-cli-hooks?style=flat&label=%E2%98%85&labelColor=555&color=white)](https://github.com/shanraisshan/codex-cli-hooks/stargazers) <img src="!/beta.svg" alt="Beta" height="20">

<p align="center">
  <img src="!/codex-speaking.svg" alt="Codex CLI mascot speaking" width="176" height="158">
</p>

<p align="center">
  <img src="!/repo-description.svg" alt="Human sounds on session start, stop, and agent turn complete, context injection" height="56">
</p>

## Installation

<p>
  <a href="install/README-mac.md"><img src="!/pill-mac.svg" alt="Mac" height="36"></a>&nbsp;
  <a href="install/README-linux.md"><img src="!/pill-linux.svg" alt="Linux" height="36"></a>&nbsp;
  <a href="install/README-windows.md"><img src="!/pill-windows.svg" alt="Windows" height="36"></a>
</p>

![How to Use](!/how-to-use.svg)

**Step 1.** Start Codex CLI with the hooks engine <img src="!/beta.svg" alt="Beta" height="16"> enabled:
```bash
codex -c features.codex_hooks=true
```

**Step 2.** Send a prompt (e.g., `Hi`) — you'll hear a sound on session start, tool use, prompt submit, and session stop.

## Changelog
new hook addition changelogs only

| Date | Hooks | Changes | Codex CLI Version | Demo |
|------|:-----:|---------|:-----------------:|:----:|
| Mar 26, 2026 | 5 | Added `PreToolUse` and `PostToolUse` | [v0.117.0](https://github.com/openai/codex/releases) | |
| Mar 20, 2026 | 3 | Added `UserPromptSubmit` | [v0.116.0](https://github.com/openai/codex/releases) | |
| Mar 11, 2026 | 2 | Added `SessionStart` and `Stop` | [v0.115.0](https://github.com/openai/codex/releases) | |

## Links

<p>
  <a href="#"><img src="!/pill-youtube.svg" alt="YouTube" height="36"></a>&nbsp;
  <a href="#"><img src="!/pill-linkedin.svg" alt="LinkedIn" height="36"></a>&nbsp;
  <a href="https://www.reddit.com/r/codex/comments/1rw6j0o/codex_cli_now_has_hooks_support_beta_sessionstart/"><img src="!/pill-reddit.svg" alt="Reddit" height="36"></a>&nbsp;
  <a href="https://x.com/shanraisshan/status/2033899318264856925"><img src="!/pill-x.svg" alt="X" height="36"></a>&nbsp;
</p>

## Other Repos

<a href="https://github.com/shanraisshan/claude-code-hooks"><img src="!/claude-speaking.svg" alt="Claude Code Hooks" width="40" height="40" align="center"></a> <a href="https://github.com/shanraisshan/claude-code-hooks"><strong>claude-code-hooks</strong></a> · <a href="https://github.com/shanraisshan/codex-cli-best-practice"><img src="!/codex-jumping.svg" alt="Codex CLI Best Practice" width="40" height="40" align="center"></a> <a href="https://github.com/shanraisshan/codex-cli-best-practice"><strong>codex-cli-best-practice</strong></a> · <a href="https://github.com/shanraisshan/claude-code-best-practice"><img src="!/claude-jumping.svg" alt="Claude Code Best Practice" width="40" height="40" align="center"></a> <a href="https://github.com/shanraisshan/claude-code-best-practice"><strong>claude-code-best-practice</strong></a>

<p align="center">
  <img src="!/codex-jumping.svg" alt="section divider" width="60" height="50">
</p>

## <img src="!/tags/sponsor-heart.svg" width="22" height="22" align="center"> Sponsor My Work

If you like my work, buy me a doodh patti 🍵 on

<a href="https://buy.polar.sh/polar_cl_fTn59g14xsMqJdXnPYtPmHVTdm6qnrNMnhXuB2JZJDL"><img src="!/tags/polar.svg" alt="Polar" width="40" height="40" align="center"></a> <a href="https://buy.polar.sh/polar_cl_fTn59g14xsMqJdXnPYtPmHVTdm6qnrNMnhXuB2JZJDL"><strong>Polar</strong></a>
