---
name: voiceflow-debug
description: Diagnose broken Voiceflow behavior from configuration, traces, and transcripts. Use for wrong routing, failed tools, empty values, or unexpected answers.
---

# Diagnose before editing

Read the [operation contract](../voiceflow/references/operations.md). Establish
the expected behavior, actual behavior, project, environment, and one relevant
conversation or failing step. Do not assume the currently published version is
the same as the draft.

Inspect the smallest useful evidence: current resource settings, routing,
attachment bindings, and relevant trace sections. Classify the failure as
instructions, retrieval, routing, state/wiring, integration, or runtime/version.

For a tool failure, distinguish model selection from missing inputs, external
HTTP failure, output shape, capture mapping, and dependent-call ordering.
Use [wiring](../voiceflow-wiring/SKILL.md); prompt edits cannot repair missing
output captures or IDs.

For an unexpected answer, check the actual retrieved source and active prompt
layer before rewriting persona text. For workflow failures, read ports and
branch topology rather than infer connections from names.

Report observed evidence separately from hypotheses. Make the smallest
authorized correction and verify its stored result. A read-back proves saved
configuration, not runtime success. Ask for or run a scoped test only when it
is within the user's request; real integrations may fire.

Sources: [Transcripts](https://www.voiceflow.com/docs/documentation/measure/transcripts),
[Tests](https://www.voiceflow.com/docs/documentation/measure/tests).
