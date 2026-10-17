---
name: voiceflow-build
description: Build or extend Voiceflow agents and playbooks, choose the right architecture, and connect routing and tools. Use after the user describes what they want to build.
---

# Build an agent

Read the [operation contract](../voiceflow/references/operations.md). Resolve the
user's intended project and environment from context; clarify only missing
choices. A build request authorizes its necessary draft work, not publishing.

Keep knowledge-only Q&A on the main agent. Use a playbook for a distinct
multi-step job needing its own tools or procedures; a workflow for deterministic
branching or ordered steps. Avoid creating a playbook solely to wrap the KB.

Separate three instruction layers: global identity/style/guardrails, main-agent
routing, and playbook job instructions. Playbooks inherit the global prompt;
they do not see each other's private instructions.

For a new agent, align the global identity and starting message with the user's
business instead of leaving sample-company text. A playbook can collect and
summarize a request without submitting it anywhere. Do not promise submission,
booking, or human follow-up unless an actual configured action supports it.

Build in dependency order: agent context, playbook, required resources, tool
attachments, then instructions referencing those attached tools. Every attachment
and routing description must say both WHAT it does and WHEN to use it.

Read the complete existing routing registry before updating it: a supplied
playbooks/workflows list replaces the list. Keep existing entries and a valid
entry route. Never leave both registries empty during a migration.

Use returned IDs. Confirm write results, unresolved references, tool descriptions,
and routing before reporting the draft ready. Do not run tools that contact
external services merely to inspect configuration.

Read [prompting](../voiceflow-prompting/SKILL.md) for instructions and
[wiring](../voiceflow-wiring/SKILL.md) before attaching functions/API tools.
Source: [Playbooks](https://www.voiceflow.com/docs/documentation/build/playbooks).
