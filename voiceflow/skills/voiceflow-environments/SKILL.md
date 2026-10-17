---
name: voiceflow-environments
description: Resolve Voiceflow environment aliases and drafts, clone environments, compare changes, and manage explicitly requested merges or publishing.
---

# Environments and release actions

For questions about draft/live behavior, cloning, shared resources, merges, or publishing
that this skill does not answer, follow the
[docs MCP workflow](../voiceflow/references/documentation.md) before answering
or implementing. Consult it whenever unsure; do not guess from memory.

Read the [operation contract](../voiceflow/references/operations.md). Resolve the
project and environment from live data. An environment alias, environment ID,
and version ID are different. Draft-editing operations use the alias required
by their schema. Never silently choose Main because it is the default.

Each environment has draft and live content. A user can mean unpublished draft
changes when asking to clone; inspect clone options and source version. Do not
publish merely to make a clone include recent edits.

Compile draft edits before a conversation test: use the environment's `compile`
operation, check its result, and start a fresh draft conversation. This refreshes
the runtime representation without publishing. See the
[verified compile sequence](../voiceflow/references/request-shapes.md#compile-before-a-draft-conversation-test).

Environment isolation has limits: knowledge document bodies and evaluation
resources can be project-shared; secret names are shared while values are
environment-specific. Cloning can copy secret values and does not isolate
external services.

Publishing content does not promote Draft secret values to Default values.
Discarding or reverting content does not undo credential changes. A merge may
preserve Main's secret values or override them depending on options; inspect the
actual behavior before proceeding.

Publish, merge, deletion, and traffic changes require scope from the user.
Read the current diff/state and explain the concrete effect before an approval
when authorization is missing. Protected environments may restrict these actions
to admins/owners. Do not bypass protection.

After an authorized release action, verify the resulting status/version and
report what became live. A saved draft is not a deployment.

Source: [Environment overview](https://www.voiceflow.com/docs/documentation/deploy/environments/overview).
