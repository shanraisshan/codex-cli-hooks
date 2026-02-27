#!/usr/bin/env python3
"""
Codex CLI Hook Handler
=============================================
This script handles the notify event from Codex CLI and plays a notification sound.
Codex CLI supports 1 hook: notify (event: agent-turn-complete)

Input: JSON payload passed as CLI argument (sys.argv[1])
"""

import sys
import json
import subprocess
import platform
from pathlib import Path

# Windows-only module for playing WAV files
try:
    import winsound
except ImportError:
    winsound = None

# ===== HOOK EVENT TO SOUND MAPPING =====
HOOK_SOUND_MAP = {
    "agent-turn-complete": "codex-notification"
}


def get_audio_player():
    """
    Detect the appropriate audio player for the current platform.

    Returns:
        List of command and args to use for playing audio, or None if no player found
    """
    system = platform.system()

    if system == "Darwin":
        # macOS: use afplay (built-in)
        return ["afplay"]
    elif system == "Linux":
        # Linux: try different players in order of preference
        players = [
            ["paplay"],           # PulseAudio (most common on modern Linux)
            ["aplay"],            # ALSA (fallback)
            ["ffplay", "-nodisp", "-autoexit"],  # FFmpeg (if installed)
            ["mpg123", "-q"],     # mpg123 (if installed)
        ]

        for player in players:
            try:
                subprocess.run(
                    ["which", player[0]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                return player
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        return None
    elif system == "Windows":
        # Windows: Use winsound for WAV files (built-in, reliable)
        return ["WINDOWS"]
    else:
        return None


def play_sound(sound_name):
    """
    Play a sound file for the given sound name.

    Args:
        sound_name: Name of the sound file (e.g., "codex-notification")
                   The file should be at .codex/hooks/sounds/{folder}/{sound_name}.{mp3|wav}

    Returns:
        True if sound played successfully, False otherwise
    """
    # Security check: Prevent directory traversal attacks
    if "/" in sound_name or "\\" in sound_name or ".." in sound_name:
        print(f"Invalid sound name: {sound_name}", file=sys.stderr)
        return False

    audio_player = get_audio_player()
    if not audio_player:
        return False

    # Build path: scripts/ -> hooks/ -> sounds/{folder}/
    script_dir = Path(__file__).parent  # .codex/hooks/scripts/
    hooks_dir = script_dir.parent       # .codex/hooks/

    # Determine the folder based on the sound name prefix
    folder_name = sound_name.split('-')[0]
    # For "codex-notification", folder is "notification" (skip the "codex" prefix)
    if folder_name == "codex":
        parts = sound_name.split('-')
        folder_name = parts[1] if len(parts) > 1 else folder_name
    sounds_dir = hooks_dir / "sounds" / folder_name

    is_windows = audio_player[0] == "WINDOWS"
    extensions = ['.wav'] if is_windows else ['.wav', '.mp3']

    for extension in extensions:
        file_path = sounds_dir / f"{sound_name}{extension}"

        if file_path.exists():
            try:
                if is_windows:
                    if winsound:
                        winsound.PlaySound(str(file_path),
                                         winsound.SND_FILENAME | winsound.SND_NODEFAULT)
                        return True
                    else:
                        return False
                else:
                    subprocess.Popen(
                        audio_player + [str(file_path)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                    return True
            except (FileNotFoundError, OSError) as e:
                print(f"Error playing sound {file_path.name}: {e}", file=sys.stderr)
                return False
            except Exception as e:
                print(f"Error playing sound {file_path.name}: {e}", file=sys.stderr)
                return False

    return False


def is_hook_disabled(event_name):
    """
    Check if the notify hook is disabled in the config files.
    Uses fallback logic: hooks-config.local.json -> hooks-config.json

    Args:
        event_name: The event name (e.g., "agent-turn-complete")

    Returns:
        True if the hook is disabled, False otherwise
    """
    try:
        script_dir = Path(__file__).parent
        hooks_dir = script_dir.parent
        config_dir = hooks_dir / "config"

        local_config_path = config_dir / "hooks-config.local.json"
        default_config_path = config_dir / "hooks-config.json"

        config_key = "disableNotifyHook"

        local_config = None
        if local_config_path.exists():
            try:
                with open(local_config_path, "r", encoding="utf-8") as f:
                    local_config = json.load(f)
            except Exception:
                pass

        default_config = None
        if default_config_path.exists():
            try:
                with open(default_config_path, "r", encoding="utf-8") as f:
                    default_config = json.load(f)
            except Exception:
                pass

        if local_config is not None and config_key in local_config:
            return local_config[config_key]
        elif default_config is not None and config_key in default_config:
            return default_config[config_key]
        else:
            return False

    except Exception:
        return False


def is_logging_disabled():
    """
    Check if logging is disabled in the config files.
    Uses fallback logic: hooks-config.local.json -> hooks-config.json

    Returns:
        True if logging is disabled, False otherwise
    """
    try:
        script_dir = Path(__file__).parent
        hooks_dir = script_dir.parent
        config_dir = hooks_dir / "config"

        local_config_path = config_dir / "hooks-config.local.json"
        default_config_path = config_dir / "hooks-config.json"

        local_config = None
        if local_config_path.exists():
            try:
                with open(local_config_path, "r", encoding="utf-8") as f:
                    local_config = json.load(f)
            except Exception:
                pass

        default_config = None
        if default_config_path.exists():
            try:
                with open(default_config_path, "r", encoding="utf-8") as f:
                    default_config = json.load(f)
            except Exception:
                pass

        if local_config is not None and "disableLogging" in local_config:
            return local_config["disableLogging"]
        elif default_config is not None and "disableLogging" in default_config:
            return default_config["disableLogging"]
        else:
            return False

    except Exception:
        return False


def log_hook_data(hook_data):
    """
    Log the hook_data to hooks-log.jsonl for debugging/auditing.
    Log file is stored at .codex/hooks/logs/hooks-log.jsonl
    """
    if is_logging_disabled():
        return

    try:
        script_dir = Path(__file__).parent
        hooks_dir = script_dir.parent
        logs_dir = hooks_dir / "logs"

        logs_dir.mkdir(parents=True, exist_ok=True)

        log_path = logs_dir / "hooks-log.jsonl"
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(hook_data, ensure_ascii=False, indent=2) + "\n")
    except Exception as e:
        print(f"Failed to log hook_data: {e}", file=sys.stderr)


def main():
    """
    Main program - runs when Codex CLI triggers the notify hook.

    How it works:
    1. Codex CLI sends event data as JSON via CLI argument (sys.argv[1])
    2. We check if the notify hook is disabled in hooks-config.json
    3. We parse the JSON to get the event type
    4. We play the corresponding notification sound
    5. We exit successfully
    """
    try:
        # Read event data from CLI argument (Codex passes JSON as argv[1])
        if len(sys.argv) < 2:
            sys.exit(0)

        input_data = json.loads(sys.argv[1])

        # Log hook data
        log_hook_data(input_data)

        # Check if the notify hook is disabled
        event_type = input_data.get("type", "")
        if is_hook_disabled(event_type):
            sys.exit(0)

        # Determine which sound to play
        sound_name = HOOK_SOUND_MAP.get(event_type)

        # Play the sound
        if sound_name:
            play_sound(sound_name)

        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
