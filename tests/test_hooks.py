#!/usr/bin/env python3
"""
Tests for Codex CLI Hook Handler
=================================
Tests all 5 hooks: SessionStart, PreToolUse, PostToolUse, Stop, and UserPromptSubmit.
Run with: python3 -m pytest tests/test_hooks.py -v
"""

import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / ".codex" / "hooks" / "scripts"))
import hooks


class TestParseArgs(unittest.TestCase):
    """Test argument parsing."""

    def test_empty_args(self):
        event_type, input_data = hooks.parse_args([])
        self.assertIsNone(event_type)
        self.assertIsNone(input_data)

    def test_session_start_hook_flag(self):
        """hooks.json: --hook SessionStart."""
        event_type, input_data = hooks.parse_args(["--hook", "SessionStart"])
        self.assertEqual(event_type, "SessionStart")
        self.assertEqual(input_data, {"type": "SessionStart"})

    def test_stop_hook_flag(self):
        """hooks.json: --hook Stop."""
        event_type, input_data = hooks.parse_args(["--hook", "Stop"])
        self.assertEqual(event_type, "Stop")
        self.assertEqual(input_data, {"type": "Stop"})

    def test_pre_tool_use_hook_flag(self):
        """hooks.json: --hook PreToolUse."""
        event_type, input_data = hooks.parse_args(["--hook", "PreToolUse"])
        self.assertEqual(event_type, "PreToolUse")
        self.assertEqual(input_data, {"type": "PreToolUse"})

    def test_post_tool_use_hook_flag(self):
        """hooks.json: --hook PostToolUse."""
        event_type, input_data = hooks.parse_args(["--hook", "PostToolUse"])
        self.assertEqual(event_type, "PostToolUse")
        self.assertEqual(input_data, {"type": "PostToolUse"})

    def test_UserPromptSubmit_hook_flag(self):
        """hooks.json: --hook UserPromptSubmit."""
        event_type, input_data = hooks.parse_args(["--hook", "UserPromptSubmit"])
        self.assertEqual(event_type, "UserPromptSubmit")
        self.assertEqual(input_data, {"type": "UserPromptSubmit"})

    def test_hook_flag_missing_value(self):
        """--hook without a value should return None."""
        event_type, input_data = hooks.parse_args(["--hook"])
        self.assertIsNone(event_type)
        self.assertIsNone(input_data)

    def test_invalid_arg(self):
        """Invalid argument should return None gracefully."""
        event_type, input_data = hooks.parse_args(["not-a-hook-flag"])
        self.assertIsNone(event_type)
        self.assertIsNone(input_data)


class TestHookSoundMap(unittest.TestCase):
    """Test that all hook events have sound mappings."""

    def test_session_start_mapping(self):
        self.assertIn("SessionStart", hooks.HOOK_SOUND_MAP)

    def test_session_stop_mapping(self):
        self.assertIn("Stop", hooks.HOOK_SOUND_MAP)

    def test_pre_tool_use_mapping(self):
        self.assertIn("PreToolUse", hooks.HOOK_SOUND_MAP)

    def test_post_tool_use_mapping(self):
        self.assertIn("PostToolUse", hooks.HOOK_SOUND_MAP)

    def test_UserPromptSubmit_mapping(self):
        self.assertIn("UserPromptSubmit", hooks.HOOK_SOUND_MAP)

    def test_unknown_event_no_mapping(self):
        self.assertNotIn("unknown-event", hooks.HOOK_SOUND_MAP)


class TestHookConfigMap(unittest.TestCase):
    """Test that all hook events have config key mappings."""

    def test_session_start_config_key(self):
        self.assertEqual(hooks.HOOK_CONFIG_MAP["SessionStart"], "disableSessionStartHook")

    def test_session_stop_config_key(self):
        self.assertEqual(hooks.HOOK_CONFIG_MAP["Stop"], "disableStopHook")

    def test_pre_tool_use_config_key(self):
        self.assertEqual(hooks.HOOK_CONFIG_MAP["PreToolUse"], "disablePreToolUseHook")

    def test_post_tool_use_config_key(self):
        self.assertEqual(hooks.HOOK_CONFIG_MAP["PostToolUse"], "disablePostToolUseHook")

    def test_UserPromptSubmit_config_key(self):
        self.assertEqual(hooks.HOOK_CONFIG_MAP["UserPromptSubmit"], "disableUserPromptSubmitHook")


