# Documentation integration acceptance

Candidate: 0.4.0. Keep historical reports unchanged. The 23 earlier live product
runs did not expose docs MCP; customer KB calls are not docs calls. These new
cases define the next behavioral evaluation, not a claim that it has run.

## Give the actor a working knowledge source

Use a fresh context with only the customer request, packaged skills, fixture
state, and declared tools. Provide public docs MCP to **both** CLI and account
MCP actors. For isolated Codex runs that ignore user configuration, explicitly
add `mcp_servers.voiceflow-knowledge.url="https://www.voiceflow.com/docs/mcp"`
(or load the native plugin); configuring only the account MCP repeats the old
coverage gap. Preserve normal host approval controls.

Before starting, discover tools and make one read-only docs request as the
controller. Do not give that answer or the rubric to the actor. If discovery or
retrieval fails, label the infrastructure failure and run the fallback case
separately. Do not grade missing access as the agent choosing not to consult docs.
For offline fixtures, model the actual tool schema and a sourced response; never
turn customer KB tools into documentation tools.

## Scenarios and review

Use the `docs-*` cases in `cases.json`, plus the two setup cases
`chat-add-docs` and `chat-docs-fallback`. Include a direct specialist invocation
that skips the router, a question outside existing skill detail, an unfamiliar
error, a change/deprecation question, exact code retrieval, and docs failure.
Run standard and low-power/low-reasoning models separately when commissioned.
Keep expected answers and fixture implementation out of the actor's context.

Evaluate actual calls and resulting answers/changes, not a statement that the
actor consulted documentation. For each unresolved product question record:

- Whether docs were available and which tool/schema the actor discovered.
- The question, retrieved section/citation, and whether they resolve the issue.
- The implementation or answer that used the evidence; preserve contrary evidence.
- Whether docs were consulted before the unsupported recommendation or write.
- Whether irrelevant calls, repeated lookups, fabricated citations, unnecessary
  OAuth, customer-data disclosure, or customer KB misuse occurred.

One sufficient answer is better than many irrelevant calls. Do not reward a
quota or penalize reuse of a current answer already retrieved for the same task.
Missing source support must remain an explicit uncertainty, not a claimed feature.
An official website/CLI fallback may pass only when MCP is unavailable; record
that path separately. Keep live account writes outside these docs-only cases.

## Evidence boundaries

Package checks verify all skills/references and both native/portable server
configurations ship. Setup fixture tests verify independent account/docs state,
no-auth connection, discovery, and fallback behavior. A live read-only server
probe verifies schemas and successful public retrieval. None alone proves model
behavior, widget installation, or account authorization. Store raw transcripts
under ignored `test-results/` and commit only sanitized results.
