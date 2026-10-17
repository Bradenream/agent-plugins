# Live product acceptance — 2026-10-16

**The initial eight runs passed 29 of 40 functional task checks. After targeted
guidance changes, fresh Luna low-reasoning runs passed all five checks over both
CLI and MCP. This is useful regression evidence, not a launch-readiness or
statistical reliability claim. Sample-company identity still leaked into the
retested agents' greetings.**

These were real account operations: CLI reused an existing sign-in, and the
user completed native hosted-MCP OAuth. All changes were confined to a dedicated
synthetic project in the user-selected workspace. Ten separate draft environments
held the eight baseline runs and two retests. No publishing, merging, deletion,
or traffic changes were observed. Each test environment retained zero traffic
and its original single release. Test resources remain available for inspection.

## Baseline

Package 0.2.0 at `df75808bdff7c7f5b5a30b44894dad09c50b7d8f` was frozen for all
eight runs. The five items were an appointment playbook, an order function with
captured outputs, a deterministic confirmation workflow, knowledge import and
retrieval, and repair of a seeded function bug.

| Transport | Model / reasoning | Appointment | Wiring | Workflow | Knowledge | Debug | Checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLI | Luna / low | Pass | Incomplete | Incomplete | Pass | Pass | 3/5 |
| CLI | Luna / medium | Pass | Incomplete | Incomplete | Pass | Pass | 3/5 |
| CLI | Sol / low | Pass | Pass | Pass | Pass | Pass | 5/5 |
| CLI | Sol / medium | Pass | Pass | Pass | Pass | Pass | 5/5 |
| MCP | Luna / low | Incomplete | Incomplete | Incomplete | Incomplete | Incomplete | 0/5 |
| MCP | Luna / medium | Pass | Pass | Pass | Pass | Pass | 5/5 |
| MCP | Sol / low | Pass | Pass | Pass | Incomplete | Pass | 4/5 |
| MCP | Sol / medium | Pass | Pass | Pass | Incomplete | Pass | 4/5 |

Models were `gpt-6-luna` and `gpt-6.1-sol`. A pass covers the named task's
functional requirements; it does not imply a polished customer experience.
Known incomplete constructions were not passed based on the actor's answer.

The verifier read actual resources, declarations, bindings, message references,
and routes. It executed each available pure function with two distinct inputs
and queried the draft knowledge base for the unique policy code. After compiling
the relevant drafts, it ran appointment conversations for seven baseline agents,
order conversations for the five with attachments, and confirmation conversations
for the five with complete workflows. Order state changed from `EVAL-101` to
`EVAL-202` with status `processing`; confirmation emitted the exact sentence
followed by an End trace.

## Findings and corrections

- **Management request shapes were the main obstacle.** Luna CLI runs created
  the function but could not attach it; one workflow ended without its required
  message. MCP Luna low put execution inputs outside the body and abandoned
  otherwise available operations. Successful runs established the precise
  target, binding, route, and message-step fields.
- **MCP text upload works without a terminal.** Both Sol MCP runs failed to
  discover the file representation. Luna medium found the working
  `body.file` object with `filename`, `mimeType`, and `content`, and retrieval
  verified its real content. It first created an `undefined`-named duplicate;
  the CLI Luna low baseline also left an extra `policy.txt` import.
- **Compile before conversation testing.** All four baseline CLI actors stopped
  at saved configuration. Initial verifier conversations consequently ran the
  old compiled routing and reported no playbooks/workflows. The verifier then
  compiled those drafts and repeated checks with fresh users. The working
  routes, captures, and workflows then executed correctly. Successful MCP actors
  compiled their drafts themselves. This was a missing test prerequisite, not
  evidence of a broken routing backend.
- **Function debugging worked when requests were formed correctly.** Actual
  execution reproduced `Buffer is not defined`; repaired functions preserved
  their declarations and returned both expected normalized addresses.
- **Conversation quality needs separate checks.** Baseline Luna medium agents
  promised submission or human follow-up without a corresponding action.
  Some agents also retained the default Acme Corp identity. These observations
  are not concealed by the narrower functional pass count.

Version 0.2.1 adds a progressively disclosed request-shape reference and links
from the relevant skills. It documents the tested upload, binding, routing,
message/end, and compilation shapes. Build guidance also distinguishes request
collection from actual submission and calls for updating sample-company identity.
It does not install approval hooks, change authentication, or vendor private code.

## Fresh retests

The same five-part request was rerun in two new draft environments with fresh
Luna low contexts and the revised skills. Actors received no previous transcript,
grader results, or baseline resource IDs. These are targeted regression cases
following examples derived from the failures, not held-out generalization tests.

| Transport | Before | Retest | Actor elapsed time | Independent runtime verification |
| --- | --- | --- | --- | --- |
| CLI | 3/5 | 5/5 | 153 seconds | Appointment, two order captures, exact confirmation + End, KB retrieval, both normalization inputs |
| MCP | 0/5 | 5/5 | 177 seconds | Appointment, two order captures, exact confirmation + End, KB retrieval, both normalization inputs |

Both retest actors compiled their own drafts. Each created one correctly named
policy document, with no duplicate import. Both distinguished stored checks
from runtime tests in their final reports; the independent verifier supplied
the conversation evidence. Their request summaries avoided the earlier false
submission/follow-up claim, but **the default Acme Corp greeting still appeared
in both retests**. The identity instruction alone did not reliably fix that.

Normal automatic approval review remained enabled. In the CLI retest it declined
two commands: one used a mistyped executable path, and one used a filename that
did not match the requested document name. The actor corrected the requests and
normal review accepted them. No approval bypass was used. These results include
the host's review assistance; they are not an unattended no-review benchmark.

## Method and limits

- Codex CLI `0.162.0-alpha.2`, macOS `26.4`, Voiceflow CLI `0.287.0`, hosted
  Voiceflow account MCP. Native processes used fresh ephemeral contexts and
  normal automatic approval review. Guidance was copied unchanged per run.
- Each run was a five-task journey sharing one context. There was one sample
  per model/reasoning/transport cell, with a 20-minute cap; none reached the cap.
  Durations include discovery and approval overhead, exclude fixture setup and
  independent verification, and are not controlled latency benchmarks.
- One initial CLI attempt could not access the existing OS-keychain session
  from its sandbox. It made no changes and was excluded. The runner was corrected
  to use normal command approval for that exact CLI. An initial MCP smoke read
  similarly needed normal tool approval enabled before the scored runs began.
- CLI JSON output combined with its own timeout flag sometimes returned an
  empty successful response. The fixture controller used YAML; the independent
  verifier used JSON with an external subprocess deadline. Blank responses
  were never treated as successful verification or blindly retried mutations.
- The fixture started with empty route registries. It does not establish
  preservation of a complex existing agent, production integration behavior,
  secret handling, large knowledge imports, voice calls, or long-term reliability.
- MCP used real account tools in Codex with local guidance access. This does not
  prove installation, browser OAuth, tool discovery, or persistence in actual
  ChatGPT, Claude, or other non-coding chat applications. CLI reused an existing
  login; a fresh CLI sign-in was not tested here.

The next acceptance work should cover sample-identity removal, promises and
side-effect honesty, varied held-out tasks, repeated low-reasoning trials, and
the real chat clients we intend to support. The current result supports using
the improved package for further testing, not claiming universal reliability.

See the [protocol](../live-product-protocol.md) and
[sanitized evidence](2026-10-16-live-product.json) for exact checks, synthetic
conversation outputs, model settings, skill hashes, and raw-evidence hashes.
Raw local traces remain ignored; no credentials, OAuth links, account identity,
or customer data are included in the report.
