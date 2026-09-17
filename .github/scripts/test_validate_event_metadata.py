"""Regression tests for speaker-root layout validation."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from validate_event_metadata import validate_speaker_session_layout


class SpeakerSessionLayoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = Path(tempfile.mkdtemp())
        self.speaker_dir = (
            self._tmpdir / "events" / "2026" / "2026-01-01-sample" / "speakers" / "alice"
        )
        self.speaker_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def test_allowlisted_root_files_pass(self) -> None:
        for name in ("speaker.md", "card.jpg", "card.webp", "readme.md", ".gitkeep"):
            (self.speaker_dir / name).write_text("x", encoding="utf-8")
        (self.speaker_dir / "assets").mkdir()
        (self.speaker_dir / "assets" / "deck.pdf").write_bytes(b"%PDF")

        errors = validate_speaker_session_layout(self._tmpdir / "events")
        self.assertEqual(errors, [])

    def test_notes_md_at_root_is_rejected(self) -> None:
        (self.speaker_dir / "speaker.md").write_text("---\nname: A\n---\n", encoding="utf-8")
        (self.speaker_dir / "notes.md").write_text("notes", encoding="utf-8")

        errors = validate_speaker_session_layout(self._tmpdir / "events")
        self.assertTrue(any("notes.md" in error for error in errors), errors)
        self.assertTrue(any("readme.md" in error and ".gitkeep" in error for error in errors), errors)

    def test_session_binary_at_root_is_rejected(self) -> None:
        (self.speaker_dir / "speaker.md").write_text("---\nname: A\n---\n", encoding="utf-8")
        (self.speaker_dir / "deck.pdf").write_bytes(b"%PDF")

        errors = validate_speaker_session_layout(self._tmpdir / "events")
        self.assertTrue(any("deck.pdf" in error for error in errors), errors)
        self.assertTrue(any("readme.md" in error and ".gitkeep" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
