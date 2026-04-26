# CLAUDE.md / AGENTS.md

This file provides guidance to AI coding assistants — **Claude Code** (claude.ai/code) reads it as `CLAUDE.md` and **Codex CLI** reads it as `AGENTS.md` (symlinked) — when working with code in this repository.

## What this repo is

A drop-in hooks pack for **OpenAI's Codex CLI**. A single Python handler (`.codex/hooks/scripts/hooks.py`) plays an ElevenLabs "Adam" voice clip on each Codex hook event and injects context at session start. Codex CLI discovers it via `.codex/hooks.json`. The repo is also distributed as installer bundles for Mac/Linux/Windows under `install/`.

This is **not** Claude Code hooks — `.claude/` exists only because the maintainer also runs Claude Code locally. Do not confuse the two systems: Codex CLI and Claude Code each have their own hook event names and config formats.

## Common commands

```bash
# Run the test suite (uses unittest, not pytest despite the docstring)
python3 -m unittest tests.test_hooks -v

# Run a single test
python3 -m unittest tests.test_hooks.TestParseArgs.test_session_start_hook_flag -v

# Manually invoke a hook (what Codex does internally)
python3 .codex/hooks/scripts/hooks.py --hook SessionStart
echo '{"type":"PreToolUse","tool_name":"Bash"}' | python3 .codex/hooks/scripts/hooks.py --hook PreToolUse

# Start Codex CLI (hooks load automatically as of v0.123.0)
codex
```

There is no build step, lint config, or package manager — the project is plain Python 3 plus JSON/SVG assets.

## Architecture

**One handler, many events.** Every hook in `.codex/hooks.json` invokes the same `hooks.py` script with `--hook <EventName>`. The script reads optional JSON from stdin, looks up the event in two dicts at the top of the file, and acts on it:

- `HOOK_SOUND_MAP` — event name → sound folder name (e.g. `PermissionRequest` → `sounds/PermissionRequest/PermissionRequest.{mp3,wav}`)
- `HOOK_CONFIG_MAP` — event name → disable-toggle key in `hooks-config.json`

To add a new hook, you must update **all** of these in lockstep, or it will silently no-op:
1. `HOOK_SOUND_MAP` and `HOOK_CONFIG_MAP` in `.codex/hooks/scripts/hooks.py`
2. The disable-toggle key in `.codex/hooks/config/hooks-config.json`
3. The hook entry in `.codex/hooks.json` **and** all three `install/hooks-{mac,linux,windows}.json` (they are intentional duplicates — `.codex/hooks.json` is the live config, `install/*` are templates the user copies during install). Windows uses `python` (not `python3`); Mac/Linux use `python3`.
4. Sound files at `.codex/hooks/sounds/<EventName>/<EventName>.{mp3,wav}` — folder and filename must match the event name **exactly** (CamelCase). Generate both formats: macOS/Linux play `.mp3` via `afplay`/`paplay`; Windows plays `.wav` via `winsound`.

**Currently supported events** (Codex CLI 0.122.0+): `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Stop`. The full Codex hook surface is only these six — much narrower than Claude Code's. When the user asks "are there more hooks", check the official Codex changelog at developers.openai.com/codex/changelog before claiming a hook exists.

**Special-case event:** `SessionStart` writes context (date, git branch, cwd) to **stdout**, which Codex injects into the model's context window. Other events only play sound and exit. Don't add stdout output to other events unless you intend it to land in the prompt.

**Config layering:** `hooks-config.local.json` (gitignored) overrides `hooks-config.json` (committed) per-key. Use `get_config_value()` — it implements the fallback. Don't read either file directly.

**Logging:** When `disableLogging` is `false`, every invocation appends a JSONL entry to `.codex/hooks/logs/hooks-log.jsonl`. The log writer only persists three keys (`hook`, `timestamp`, `last_assistant_message`); raw payload is discarded.

## Voice / sound assets

All sounds are generated on **elevenlabs.io** with the **Adam — American, Dark and Tough** voice. When adding a new hook, generate both `.mp3` and `.wav` for cross-platform support. Existing sounds for the six hooks live under `.codex/hooks/sounds/<EventName>/`.

## README image assets

The directory literally named `!/` (yes, with the exclamation mark) holds all SVG/PNG assets referenced from `README.md`. The `!` prefix is intentional — it sorts to the top of file listings. Pill-style tag SVGs (e.g. `!/hooks-tags.svg`, `!/pill-mac.svg`) follow a consistent design language: rounded rect background, single-line sans-serif text, fixed height. Match that style when adding new tags.

## Git commit rule — one commit per file

**Always create a separate commit for each changed file.** Do NOT bundle multiple files into one commit. If 5 files changed, create 5 commits.

Example — if `README.md`, `.codex/hooks.json`, and `tests/test_hooks.py` all changed:
1. `git add README.md` → commit with a README-specific message
2. `git add .codex/hooks.json` → commit with a hooks.json-specific message
3. `git add tests/test_hooks.py` → commit with a test-specific message

Each commit message should describe **only** that file's change. This keeps history reviewable, revertable, and cherry-pickable.

The only exception is when the user explicitly says "single commit", "one commit", "all in one", or similar. Otherwise, one-commit-per-file is the default — even if the user just says "commit all".

## Other repo conventions

- The README, `HOOKS-README.md`, and `tests/test_hooks.py` docstrings all hardcode the hook count. When you add or remove a hook, update all of them in lockstep — code is source of truth.
- The hooks engine is **stable** as of Codex CLI v0.123.0 — no feature flag required. (Older versions needed `-c features.codex_hooks=true`; if you see that flag in old docs or scripts, it can be dropped.)
- The repo intentionally has no CI, no lockfile, no formatter config. Don't add them speculatively.
