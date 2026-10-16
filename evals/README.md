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
successful account read and accessible guidance. Persist skills only in hosts
that support it; chat assistants must describe session-only guidance honestly.
Public documentation access does not verify account access. For product cases, use synthetic
draft resources and only the mutations explicitly described in the fixture.

Release gates:

- All setup cases in Claude Code, Codex, and Cursor.
- Chat setup cases in each real chat application we claim to support, including
  browser OAuth, tool rediscovery, and its actual account permissions.
- A second conversation in each client discovers and uses the relevant skill.
- Representative product tasks: build, wiring, workflow, knowledge, and debug.
- No unexpected customer write during setup, secret disclosure, forced overwrite,
  false success, or unauthorized publish.
- Report failed/unrun cases explicitly. A missing client is not a pass.

## Capability-constrained subagent tests

`scripts/chat_eval.py` is an offline fixture transport for the twelve `chat-*`
cases. It snapshots the real package Markdown and published link rewriting,
exposes only each simulated host's tools, records requests/responses, and never
contacts a service. A controller's Python process is not a terminal available to
the simulated customer. The model must not inspect the runner, scenario source,
expected assertions, or session files. It follows only the returned user request,
guide, capabilities, and tool results.

Use a fresh temporary directory for each case:

```sh
python3 scripts/chat_eval.py start --case chat-existing --session /tmp/vf-eval-unique
python3 scripts/chat_eval.py step --session /tmp/vf-eval-unique --request '{"tool":"read_document","arguments":{"url":"https://preview.invalid/agents/setup.md"}}'
```

Continue with `step` and a declared tool/arguments object; `ask_user` receives a
fixture reply rather than contacting a real user. Record the customer response
with `finish --status ready|blocked|needs_user --message '...'`. A finished
session cannot be rewritten. Review its recorded actions and final response
against `cases.json`; do not ask the model to grade itself. Keep source hashes,
model/runtime, run grouping, and any failures in the sanitized report.

These are instruction-constrained model simulations, not separate non-coding
model products or live ChatGPT/Claude sessions. The harness rejects unavailable
simulated tools; the subagent's broader runtime is restricted by its evaluation
instructions. A passing simulation does not prove OAuth callbacks, app policy,
tool discovery, or fresh-chat persistence in a real client.

Browser OAuth and real product-task acceptance remain unrun by the repository's
automated suite. See the committed reports for separately run model simulations.
