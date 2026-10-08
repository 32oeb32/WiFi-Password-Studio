"""Offline, reproducible invariants for Wi-Fi Password Studio."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import wifi_password_studio_v2 as studio


class TestPasswordStudio(unittest.TestCase):
    def test_valid_ascii_boundaries(self):
        self.assertFalse(studio.valid_wifi_password("A" * 7))
        self.assertTrue(studio.valid_wifi_password("A" * 8))
        self.assertTrue(studio.valid_wifi_password("A" * 63))
        self.assertFalse(studio.valid_wifi_password("A" * 64))
        self.assertFalse(studio.valid_wifi_password("A" * 7 + "é"))
        self.assertFalse(studio.valid_wifi_password("A" * 7 + "\n"))

    def test_secure_random_generation(self):
        for length in (8, 16, 20, 63):
            for _ in range(12):
                secret = studio.secure_random_password(length)
                self.assertEqual(len(secret), length)
                self.assertTrue(studio.valid_wifi_password(secret))
                self.assertTrue(any(c.islower() for c in secret))
                self.assertTrue(any(c.isupper() for c in secret))
                self.assertTrue(any(c.isdigit() for c in secret))
                self.assertTrue(any(c in studio.SYMBOLS for c in secret))

    def test_secure_random_invalid_length(self):
        for length in (7, 64):
            with self.assertRaises(ValueError):
                studio.secure_random_password(length)

    def test_memorable_passphrase(self):
        for words in (4, 5, 6, 7):
            secret = studio.memorable_password(words)
            self.assertEqual(len(secret.split("-")), words)
            self.assertTrue(studio.valid_wifi_password(secret))

    def test_invalid_memorable_options(self):
        for number in (3, 8):
            with self.assertRaises(ValueError):
                studio.memorable_password(number)
        with self.assertRaises(ValueError):
            studio.memorable_password(4, separator=" ")

    def test_custom_passphrase(self):
        secret = studio.custom_passphrase("lighthouse, maple, sky")
        self.assertTrue(secret.startswith("Lighthouse-Maple-Sky!"))
        self.assertTrue(studio.valid_wifi_password(secret))

    def test_reject_non_ascii_custom_words(self):
        with self.assertRaises(ValueError):
            studio.custom_passphrase("nebulä, maple, sky")

    def test_assessment_reports_weak_patterns(self):
        notes = " ".join(studio.assess_password("password123!"))
        self.assertIn("widely used", notes)

    def test_seed_parsing_deduplicates(self):
        self.assertEqual(studio.parse_seed_words("nebula, nebula, 47"), ["nebula", "47"])
        self.assertNotIn("welcome", studio.parse_seed_words("nebula"))
        self.assertIn("welcome", studio.parse_seed_words("nebula", True))

    def test_seed_parsing_empty(self):
        with self.assertRaises(ValueError):
            studio.parse_seed_words(" , , ")

    def test_patterned_dataset_unique_and_valid(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "samples.txt"
            amount = studio.create_patterned_list(["nebula", "harbor", "47"], 1250, path)
            lines = path.read_text(encoding="ascii").splitlines()
            self.assertEqual(amount, 1250)
            self.assertEqual(len(lines), 1250)
            self.assertEqual(len(set(lines)), 1250)
            self.assertTrue(all(studio.valid_wifi_password(s) for s in lines))
            if sys.platform != "win32":
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_no_output_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "samples.txt"
            path.write_text("keep", encoding="ascii")
            with self.assertRaises(FileExistsError):
                studio.create_patterned_list(["demo"], 5, path)
            self.assertEqual(path.read_text(encoding="ascii"), "keep")

    def test_bounds_on_dataset_size(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "samples.txt"
            for amount in (0, 1_000_001):
                with self.assertRaises(ValueError):
                    studio.create_patterned_list(["nebula"], amount, target)
            self.assertFalse(target.exists())

    def test_banner_and_footer_text(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            studio.show_banner()
            studio.show_developer_footer()
        text = out.getvalue()
        self.assertIn("SPES_MEA_IN_DEO_EST#32", text)
        self.assertIn("#DEV32#", text)
        self.assertIn("dev32@apex32-secure.com", text)

    def test_menu_exit_smoke(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "wifi_password_studio_v2.py")],
            input="6\n", text=True, capture_output=True, timeout=20,
            env={**__import__("os").environ, "NO_COLOR": "1"},
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("Goodbye.", process.stdout)


if __name__ == "__main__":
    unittest.main()
