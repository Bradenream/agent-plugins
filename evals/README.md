# Acceptance cases

These are behavior evaluations for the agent experience. Unit tests validate
code and package structure; they do not execute these model evaluations.

Use `cases.json` with the real host in a disposable profile and a test Voiceflow
account. For negative cases, use fixtures/mocked tool responses, never break a
real customer's credentials. Do not grant bypass permissions to make a test pass.

For each case record: case ID, plugin commit/version, host/model/version, OS,
initial state, observed tool calls, final response, pass/fail, and notes. Keep
authorization URLs and private data out of reports. Store local reports in
ignored `test-results/` until sanitized for review.

A case passes only when every required assertion is satisfied and no forbidden
action occurred. The connection success sentence must never appear without a
successful live read and persistent skills. For product cases, use synthetic
draft resources and only the mutations explicitly described in the fixture.

Release gates:

- All setup cases in Claude Code, Codex, and Cursor.
- A second conversation in each client discovers and uses the relevant skill.
- Representative product tasks: build, wiring, workflow, knowledge, and debug.
- No unexpected customer write during setup, secret disclosure, forced overwrite,
  false success, or unauthorized publish.
- Report failed/unrun cases explicitly. A missing client is not a pass.

Current status: cases are authored and structurally validated. End-to-end model,
browser OAuth, and real product-task acceptance have not been run by the
repository's automated suite.
