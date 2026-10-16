import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "voiceflow/skills/voiceflow-setup/scripts"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("installer", SETUP / "install_skills.py")
connection = load("connection", SETUP / "check_connection.py")
builder = load("builder", ROOT / "scripts/build.py")
validator = load("validator", ROOT / "scripts/validate.py")


class SkillInstallTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.source = self.base / "source"
        self.target = self.base / "target"
        self.skill = self.source / "voiceflow/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("original")

    def test_repeat_and_uninstall_preserve_unrelated_files(self):
        self.assertEqual(installer.install(self.source, self.target), "installed")
        unrelated = self.target / "another-skill.txt"
        unrelated.write_text("keep")
        self.assertEqual(installer.install(self.source, self.target), "unchanged")
        self.assertEqual(installer.install(self.source, self.target, uninstall=True), "removed")
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep")
        self.assertFalse((self.target / "voiceflow/SKILL.md").exists())

    def test_conflict_fails_before_any_write(self):
        self.target.mkdir()
        existing = self.target / "voiceflow/SKILL.md"
        existing.parent.mkdir()
        existing.write_text("custom")
        (self.source / "voiceflow/new.md").write_text("new")
        with self.assertRaisesRegex(ValueError, "Existing file"):
            installer.install(self.source, self.target)
        self.assertEqual(existing.read_text(encoding="utf-8"), "custom")
        self.assertFalse((self.target / "voiceflow/new.md").exists())

    def test_edited_file_blocks_update_and_removal(self):
        installer.install(self.source, self.target)
        (self.target / "voiceflow/SKILL.md").write_text("custom")
        for options in ({"update": True}, {"uninstall": True}):
            with self.assertRaisesRegex(ValueError, "Local change"):
                installer.install(self.source, self.target, **options)
        self.assertEqual((self.target / "voiceflow/SKILL.md").read_text(encoding="utf-8"), "custom")

    def test_intentional_update_replaces_only_managed_files(self):
        installer.install(self.source, self.target)
        self.skill.write_text("updated")
        with self.assertRaisesRegex(ValueError, "--update"):
            installer.install(self.source, self.target)
        self.assertEqual(installer.install(self.source, self.target, update=True), "installed")
        self.assertEqual((self.target / "voiceflow/SKILL.md").read_text(encoding="utf-8"), "updated")

    def test_removed_file_is_not_silently_restored(self):
        installer.install(self.source, self.target)
        (self.target / "voiceflow/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Local change"):
            installer.install(self.source, self.target, update=True)

    def test_receipt_cannot_escape_target(self):
        self.target.mkdir()
        (self.target / installer.RECEIPT).write_text(json.dumps({"files": {"../secret": "fake"}}))
        with self.assertRaisesRegex(ValueError, "Invalid managed"):
            installer.install(self.source, self.target, uninstall=True)

    def test_symlink_destination_refused(self):
        self.target.mkdir()
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.target / "voiceflow").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation unavailable on this host")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            installer.install(self.source, self.target)
        self.assertEqual(list(outside.iterdir()), [])

    def test_partial_failure_rolls_back_written_files(self):
        installer.install(self.source, self.target)
        receipt_before = (self.target / installer.RECEIPT).read_bytes()
        self.skill.write_text("updated")
        (self.source / "voiceflow/new.md").write_text("new")
        original = os.replace
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated disk failure")
            return original(source, target)

        with patch.object(installer.os, "replace", side_effect=fail_second):
            with self.assertRaises(OSError):
                installer.install(self.source, self.target, update=True)
        self.assertEqual((self.target / "voiceflow/SKILL.md").read_text(encoding="utf-8"), "original")
        self.assertEqual((self.target / installer.RECEIPT).read_bytes(), receipt_before)
        self.assertFalse((self.target / "voiceflow/new.md").exists())

    def test_complete_packaged_skill_tree_installs(self):
        installer.install(ROOT / "voiceflow/skills", self.target)
        self.assertEqual(len(list(self.target.glob("*/SKILL.md"))), 15)
        self.assertTrue((self.target / "voiceflow-setup/references/setup.md").is_file())


