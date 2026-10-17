---
name: voiceflow-voice
description: Configure or improve Voiceflow agents for spoken conversations, voice settings, turn handling, and phone interactions.
---

# Spoken conversations

For questions about voice providers, turn handling, interruptions, telephony, or transfer behavior
that this skill does not answer, follow the
[docs MCP workflow](../voiceflow/references/documentation.md) before answering
or implementing. For every new Voiceflow troubleshooting issue, consult it even
when this skill suggests a fix. Include package/skill/stage context in `why` as
described there. Reuse guidance for the same issue; consult it whenever unsure.

Read the [operation contract](../voiceflow/references/operations.md). Identify the
channel and current voice/provider settings before editing. Use supported
provider values from live schemas; never invent a voice ID.

Prefer short spoken turns, one question at a time, and explicit confirmation for
ambiguous names, dates, amounts, and identifiers. Do not read Markdown, URLs, or
long lists verbatim. Preserve already-known context instead of restarting the
conversation after routing.

Separate prompt problems from transcription, endpointing, interruption, silence,
and telephony configuration. Use a specific transcript/trace to identify which
layer failed. A successful text test does not establish audio quality or phone
routing correctness.

Phone-number assignment and outbound calls can affect real people and billing.
Only perform them within the user's explicit task. Inspect configuration before
placing calls. Custom traces or transfer payloads require the documented runtime
contract; do not assume a chat trace works in telephony.

Use [functions](../voiceflow-functions/SKILL.md) for custom transfer logic and
[evaluations](../voiceflow-evaluations/SKILL.md) for scoped voice testing.

Source: [Voiceflow documentation](https://www.voiceflow.com/docs).
