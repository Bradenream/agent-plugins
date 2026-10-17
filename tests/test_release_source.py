"""Release trust-boundary cases with synthetic GitHub responses; no account writes."""
import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_source", ROOT / "scripts/verify_release_source.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class ReleaseSourceTests(unittest.TestCase):
    def setUp(self):
        self.commit = "a" * 40
        self.head = "b" * 40

    def verify(self, status="ahead", protected=True, workflow_ref="refs/heads/main",
               merge_base=None, branch_name="main"):
        responses = [{"default_branch": branch_name},
                     {"protected": protected, "commit": {"sha": self.head}},
                     {"status": status, "merge_base_commit": {"sha": merge_base or self.commit}}]
        with patch.object(guard, "github_json", side_effect=responses) as api:
            result = guard.verify("example/package", self.commit, "0.4.2", workflow_ref, api=api)
            self.assertEqual(api.call_args.args[0],
                             "repos/example/package/compare/" + self.commit + "..." + self.head)
            return result

    def test_current_and_ancestor_commits_are_eligible(self):
        self.assertEqual(self.verify(), "main")
        self.head = self.commit
        self.assertEqual(self.verify(status="identical"), "main")

    def test_unmerged_and_divergent_commits_are_rejected(self):
        for status in ("behind", "diverged"):
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, "already be on"):
                self.verify(status=status)
        with self.assertRaisesRegex(ValueError, "already be on"):
            self.verify(merge_base="c" * 40)

    def test_unprotected_default_branch_is_rejected(self):
        for protected in (False, None):
            with self.subTest(protected=protected), self.assertRaisesRegex(ValueError, "protected"):
                self.verify(protected=protected)

    def test_dispatch_from_a_feature_branch_or_tag_is_rejected(self):
        for ref in ("refs/heads/codex/change", "refs/tags/v0.4.2"):
            with self.subTest(ref=ref), self.assertRaisesRegex(ValueError, "workflow from"):
                self.verify(workflow_ref=ref)

    def test_renamed_default_branch_is_supported(self):
        self.assertEqual(self.verify(branch_name="stable/release",
                                     workflow_ref="refs/heads/stable/release"), "stable/release")

    def test_bad_identifiers_fail_before_network(self):
        for values in (("../../other", self.commit, "0.4.2"),
                       ("example/package", "main", "0.4.2"),
                       ("example/package", self.commit, "v0.4.2")):
            with patch.object(guard, "github_json") as api:
                with self.assertRaises(ValueError):
                    guard.verify(*values, "refs/heads/main", api=api)
                api.assert_not_called()

    def test_api_failure_does_not_allow_a_release_or_print_response(self):
        failed = subprocess.CompletedProcess([], 1, "private response", "private error")
        with patch.object(guard.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "release blocked") as error:
                guard.github_json("repos/example/package")
        self.assertNotIn("private", str(error.exception))