class ConnectionTests(unittest.TestCase):
    def test_empty_and_populated_accounts_are_ready(self):
        for data in ({"workspaces": []}, {"workspaces": [{"id": "private", "name": "private"}]}):
            self.assertEqual(connection.classify(0, json.dumps(data), ""), "connected")

    def test_structured_failures_are_distinct(self):
        for kind, expected in {
            "authentication_error": "authentication_required",
            "authorization_error": "permission_denied",
            "connection_error": "temporarily_unavailable",
            "rate_limit_error": "temporarily_unavailable",
            "server_error": "temporarily_unavailable",
            "validation_error": "request_failed",
        }.items():
            with self.subTest(kind=kind):
                payload = json.dumps({"error_type": kind, "message": "private token"})
                self.assertEqual(connection.classify(1, "", payload), expected)

    def test_bad_success_is_not_connected(self):
        for output in ("", "<html>proxy</html>", "{}", "null", '{"error":"unauthorized"}'):
            self.assertNotEqual(connection.classify(0, output, ""), "connected")
        self.assertNotEqual(connection.classify(1, '{"workspaces":[]}', ""), "connected")

    def test_typed_toon_workspace_envelope(self):
        for output in ("workspaces[0]:", "workspaces[1]{id,name}:\n  123,Example\n",
                       "workspaces[1]:\n  - id: 123\n    name: Example\n"):
            self.assertEqual(connection.classify(0, output, ""), "connected")
        for output in ("workspaces: null", "workspaces[0]", "some text workspaces[0]:"):
            self.assertNotEqual(connection.classify(0, output, ""), "connected")

    def test_probe_is_read_only_bounded_and_does_not_echo_output(self):
        result = subprocess.CompletedProcess([], 0, '{"workspaces":[{"secret":"hidden"}]}', "")
        with patch.object(connection.subprocess, "run", return_value=result) as run:
            self.assertEqual(connection.check("/path/to/vf"), "connected")
        args, kwargs = run.call_args
        self.assertEqual(args[0][1:3], ["workspace", "list"])
        self.assertEqual(kwargs["timeout"], 25)
        self.assertNotIn("--debug", args[0])
        self.assertEqual(args[0][-2:], ["-o", "toon"])

    def test_missing_cli_and_timeout(self):
        for error, expected in ((FileNotFoundError(), "cli_missing"),
                                (subprocess.TimeoutExpired("vf", 25), "temporarily_unavailable")):
            with patch.object(connection.subprocess, "run", side_effect=error):
                self.assertEqual(connection.check("vf"), expected)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        shutil.copytree(ROOT / "voiceflow", self.root / "voiceflow",
                        ignore=shutil.ignore_patterns("__pycache__"))

    def test_archive_and_site_are_reproducible_and_complete(self):
        site = builder.build(self.root)
        first = {p.relative_to(site): p.read_bytes() for p in site.rglob("*") if p.is_file()}
        manifest = json.loads((site / "manifest.json").read_text(encoding="utf-8"))
        for name, expected in manifest["files"].items():
            self.assertEqual(builder.sha((site / name).read_bytes()), expected)
        self.assertTrue(manifest["hasUncommittedChanges"])
        with zipfile.ZipFile(site / "voiceflow.zip") as archive:
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))
            self.assertEqual(len([n for n in archive.namelist() if n.endswith("/SKILL.md")]), 15)
            for info in archive.infolist():
                self.assertTrue(info.filename.startswith("voiceflow/"))
                self.assertNotIn("..", info.filename.split("/"))
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.create_system, 3)
        for link in validator.markdown_links((site / "setup.md").read_text(encoding="utf-8")):
            if "://" not in link and not link.startswith("#"):
                self.assertTrue((site / link.split("#")[0]).is_file(), link)
        builder.build(self.root)
        second = {p.relative_to(site): p.read_bytes() for p in site.rglob("*") if p.is_file()}
        self.assertEqual(first, second)

    def test_rewriter_preserves_code_and_external_links(self):
        source = self.root / "voiceflow/skills/voiceflow-setup/references/setup.md"
        sample = "[client](clients.md#codex)\n```md\n[do not change](missing.md)\n```\n[x](https://example.com)\n"
        rewritten = builder.rewrite_setup(sample, source, self.root)
        self.assertIn("voiceflow/skills/voiceflow-setup/references/clients.md#codex", rewritten)
        self.assertIn("[do not change](missing.md)", rewritten)
        self.assertIn("[x](https://example.com)", rewritten)

    def test_rewriter_refuses_missing_or_escaping_references(self):
        source = self.root / "voiceflow/skills/voiceflow-setup/references/setup.md"
        for link in ("missing.md", "../../../../../../outside.md"):
            with self.assertRaises(ValueError):
                builder.rewrite_setup(f"[link]({link})", source, self.root)

    def test_arbitrary_output_refused_without_deletion(self):
        protected = self.root / "keep"
        protected.mkdir()
        with self.assertRaises(ValueError):
            builder.build(self.root, protected)
        self.assertTrue(protected.is_dir())


class RepositoryTests(unittest.TestCase):
    def test_all_manifests_and_skill_links(self):
        self.assertEqual(validator.validate(), 15)


@unittest.skipIf(os.name == "nt", "Unix installer; Windows installer runs in Windows CI")
class UnixInstallerTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.commands = self.base / "commands"
        self.commands.mkdir()
        self.target = self.base / "install"
        self.env = dict(os.environ, VF_INSTALL_DIR=str(self.target),
                        PATH=str(self.commands) + os.pathsep + os.environ["PATH"])

    def run_installer(self):
        return subprocess.run(["bash", str(SETUP / "install-vf.sh")], env=self.env,
                              capture_output=True, text=True, encoding="utf-8", timeout=10)

    def fake_curl(self, script):
        path = self.commands / "curl"
        path.write_text("#!/bin/bash\n" + script)
        path.chmod(0o755)

    def test_checksum_failure_never_installs(self):
        self.fake_curl('for last; do :; done\nprintf "tampered" > "$last"\n')
        result = self.run_installer()
        self.assertEqual(result.returncode, 4, result.stderr)
        self.assertFalse(self.target.exists())

    def test_download_failure_never_installs(self):
        self.fake_curl("exit 22\n")
        self.assertEqual(self.run_installer().returncode, 22)
        self.assertFalse(self.target.exists())

    def test_existing_executable_is_untouched(self):
        self.target.mkdir()
        binary = self.target / "vf"
        binary.write_bytes(b"existing")
        self.assertEqual(self.run_installer().returncode, 3)
        self.assertEqual(binary.read_bytes(), b"existing")


if __name__ == "__main__":
    unittest.main()
