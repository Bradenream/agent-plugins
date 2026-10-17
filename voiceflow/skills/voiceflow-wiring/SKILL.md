---
name: voiceflow-wiring
description: Connect Voiceflow function/API tool inputs, secrets, captured outputs, and project variables; diagnose empty values or incorrect tool bindings.
---

# Wire tools and state

For questions about input collection, defaults, captures, references, or state behavior
that this skill does not answer, follow the
[docs MCP workflow](../voiceflow/references/documentation.md) before answering
or implementing. Consult it whenever unsure; do not guess from memory.

Read the [operation contract](../voiceflow/references/operations.md). Inspect the
resource declarations and the specific attachment using them. Tool definitions,
attachments, and project variables are different resources.
Read [attachment request shapes](../voiceflow/references/request-shapes.md#attach-a-function-and-capture-its-results)
when creating a binding or diagnosing an invalid target/capture payload.

For function inputs, key inputVariables by the declared input UUID, with the same
functionInputVariableID inside. For API tool inputs use apiToolInputVariableID.
Do not key by a friendly name merely because an existing attachment does.

A defaultValue can bind a project variable or secret by name. Check
unresolvedReferences after writes. Secret values belong in the secure Voiceflow
UI/connection flow, never chat or source code. Leave collection disabled for
secret-bound inputs according to the live schema.

Agent collection and defaults are distinct. Disable collection only when a
reliable default/setter exists on every incoming path; otherwise an empty value
may silently reach the integration. A default alone does not prove a value is
available.

Capture outputs explicitly into the intended project variable IDs. Output text
visible to the model is not persistent state. Each attachment has independent
bindings; changing one does not configure every playbook using the same tool.

Order dependent tool calls. Do not assume two calls in one parallel batch see
each other's captured writes. Re-read after UI edits if captures appear lost.

Prefer the smallest relevant inspection over sweeping the whole project. Verify
UUIDs, WHAT + WHEN descriptions, references, captures, and route coverage before
running anything.

Source: [References](https://www.voiceflow.com/docs/documentation/build/editor/references).