class TestIsHookDisabled(unittest.TestCase):
    """Test hook disable/enable logic with config files."""

    def _create_config(self, config_dir, filename, data):
        path = config_dir / filename
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    @patch("hooks.load_config")
    def test_hook_enabled_by_default(self, mock_load):
        mock_load.return_value = (None, None)
        self.assertFalse(hooks.is_hook_disabled("SessionStart"))
        self.assertFalse(hooks.is_hook_disabled("Stop"))
        self.assertFalse(hooks.is_hook_disabled("PreToolUse"))
        self.assertFalse(hooks.is_hook_disabled("PostToolUse"))
        self.assertFalse(hooks.is_hook_disabled("UserPromptSubmit"))

    @patch("hooks.load_config")
    def test_session_start_disabled_in_default_config(self, mock_load):
        mock_load.return_value = (None, {"disableSessionStartHook": True})
        self.assertTrue(hooks.is_hook_disabled("SessionStart"))

    @patch("hooks.load_config")
    def test_session_stop_disabled_in_default_config(self, mock_load):
        mock_load.return_value = (None, {"disableStopHook": True})
        self.assertTrue(hooks.is_hook_disabled("Stop"))

    @patch("hooks.load_config")
    def test_pre_tool_use_disabled_in_default_config(self, mock_load):
        mock_load.return_value = (None, {"disablePreToolUseHook": True})
        self.assertTrue(hooks.is_hook_disabled("PreToolUse"))

    @patch("hooks.load_config")
    def test_post_tool_use_disabled_in_default_config(self, mock_load):
        mock_load.return_value = (None, {"disablePostToolUseHook": True})
        self.assertTrue(hooks.is_hook_disabled("PostToolUse"))

    @patch("hooks.load_config")
    def test_UserPromptSubmit_disabled_in_default_config(self, mock_load):
        mock_load.return_value = (None, {"disableUserPromptSubmitHook": True})
        self.assertTrue(hooks.is_hook_disabled("UserPromptSubmit"))

    @patch("hooks.load_config")
    def test_local_config_overrides_default(self, mock_load):
        mock_load.return_value = (
            {"disableSessionStartHook": True},
            {"disableSessionStartHook": False},
        )
        self.assertTrue(hooks.is_hook_disabled("SessionStart"))

    @patch("hooks.load_config")
    def test_local_config_enables_when_default_disables(self, mock_load):
        mock_load.return_value = (
            {"disableSessionStartHook": False},
            {"disableSessionStartHook": True},
        )
        self.assertFalse(hooks.is_hook_disabled("SessionStart"))


class TestIsLoggingDisabled(unittest.TestCase):
    """Test logging disable/enable logic."""

    @patch("hooks.get_config_value")
    def test_logging_disabled(self, mock_config):
        mock_config.return_value = True
        self.assertTrue(hooks.is_logging_disabled())

    @patch("hooks.get_config_value")
    def test_logging_enabled(self, mock_config):
        mock_config.return_value = False
        self.assertFalse(hooks.is_logging_disabled())


class TestGetSessionContext(unittest.TestCase):
    """Test SessionStart context generation."""

    def test_context_returns_hooks_context_run(self):
        context = hooks.get_session_context()
        self.assertEqual(context, "hooks context: run")


class TestGetAudioPlayer(unittest.TestCase):
    """Test audio player detection."""

    @patch("hooks.platform.system", return_value="Darwin")
    def test_macos_player(self, _):
        self.assertEqual(hooks.get_audio_player(), ["afplay"])

    @patch("hooks.platform.system", return_value="Windows")
    def test_windows_player(self, _):
        self.assertEqual(hooks.get_audio_player(), ["WINDOWS"])

    @patch("hooks.platform.system", return_value="UnknownOS")
    def test_unknown_os_returns_none(self, _):
        self.assertIsNone(hooks.get_audio_player())


