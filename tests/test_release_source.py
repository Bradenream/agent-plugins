"""Release trust-boundary cases with synthetic GitHub responses; no account writes."""
import importlib.util
import copy
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
        self.rules = [
            {"type": "deletion"}, {"type": "non_fast_forward"},
            {"type": "pull_request", "parameters": {
                "required_approving_review_count": 1,
                "dismiss_stale_reviews_on_push": True,
                "require_code_owner_review": True,
                "required_review_thread_resolution": True,
            }},
            {"type": "required_status_checks", "parameters": {
                "strict_required_status_checks_policy": True,
                "required_status_checks": [{"context": name, "integration_id": 15368} for name in (
                    "security / Secrets and workflow security", "checks (ubuntu-latest)",
                    "checks (macos-latest)", "checks (windows-latest)")],
            }},
        ]

    def verify(self, status="ahead", protected=True, workflow_ref="refs/heads/main",
               merge_base=None, branch_name="main"):
        responses = [{"default_branch": branch_name},
                     {"protected": protected, "commit": {"sha": self.head}},
                     self.rules,
                     {"status": status, "merge_base_commit": {"sha": merge_base or self.commit}}]
        with patch.object(guard, "github_json", side_effect=responses) as api:
            result = guard.verify("example/package", self.commit, "0.4.2", workflow_ref, api=api)
            self.assertEqual(api.call_args.args[0],
                             "repos/example/package/compare/" + self.commit + "..." + self.head)
            return result

    def test_protected_flag_without_required_active_rules_is_rejected(self):
        for rules in ([], [{"type": "non_fast_forward"}], {"rules": self.rules}, [None]):
            self.rules = rules
            with self.subTest(rules=rules), self.assertRaises(ValueError):
                self.verify()

    def test_weak_review_requirements_are_rejected(self):
        for key, value in (("required_approving_review_count", 0),
                           ("required_approving_review_count", True),
                           ("required_approving_review_count", "1"),
                           ("dismiss_stale_reviews_on_push", False),
                           ("require_code_owner_review", False),
                           ("required_review_thread_resolution", False)):
            with self.subTest(key=key, value=value):
                original = copy.deepcopy(self.rules)
                self.rules[2]["parameters"][key] = value
                with self.assertRaisesRegex(ValueError, "review"):
                    self.verify()
                self.rules = original

    def test_each_required_check_must_be_present_strict_and_from_actions(self):
        original = copy.deepcopy(self.rules)
        for index in range(4):
            for change in ("missing", "wrong_app", "unspecified_app"):
                self.rules = copy.deepcopy(original)
                checks = self.rules[3]["parameters"]["required_status_checks"]
                if change == "missing":
                    checks.pop(index)
                elif change == "wrong_app":
                    checks[index]["integration_id"] = 99
                else:
                    del checks[index]["integration_id"]
                with self.subTest(index=index, change=change), self.assertRaisesRegex(ValueError, "four"):
                    self.verify()
        self.rules = original
        self.rules[3]["parameters"]["strict_required_status_checks_policy"] = False
        with self.assertRaisesRegex(ValueError, "strict"):
            self.verify()

    def test_deletion_and_force_push_protection_are_both_required(self):
        for removed in ("deletion", "non_fast_forward"):
            original = self.rules
            self.rules = [rule for rule in original if rule["type"] != removed]
            with self.subTest(removed=removed), self.assertRaisesRegex(ValueError, "deletion and force"):
                self.verify()
            self.rules = original

    def test_active_rules_pagination_is_complete_and_bounded(self):
        with patch.object(guard, "github_json", side_effect=[[{"type": "other"}] * 100, self.rules]) as api:
            guard.verify_rules("repos/example/package", "stable/release", api)
            self.assertEqual(api.call_count, 2)
            self.assertEqual(api.call_args.args[0],
                             "repos/example/package/rules/branches/stable%2Frelease?per_page=100&page=2")
        with patch.object(guard, "github_json", return_value=[{"type": "other"}] * 100) as api:
            with self.assertRaisesRegex(ValueError, "Too many"):
                guard.verify_rules("repos/example/package", "main", api)
            self.assertEqual(api.call_count, 10)

    def test_rules_api_failure_blocks_before_candidate_comparison(self):
        with patch.object(guard, "github_json", side_effect=[
                {"default_branch": "main"}, {"protected": True, "commit": {"sha": self.head}},
                RuntimeError("release blocked")]) as api:
            with self.assertRaises(RuntimeError):
                guard.verify("example/package", self.commit, "0.4.2", "refs/heads/main", api=api)
            self.assertEqual(api.call_count, 3)

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
