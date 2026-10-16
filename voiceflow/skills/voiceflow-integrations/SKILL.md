---
name: voiceflow-integrations
description: Connect Voiceflow integrations, API tools, MCP tools, and secret-backed credentials. Use for external services or missing tool connections.
---

# External services

Read the [operation contract](../voiceflow/references/operations.md). Inspect
available integrations and their schemas before writing a custom API/function.
A connection is not an attached agent tool: verify both.

Use an existing integration when it supports the task; an API tool for a plain
request; a function for logic; an MCP tool for a supported remote capability.
Do not confuse the coding agent's Voiceflow MCP connection with an MCP server
that the customer is adding to their Voiceflow agent.

The user completes third-party OAuth or enters secret values in the secure
Voiceflow interface. Never request credentials in conversation. If the public
API cannot establish a connection, give the precise remaining UI step, then
resume inspection after it exists. Don't invent a private connection helper.

API-tool fields reference the tool's declared input variables. Bind project
variables or secrets through defaults on each attachment, not by assuming a
URL token can read all project state. Use [wiring](../voiceflow-wiring/SKILL.md).

Secret names may be shared while values differ by environment. Publishing
does not promote Draft credentials to Default credentials. Check whether a
value exists without retrieving or printing it.

A configured request is not proof of a successful integration. Inspect schemas
and bindings first; when authorized to test, choose a harmless read if possible.
Never send an email, payment, deletion, or other side effect solely to validate
connectivity.

Sources: [API tool](https://www.voiceflow.com/docs/documentation/build/tools/api-tool),
[Secrets](https://www.voiceflow.com/docs/documentation/build/data/secrets).
