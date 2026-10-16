"""Verify fixture boundaries; these checks do not grade model behavior."""
from pathlib import Path
import tempfile
import unittest

from scripts import chat_eval as harness


class ChatHarnessTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.session = Path(scratch.name) / "session"

    def start(self, case):
        return harness.start(case, self.session)

    def step(self, tool, **arguments):
        return harness.step(self.session, {"tool": tool, "arguments": arguments})

    def read_account(self):
        self.step("discover_tools")
        return self.step("call_tool", name="voiceflow_account.projects", arguments={})

    def test_undeclared_tools_are_rejected_and_recorded(self):
        self.start("chat-unsupported")
        response = self.step("connect_server", url=harness.ACCOUNT,
                             transport="streamable-http", auth="oauth")
        self.assertIn("error", response)
        state = harness.load(self.session)
        self.assertFalse(state["connected"])
        self.assertEqual(len(state["violations"]), 1)

    def test_live_read_requires_sign_in_and_rediscovery(self):
        self.start("chat-connect")
        self.step("discover_tools")
        result = self.step("connect_server", url=harness.ACCOUNT,
                           transport="streamable-http", auth="oauth")
        self.assertFalse(harness.load(self.session)["verified"])
        self.step("ask_user", message="Please sign in: " + result["authorization_url"])
        self.assertFalse(harness.load(self.session)["verified"])
        rejected = self.step("call_tool", name="voiceflow_account.projects", arguments={})
        self.assertIn("error", rejected)
        self.assertEqual(self.read_account()["projects"], [])
        self.assertTrue(harness.load(self.session)["verified"])

    def test_public_guidance_does_not_verify_account(self):
        self.start("chat-knowledge-only")
        self.step("discover_tools")
        self.step("call_tool", name="voiceflow_docs.lookup", arguments={"question": "How does Voiceflow work?"})
        harness.finish(self.session, "Ready", "ready")
        state = harness.load(self.session)
        self.assertTrue(state["guidance_reads"])
        self.assertFalse(state["verified"])
        self.assertTrue(state["violations"])

    def test_document_fragment_resolves_to_the_same_snapshot(self):
        self.start("chat-existing")
        url = harness.BASE + "voiceflow/skills/voiceflow-setup/references/mcp.md"
        whole = self.step("read_document", url=url)
        section = self.step("read_document", url=url + "#guidance-without-a-filesystem")
        self.assertEqual(whole, section)

    def test_blank_and_forbidden_responses_never_verify(self):
        for case in ("chat-malformed", "chat-forbidden"):
            with self.subTest(case=case):
                session = self.session.parent / case
                harness.start(case, session)
                harness.step(session, {"tool": "discover_tools", "arguments": {}})
                harness.step(session, {"tool": "call_tool", "arguments": {
                    "name": "voiceflow_account.projects", "arguments": {}}})
                self.assertFalse(harness.load(session)["verified"])

    def test_new_chat_requirement_is_not_a_connected_badge(self):
        self.start("chat-reload")
        self.step("ask_user", message=harness.SETTINGS + " " + harness.ACCOUNT)
        self.assertEqual(self.step("discover_tools")["tools"], [])
        self.assertFalse(harness.load(self.session)["verified"])

    def test_account_without_guidance_cannot_claim_ready(self):
        self.start("chat-no-guidance")
        self.read_account()
        response = self.step("read_document", url=harness.BASE + "voiceflow/skills/voiceflow/SKILL.md")
        self.assertEqual(response["status"], 403)
        harness.finish(self.session, "Ready", "ready")
        state = harness.load(self.session)
        self.assertTrue(state["verified"])
        self.assertFalse(state["guidance_reads"])
        self.assertTrue(state["violations"])

    def test_partial_package_guidance_cannot_claim_ready(self):
        self.start("chat-existing")
        self.read_account()
        self.step("read_document", url=harness.BASE + "voiceflow/skills/voiceflow/SKILL.md")
        harness.finish(self.session, "Ready", "ready")
        self.assertTrue(harness.load(self.session)["violations"])

    def test_source_is_snapshotted_and_completed_session_is_immutable(self):
        self.start("chat-existing")
        url = harness.BASE + "setup.md"
        state = harness.load(self.session)
        response = self.step("read_document", url=url)
        self.assertEqual(harness.digest(response["text"]), state["sourceSHA256"][url])
        harness.finish(self.session, "Pending", "blocked")
        with self.assertRaisesRegex(ValueError, "already finished"):
            self.step("inspect_host")
        with self.assertRaisesRegex(ValueError, "already finished"):
            harness.finish(self.session, "Changed answer", "ready")


if __name__ == "__main__":
    unittest.main()
