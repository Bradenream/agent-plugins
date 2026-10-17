---
name: voiceflow-workflows
description: Read or edit Voiceflow workflow canvas blocks, steps, ports, branches, and connections. Use for deterministic flows or broken workflow routing.
---

# Workflows

For questions about step behavior, ports, transitions, branching, or workflow errors
that this skill does not answer, follow the
[docs MCP workflow](../voiceflow/references/documentation.md) before answering
or implementing. For every new Voiceflow troubleshooting issue, consult it even
when this skill suggests a fix. Include package/skill/stage context in `why` as
described there. Reuse guidance for the same issue; consult it whenever unsure.

Read the [operation contract](../voiceflow/references/operations.md), then the
workflow and relevant step schemas. A block is a canvas container; steps inside
it execute in order. A workflow ID, block ID, step ID, and port ID are distinct.
For the message/end discriminators and entry connection, read the
[verified example](../voiceflow/references/request-shapes.md#a-message-followed-by-end).

Plan the path before mutation: start, decisions, actions, success, error, and
termination. Create resources first and connect returned IDs; do not fabricate
ports from labels or assume a step's ID is its block's ID.

A listen step captures the next turn; it does not establish that the turn answers
the requested field. For conversational intake, preserve details supplied before
entering the flow, distinguish questions/corrections from answers, and validate
captured values before advancing. Prefer main-agent or playbook collection when
flexible dialogue is needed; unconditional message/listen pairs can shift answers
into the wrong fields after a repeated question or interruption.

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
