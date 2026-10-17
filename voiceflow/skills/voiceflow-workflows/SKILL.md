---
name: voiceflow-workflows
description: Read or edit Voiceflow workflow canvas blocks, steps, ports, branches, and connections. Use for deterministic flows or broken workflow routing.
---

# Workflows

Read the [operation contract](../voiceflow/references/operations.md), then the
workflow and relevant step schemas. A block is a canvas container; steps inside
it execute in order. A workflow ID, block ID, step ID, and port ID are distinct.
For the message/end discriminators and entry connection, read the
[verified example](../voiceflow/references/request-shapes.md#a-message-followed-by-end).

Plan the path before mutation: start, decisions, actions, success, error, and
termination. Create resources first and connect returned IDs; do not fabricate
ports from labels or assume a step's ID is its block's ID.

When a mutation accepts expectedSteps, pass the current ordered step IDs.
On a conflict, re-read and reconcile once rather than retrying stale state.
Inserting, splitting, moving, and deleting steps can change ownership or ports;
read back the affected blocks and links after the edit.

Link the actual branch/exit port to the target block using the live schema.
Playbook steps must use the playbook's declared exit paths. Check every expected
branch, including default/no-match, rather than only the happy path.

Messages and prompts are separate resources in relevant step schemas. Create
or reuse them through their supported operations; don't insert a guessed text
field into a step payload.

Verification starts with read-back topology and reference checks. A runtime
test can invoke real integrations; scope it with [evaluations](../voiceflow-evaluations/SKILL.md)
only when the user requested testing.

Source: [Workflows](https://www.voiceflow.com/docs/documentation/build/workflows).
