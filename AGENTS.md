# AGENTS.md

This file provides guidance to Codex CLI when working with code in this repository.

## What this repo is

A drop-in hooks pack for **Codex CLI**. A single Python handler (`.codex/hooks/scripts/hooks.py`) plays an ElevenLabs "Adam" voice clip on each Codex hook event and injects context at session start. Codex CLI discovers it via `.codex/hooks.json`. Distributed as installer bundles for Mac/Linux/Windows under `install/`.

The hooks engine is **stable** as of Codex CLI v0.123.0. Enable it with `codex -c features.codex_hooks=true`.

## Supported hooks (6 total)

`SessionStart` · `UserPromptSubmit` · `PreToolUse` · `PermissionRequest` · `PostToolUse` · `Stop`

To add a new hook, update **all** of the following in lockstep — missing any one causes a silent no-op:
1. `HOOK_SOUND_MAP` and `HOOK_CONFIG_MAP` in `.codex/hooks/scripts/hooks.py`
2. The disable-toggle key in `.codex/hooks/config/hooks-config.json`
3. The hook entry in `.codex/hooks.json` and all three `install/hooks-{mac,linux,windows}.json` (Windows uses `python`, Mac/Linux use `python3`)
4. Sound files at `.codex/hooks/sounds/<EventName>/<EventName>.{mp3,wav}` — both formats required (macOS/Linux play `.mp3`, Windows plays `.wav` via `winsound`); generate via [elevenlabs.io](https://elevenlabs.io/) using the **Adam — American, Dark and Tough** voice
5. Update hook-count references in `README.md` (badge + changelog), `.codex/hooks/HOOKS-README.md`, and the docstring in `tests/test_hooks.py`

## Common commands

```bash
# Run the test suite (uses unittest, not pytest)
python3 -m unittest tests.test_hooks -v

# Manually invoke a hook
python3 .codex/hooks/scripts/hooks.py --hook SessionStart

# Start Codex CLI with hooks enabled
codex -c features.codex_hooks=true
```

## Git Commit Rules

When committing changes, **create separate commits per file**. Do NOT bundle multiple file changes into a single commit. If 5 files changed, create 5 commits.

For example, if `README.md`, `install/settings.json`, and a test file all changed:
- Commit 1: `git add README.md` → commit with README-specific message
- Commit 2: `git add install/settings.json` → commit with settings-specific message
- Commit 3: `git add tests/test_hooks.py` → commit with test-specific message

The only exception is when the user explicitly says "single commit", "one commit", or "all in one". Otherwise, one-commit-per-file is the default — even if the user just says "commit all".

This makes the git history cleaner and easier to review, revert, or cherry-pick individual changes.
