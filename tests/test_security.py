"""Real scanner acceptance using disposable, synthetic credentials; never auth."""
import base64
import importlib.util
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scan_secrets", ROOT / "scripts/scan_secrets.py")
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class SecretScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("gitleaks"):
            if os.environ.get("REQUIRE_GITLEAKS") == "1":
                raise RuntimeError("Security CI requires a working Gitleaks executable")
            raise unittest.SkipTest("Install Gitleaks to run scanner acceptance checks")

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        # Assemble a random provider-shaped canary, never a usable credential.
        self.canary = "gh" + "p_" + secrets.token_hex(18)

    def scan(self, mode="dir"):
        return scanner.scan(self.root, mode, ROOT / ".gitleaks.toml")

    def test_ignored_file_and_inline_allow_comment_do_not_hide_a_leak(self):
        (self.root / ".gitignore").write_text(".env\n", encoding="utf-8")
        (self.root / ".env").write_text("TOKEN=" + self.canary + " # gitleaks:allow\n", encoding="utf-8")
        findings = self.scan()
        self.assertTrue(findings, "Scanner missed a synthetic credential in .env")
        self.assertNotIn(self.canary, str(findings), "Finding output must omit credential values")

    def test_deleted_credential_is_still_detected_in_history(self):
        def git(*args):
            subprocess.run(["git", "-c", "core.hooksPath=" + str(self.root / "no-hooks"),
                            "-c", "commit.gpgsign=false", *args], cwd=self.root,
                           capture_output=True, check=True, timeout=10)
        git("init", "-q")
        git("config", "user.email", "security-test@example.invalid")
        git("config", "user.name", "Synthetic test")
        path = self.root / "config.txt"
        path.write_text("TOKEN=" + self.canary, encoding="utf-8")
        git("add", "config.txt")
        git("-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic canary")
        git("rm", "config.txt")
        git("-c", "commit.gpgsign=false", "commit", "-qm", "Remove synthetic canary")
        self.assertTrue(self.scan("git"), "Scanner missed a deleted historical credential")

    def test_encoded_secret_inside_archive_is_detected(self):
        encoded = base64.b64encode(("TOKEN=" + self.canary).encode()).decode()
        with zipfile.ZipFile(self.root / "package.zip", "w") as archive:
            archive.writestr("payload.txt", encoded)
        self.assertTrue(self.scan(), "Scanner missed an encoded credential inside an archive")

    def test_voiceflow_key_formats_are_detected_without_an_assignment(self):
        for kind in ("DM.", "WS.", "SA.", ""):
            with self.subTest(kind=kind):
                canary = "VF." + kind + secrets.token_hex(12) + "." + secrets.token_hex(32)
                (self.root / "accidental-note.md").write_text(canary, encoding="utf-8")
                findings = self.scan()
                self.assertIn("voiceflow-api-key", {finding["RuleID"] for finding in findings})

    def test_clean_files_pass(self):
        (self.root / "guide.md").write_text("Use browser OAuth; never paste credentials here.\n", encoding="utf-8")
        self.assertEqual(self.scan(), [])

    def test_scanner_failure_is_not_a_clean_scan_or_secret_in_logs(self):
        failed = subprocess.CompletedProcess([], 2, self.canary, self.canary)
        with patch.object(scanner.subprocess, "run", return_value=failed):
            with self.assertRaises(RuntimeError) as error:
                self.scan()
        self.assertNotIn(self.canary, str(error.exception))
