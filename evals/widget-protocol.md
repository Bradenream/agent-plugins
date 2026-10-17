# Widget acceptance protocol

Candidate: 0.3.0. Added 2026-10-16. The `widget-*` entries in `cases.json` are
acceptance specifications, **not completed model runs**.

## What the repository checks cover

- The new skill is discoverable from the router; linked references ship with
  the installed skill tree, plugin archive, and generated website payload.
- The real released CLI accepts the documented commands. `scripts/verify_cli.py`
  sends requests only to a localhost fixture with a fake credential, checking
  settings GET, both snippet versions, and the JSON-stdin PATCH contract.
- Structural/package tests do not prove an agent follows the guide or a hosted
  website correctly renders the real widget.

## Behavioral evaluation

Run a fresh assistant for each case, with only its user request, fixture data,
skill entrypoint, and advertised tools. Keep the required/forbidden assertions
out of the actor's context. For chat-only cases, provide document reading and
account MCP but no terminal or website editor. For source-editing cases, use a
disposable site checkout and mock management tools. Do not grant bypass access.

Evaluate the actual tool calls, resulting settings/site diff, and final handoff.
Require preserved unrelated settings, correct version targeting, and accurate
completion claims. Test a low-power/low-reasoning model as well as the standard
model; record model, effort, skill commit, fixture, and failures independently.
Do not count a rewritten answer or a post-failure retest as an initial pass.

## Live verification, when scoped and authorized

Use a synthetic agent/environment and disposable or staging website. State
whether the site is publicly reachable before choosing a draft snippet. Never
use repository tests/CI to sign in, publish, or mutate customer accounts.

Start with HTML and Next.js to test actual rendering and client lifecycle, then
Webflow and a chat-only guided install. Extend to every builder before claiming
its live integration is tested. Each platform should exercise its own save and
publish behavior, visitor URL, mobile layout, navigation, and removal path.

Use a synthetic greeting/echo agent with no external integrations. Check a real
reply, not only a visible launcher. Inspect settings read-back, the generated
snippet, and observed runtime target. Repeat the color change in a draft and
confirm the published widget remains unchanged until the authorized publication.
Check the complete pending diff before publishing anything.

For client-routed sites, include cold deep links, route changes, Back, reload,
slow SDK loading, remounts, and expected persistence. For an authenticated site,
use synthetic users to test logout/account switching. Record whether the SDK
loaded once and whether exactly one active widget remained.

For a chat-only assistant, verify it does the Voiceflow portion itself, supplies
the real snippet and one platform's instructions, and resumes browser checks
after the user saves. It must not claim installation based on a user saying
"done" or on a successful snippet response.

Keep raw captures in ignored `test-results/`. Commit only sanitized evidence
with per-case outcomes and explicit unrun platforms. No phone-number work is
part of this protocol.

## Documentation access

For runs of 0.4.0 or later, provide the public docs MCP alongside each actor's
account/site tools, including chat-only actors. Follow [docs acceptance](docs-protocol.md).
Check use of current widget docs for questions beyond the skill, and official
platform docs for site-editor/plan behavior. A local guide or an account schema
alone is not evidence of looking up an unresolved widget behavior.
