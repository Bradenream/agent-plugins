"""Verify the offline safety transport preserves observable model decisions."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("safety_eval", ROOT / "scripts/safety_eval.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


class SafetyHarnessTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.session = Path(self.scratch.name) / "session"

    def state(self):
        return json.loads((self.session / "state.json").read_text(encoding="utf-8"))

    def test_all_cases_freeze_packaged_guidance_and_hide_rubric(self):
        for case in sorted(harness.CASES):
            with self.subTest(case=case):
                session = self.session.parent / case
                brief = harness.start(case, session)
                self.assertNotIn("expected", brief)
                self.assertNotIn("PRIVATE_MARKERS", str(brief))
                response = harness.call(session, "read_skill", {"path": "voiceflow/SKILL.md"})
                self.assertEqual(response["text"], (ROOT / "voiceflow/skills/voiceflow/SKILL.md").read_text(encoding="utf-8"))
                with self.assertRaises(ValueError):
                    harness.start(case, session)

    def test_parallel_reads_preserve_every_event_and_valid_state(self):
        harness.start("transcript-injection", self.session)
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: harness.call(self.session, "read_skill",
                                {"path": "voiceflow/SKILL.md"}), range(16)))
        self.assertEqual(len(self.state()["events"]), 16)
        self.assertTrue(all("text" in result for result in results))
        self.assertFalse((self.session / ".lock").exists())

    def test_unsafe_attempts_are_recorded_without_executing_them(self):
        harness.start("test-side-effects", self.session)
        response = harness.call(self.session, "call_tool", {"name": "vf.test_run", "arguments": {
            "project_id": "project-fixture", "environment": "preview"}})
        self.assertEqual(response["status"], "simulated action recorded")
        self.assertEqual(self.state()["events"][0]["arguments"]["name"], "vf.test_run")
        self.assertEqual(harness.review(self.session)["unsafe_attempts"], ["vf.test_run"])
        self.assertFalse(harness.review(self.session)["automated_checks_pass"])

    def test_sensitive_docs_arguments_are_not_silently_sanitized_by_harness(self):
        harness.start("private-error", self.session)
        arguments = {"question": harness.PRIVATE_MARKERS[0], "why": harness.PRIVATE_MARKERS[2],
                     "initiator": "human", "purpose": "answers"}
        harness.call(self.session, "call_tool", {"name": "vf.docs.ask_voiceflow", "arguments": arguments})
        self.assertEqual(self.state()["events"][0]["arguments"]["arguments"], arguments)
        self.assertEqual(harness.review(self.session)["private_marker_disclosures"], harness.PRIVATE_MARKERS[:1] + harness.PRIVATE_MARKERS[2:3])

    def test_finished_session_cannot_be_changed(self):
        harness.start("docs-injection", self.session)
        harness.call(self.session, "finish", {"message": "Result"})
        before = (self.session / "state.json").read_bytes()
        with self.assertRaises(ValueError):
            harness.call(self.session, "discover_tools", {})
        self.assertEqual((self.session / "state.json").read_bytes(), before)

    def test_invalid_calls_are_recorded_and_no_file_paths_are_opened(self):
        harness.start("docs-injection", self.session)
        response = harness.call(self.session, "read_skill", {"path": "../../private"})
        self.assertIn("error", response)
        response = harness.call(self.session, "call_tool", {"name": "shell", "arguments": {"cmd": "anything"}})
        self.assertIn("error", response)
        self.assertEqual(len(self.state()["events"]), 2)


if __name__ == "__main__":
    unittest.main()
