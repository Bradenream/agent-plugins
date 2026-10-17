# Docs consultation and attribution — 2026-10-16

Candidate: **0.4.1**. This is focused behavioral evidence for docs consultation
and attribution, not a completed live-onboarding or customer-resolution test.
The [structured report](2026-10-16-docs-attribution.json) preserves all 18 runs,
tool arguments/results summaries, final responses, and skill snapshot hashes.

## Method

Fresh Codex CLI 0.162.0-alpha.2 processes used normal `.agents/skills` discovery. Customer requests
did not name a skill or reveal the rubric. Models were `gpt-6-luna` and
`gpt-6.1-sol`, both at low reasoning. Each run received only the installed skill
tree, a synthetic customer request, declared tools, and explicit scope limits.
The filesystem was read-only; no account credentials, sign-in, live account
operations, or customer mutations were permitted.

A test-only stdio bridge forwarded the public Knowledge MCP's schemas and tool
responses unchanged, labeling initialization `voiceflow-plugin-eval` so these
requests can be separated from customer traffic. For setup cases, it also
exposed a clearly labeled synthetic `list_workspaces` tool returning either an
empty workspace list or a 403. This is not a test of the real account MCP or its
OAuth. The outage case deliberately failed docs tool calls while leaving
official website access available. Raw transcripts and the bridge/runner are
retained under ignored `test-results/docs-20261016/`; no private data is in this
report. Models were not asked to grade themselves.

## Failure found and correction

The first design kept the version in a separate JSON file. Across ten
exploratory runs, four Luna runs used `unknown` without opening that available
file. Strengthening the read instruction helped the duplicate-answer retest but
did not reliably fix setup and fallback runs. These are retained as attribution
failures, not overwritten by retests.

The final design puts package/version metadata at the top of the documentation
workflow itself. Reading the workflow now supplies the version without another
file lookup. Repository validation rejects drift from the plugin manifests;
standalone and native installs retain the same metadata. Missing metadata is
still explicitly `unknown`, not guessed from a remote release or CLI version.

## Final eight runs

| Scenario | Models | Observed result |
| --- | --- | --- |
| Duplicate answer already explained by a skill | Luna, Sol | Both discovered relevant skills, consulted live docs, supplied correct attribution, and labeled the fix proposed/unverified |
| Successful synthetic account read | Luna, Sol | Both reused the fixture, queried live docs with setup attribution, and explicitly kept real account connection pending |
| Workspace listing denied after sign-in | Luna, Sol | Both consulted live docs, retained setup attribution, and kept account verification pending rather than claiming docs access proved connection |
| Package metadata deliberately removed | Luna | Used `unknown`, consulted live docs, and continued useful widget troubleshooting |
| Docs service unavailable | Luna | Sent attributed request, used official website pages, disclosed fallback, and left the site fix unverified |

All **15 final docs-call attempts** carried the correct version (or intentional
`unknown`), an active skill, and the appropriate stage in `why`; each stayed
under 200 characters and kept attribution out of the retrieval question. All
seven final runs with the live docs service available consulted it. The eighth
used the expected failure/fallback path. No extra success-report query was sent.

Review also checked that weak responses led to refinement/search/page retrieval
and that final advice distinguished skill guidance from retrieved documentation.
Several first answers were weak or `answerable: false`: this is useful evidence
of retrieval gaps, not a claim the documentation independently proved the fix.
Known handoff advice still depended in part on the skill's verified workflow.

## Limits and next evidence

This is an adaptive, small regression sample, not a statistical reliability
estimate. Zero customer fixes were runtime-verified. Setup cases exercised
synthetic state and correctly did not establish live onboarding completion or
time to readiness. No user intervention happened within these bounded runs;
some final responses identified actions still needed outside the simulation.

The public endpoint accepted the attributed requests. Production log retention,
dashboard ingestion/filtering, real chat-client discovery, new OAuth, and
fresh-chat persistence were not tested. The other docs/product/widget acceptance
cases remain separate; these eight runs do not imply full coverage of them.
