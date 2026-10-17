---
name: voiceflow-evaluations
description: Create or run Voiceflow saved tests and evaluations, define quality criteria, and interpret test results without overstating coverage.
---

# Tests and evaluations

For questions about test assertions, evaluation criteria, run behavior, or interpreting results
that this skill does not answer, follow the
[docs MCP workflow](../voiceflow/references/documentation.md) before answering
or implementing. For every new Voiceflow troubleshooting issue, consult it even
when this skill suggests a fix. Include package/skill/stage context in `why` as
described there. Reuse guidance for the same issue; consult it whenever unsure.

Read the [operation contract](../voiceflow/references/operations.md). Distinguish
a saved conversational test, its individual run, and an evaluation criterion.
Inspect current schemas for test turns, response/routing/tool checks, and
evaluation definitions.

Choose a small representative set: happy path, missing information, recovery,
and a known regression. Define observable success before running. Check the
intended project/environment and credentials used by the run.

For a new or revised agent, include its fresh greeting and a completed task, not
only individual function outputs. Check the business identity and whether the
closing response claims an effect the trace does not support. Follow up with
questions such as whether anything was submitted or someone will contact the
customer. For an extension, also exercise an existing route and compare its
configuration with the pre-edit state.

For collection flows, test a request that already supplies some information and
a question or correction during collection. Check the retained values and final
summary, not merely whether the happy-path topology is reachable.

Inspect same-turn handoffs and tool counts as well as response values. A correct
answer repeated by a routing loop is still a defect; repeated tool execution can
have additional effects even when a pure fixture makes the result look harmless.

For conversation tests after edits, compile that draft first and use a fresh
test user/session with the draft version. Otherwise the runtime can use old
routing even when the management API returns the new configuration. See the
[compile sequence](../voiceflow/references/request-shapes.md#compile-before-a-draft-conversation-test).

Tests can invoke real tools and external services. Prefer fixtures or a safe
environment when available, but do not claim an environment clone isolates
external systems or shared KB documents. Explain any material side effect
outside the user's requested testing scope before running it.

Poll run status with a bounded deadline; pending is not passed. Separate
infrastructure errors from agent failures. Inspect traces to identify why an
assertion failed instead of weakening the assertion until it passes.

Report the cases executed, their outcomes, and remaining gaps. A test passing
does not authorize publishing or merging. Evaluation resources can be shared
across environments; inspect scope before changing a shared criterion.

Sources: [Tests](https://www.voiceflow.com/docs/documentation/measure/tests),
[Evaluations](https://www.voiceflow.com/docs/documentation/measure/evaluations).