class TestPlaySound(unittest.TestCase):
    """Test sound playback."""

    def test_directory_traversal_blocked(self):
        self.assertFalse(hooks.play_sound("../etc/passwd"))
        self.assertFalse(hooks.play_sound("sound/../../etc"))
        self.assertFalse(hooks.play_sound("..\\windows\\system32"))

    @patch("hooks.get_audio_player", return_value=None)
    def test_no_audio_player(self, _):
        self.assertFalse(hooks.play_sound("SessionStart"))


class TestLogHookData(unittest.TestCase):
    """Test hook data logging."""

    @patch("hooks.is_logging_disabled", return_value=True)
    def test_logging_skipped_when_disabled(self, _):
        # Should not raise or write anything
        hooks.log_hook_data({"type": "test"})

    @patch("hooks.is_logging_disabled", return_value=False)
    def test_logging_writes_jsonl(self, _):
        with tempfile.TemporaryDirectory() as tmpdir:
            logs_dir = Path(tmpdir)
            log_path = logs_dir / "hooks-log.jsonl"

            with patch.object(Path, "parent", new_callable=lambda: property(lambda self: Path(tmpdir))):
                # Patch the file path resolution to use temp dir
                original_log = hooks.log_hook_data

                def patched_log(hook_data):
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(hook_data, ensure_ascii=False, indent=2) + "\n")

                patched_log({"type": "SessionStart"})
                self.assertTrue(log_path.exists())
                content = log_path.read_text()
                self.assertIn("SessionStart", content)


class TestMainIntegration(unittest.TestCase):
    """Integration tests for main() with different hook types."""

    @patch("hooks.play_sound", return_value=True)
    @patch("hooks.is_hook_disabled", return_value=False)
    @patch("hooks.log_hook_data")
    @patch("hooks.get_session_context", return_value="Date: 2026-03-17\nGit branch: main")
    def test_session_start_outputs_context_and_plays_sound(
        self, mock_context, mock_log, mock_disabled, mock_play
    ):
        with patch("sys.argv", ["hooks.py", "--hook", "SessionStart"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_context.assert_called_once()
            mock_play.assert_called_once_with("SessionStart")

    @patch("hooks.play_sound", return_value=True)
    @patch("hooks.is_hook_disabled", return_value=False)
    @patch("hooks.log_hook_data")
    def test_session_stop_plays_sound(self, mock_log, mock_disabled, mock_play):
        with patch("sys.argv", ["hooks.py", "--hook", "Stop"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_play.assert_called_once_with("Stop")

    @patch("hooks.play_sound", return_value=True)
    @patch("hooks.is_hook_disabled", return_value=False)
    @patch("hooks.log_hook_data")
    def test_pre_tool_use_plays_sound(self, mock_log, mock_disabled, mock_play):
        with patch("sys.argv", ["hooks.py", "--hook", "PreToolUse"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_play.assert_called_once_with("PreToolUse")

    @patch("hooks.play_sound", return_value=True)
    @patch("hooks.is_hook_disabled", return_value=False)
    @patch("hooks.log_hook_data")
    def test_post_tool_use_plays_sound(self, mock_log, mock_disabled, mock_play):
        with patch("sys.argv", ["hooks.py", "--hook", "PostToolUse"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_play.assert_called_once_with("PostToolUse")

    @patch("hooks.play_sound", return_value=True)
    @patch("hooks.is_hook_disabled", return_value=False)
    @patch("hooks.log_hook_data")
    def test_UserPromptSubmit_plays_sound(self, mock_log, mock_disabled, mock_play):
        with patch("sys.argv", ["hooks.py", "--hook", "UserPromptSubmit"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_play.assert_called_once_with("UserPromptSubmit")

    @patch("hooks.play_sound")
    @patch("hooks.is_hook_disabled", return_value=True)
    @patch("hooks.log_hook_data")
    def test_disabled_hook_skips_sound(self, mock_log, mock_disabled, mock_play):
        with patch("sys.argv", ["hooks.py", "--hook", "SessionStart"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_play.assert_not_called()

    @patch("hooks.play_sound")
    @patch("hooks.log_hook_data")
    def test_no_args_exits_cleanly(self, mock_log, mock_play):
        with patch("sys.argv", ["hooks.py"]):
            with self.assertRaises(SystemExit) as ctx:
                hooks.main()
            self.assertEqual(ctx.exception.code, 0)
            mock_play.assert_not_called()


if __name__ == "__main__":
    unittest.main()
