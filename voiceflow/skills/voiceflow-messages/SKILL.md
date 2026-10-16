---
name: voiceflow-messages
description: Create or edit reusable Voiceflow messages, prompts, and text referenced by workflow steps or tool messages.
---

# Messages and reusable prompts

Read the [operation contract](../voiceflow/references/operations.md). Distinguish
literal message content, a reusable prompt resource, an agent's instructions,
and a workflow step that references one of these.

Read the resource and its consumers before replacing it. Shared text changes can
affect multiple paths. Preserve variants, variable bindings, channel-specific
content, and unrelated fields.

Use current message/prompt operation schemas. Do not guess whether a step
expects raw text, a message ID, or a prompt ID. Create dependencies first and
attach the returned ID. For a local edit, prefer a supported targeted update.

Keep generated-answer instructions separate from exact text the agent should
say. Check variable references and behavior when values are missing. Voice text
should sound natural aloud; chat may include formatting inappropriate for speech.

Read back the referenced resource and owning step/tool after changes. Verify
the intended path uses the edited resource, rather than creating an unused
duplicate and claiming the user-facing text changed.

Source: [Instructions](https://www.voiceflow.com/docs/documentation/build/instructions).
