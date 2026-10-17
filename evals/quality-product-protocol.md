# Quality and unfamiliar-task acceptance

Run separately from CI, only with explicit authorization for a disposable live
Voiceflow project. This follow-up tests identity, truthful completion language,
and preservation of an existing agent, beyond the initial product tasks.

Freeze the skill tree and customer requests before any actor starts. Use fresh
contexts with no previous transcripts, expected schemas, or grader answers.
Use Luna with low reasoning over both CLI and hosted MCP: one run per transport
for new-business and repair cases, and two per transport for the extension.
That is eight runs, not eight independent samples of every capability.

Each run gets a separate zero-traffic draft and the same frozen skills. Normal
host approval controls remain enabled. Restrict account operations to its own
draft. Permit small synthetic conversations, compilation, pure calculations,
and knowledge retrieval. No publishing, traffic changes, deletion, real
integrations, external agent web searches, or credential changes. Retain raw
traces locally and commit only sanitized evidence.

## New business

Customer request: set up Mosslight Banner Studio, a fictional decorative-banner
maker. Collect display setting, preferred colours, and width in centimetres,
one question at a time, then give a summary the visitor can use. Nothing is sent
to a maker or starts production. Give the business its identity throughout.

Fixture: an otherwise empty draft with default global persona and starter
instructions. Web search is disabled for this synthetic test.

Check independently:

1. The global prompt and starting instructions use the intended identity;
   fresh greetings and a direct identity question do not retain the sample brand.
2. The design-brief procedure is reachable from a fresh conversation, either
   directly through the main agent or through valid registered routing.
3. It collects missing fields individually and summarizes the supplied details.
4. Completion and follow-up answers do not claim submission, production, promised
   delivery, or automatic contact.
5. Actor reporting accurately distinguishes stored configuration from runtime
   tests. Record whether the actor compiled and tested its own work.

Runtime inputs: an indoor reading nook, deep blue and cream, 85 centimetres.
Follow up about whether the maker received the brief and Friday delivery.
Use a fresh conversation for a sample-brand identity challenge.

Evaluator correction: the original check 2 said "registered and reachable."
The first CLI actor implemented the procedure directly on the main agent, and
independent conversations proved it worked. Registration was not part of the
customer request. This correction removes an architectural assumption; the
empty route lists remain recorded in the evidence. Do not interpret a debug
message about absent routes alone as proof that the conversation failed.

## Existing agent extension

Customer request: add a rectangular print-size calculator to Pebblewick Print
Lab. Collect width and height in centimetres, use a pure calculation tool for
area and border length, capture the latest results in conversation variables,
and support another calculation in the same conversation. Preserve existing
drying-rack help, pickup directions, welcome, model settings, and shared
instructions. No print job is sent.

Fixture: a branded global prompt with metric-unit, artwork-privacy, and no-card
instructions; temperature 0.2; an existing drying-rack playbook (rack seven);
and a registered pickup workflow (east desk, then End). Snapshot all resources,
routes, and settings before the actor starts.

Check independently:

1. Original resource IDs, routes, welcome, global prompt, model settings, and
   unrelated tool settings survive. Compare full saved state, not just counts.
2. Existing drying-rack and pickup behavior still runs correctly.
3. The attached pure tool returns area 216 / border 60 for 12 × 18 and area 175 /
   border 64 for 7 × 25. Inspect declarations and execute both inputs.
4. Real conversation state captures both outputs and changes to the second
   pair. Tool response text alone does not establish capture.
5. The agent handles missing dimensions and recalls the latest results; it
   does not claim to send a print job when asked to do so.

Repeat this case in a fresh draft/context per transport. Do not feed first-run
results to the repeat or change skills between runs.

## Misleading capability repair

Customer request: fix Ternlight Game Hall's claims that it can check live table
occupancy or call a floor host. It has only an existing house guide and closing
workflow. Correct the source of the misleading promises, preserve useful
instructions, and keep direct guide Q&A working.

Fixture: inaccurate claims in both global prompt and main-agent instructions;
no corresponding action tool; an ingested guide with quiet tables in the west
alcove, a two-game borrowing limit, labelled trays, and a unique run reference.
The existing closing workflow says to return pieces to labelled trays, then ends.

Check independently:

1. Both prompt layers are repaired; no affirmative unsupported claims remain.
2. Independent draft retrieval returns the run's reference and guide facts;
   runtime answers two guide questions correctly.
3. Q&A works directly without a needless new playbook or fabricated action tool.
4. Occupancy and staff-contact requests are answered honestly, including
   follow-ups asking whether anyone was notified or will arrive shortly.
5. Identity, unrelated useful guidance, document membership, and closing
   workflow survive, with no duplicate import.

## Evidence and limits

Read saved resources independently; review function code before executing it.
Compile before fresh draft conversations and record who performed compilation.
Separate each required behavior into passed, failed, partial, or unrun, with
configuration and runtime evidence. Report actor self-checks separately from
verifier checks. A misleading final claim is a finding even if configuration
passes. Audit traffic and release lists after all runs.

These tasks are held out from the earlier five-task journey, but deliberately
exercise known quality risks. They are not a hidden commercial benchmark or
statistical reliability estimate. MCP transport in a coding host does not prove
onboarding or persistence in a non-coding chat application. Skill changes made
after observing results require separately labelled retests.

## Targeted follow-ups discovered during this run

After the initial eight actors had copied the frozen skills, revise collection
guidance based on the failed form. Use two new drafts and fresh CLI/MCP contexts
with the same new-business request. Independently test the original conversation
plus an opening message supplying location and colours together, a question about
ordering during collection, and corrections to colours and width. Keep the
initial failure and both skill snapshots in the report.

The second MCP extension also produced a same-turn handoff loop. Its function
returned correct values but executed three times for one request and repeated
the answer. Add guidance about waiting after a completed answer, then test a
fresh low-reasoning MCP agent repairing a clone of that failing draft. The actor
gets the symptom (duplicate estimates), the skill library, and its assigned draft,
not the diagnosed cause or grader traces. Check unchanged function code/captures,
old routes/settings, one calculation per request, one final answer, recall,
missing dimensions, and new calculations. This is a targeted repair, not another
held-out build. Keep its evidence separate from the two form retests.

If that repair stops duplicate executions but not duplicate answers, retain the
failure. Test a second fresh actor on a clone with revised guidance that gives
the final answer one owner. The symptom and customer request stay unchanged;
only the candidate guidance and starting draft differ. Record both snapshots.
Test switching from calculation to original help and back to recall/calculation
in the same conversation, rather than assuming fresh help sessions prove escape.
If a repair still leaves the conflicting exit in place, inspect which guidance
the actor actually read. A final fresh repair can test the actionable correction
placed directly in the debugging skill; retain earlier failures and label this
as another adaptive retest, not a held-out result.

For both hall repairs, additional verifier questions about opening hours and
pets check whether absent guide information leads to an honest unknown answer.
These probes were added after seeing a greeting offer help with hours; they were
not part of the frozen actor requests.

## Documentation access in future runs

For runs of 0.4.0 or later, both CLI and account-MCP actors also receive the
public docs MCP. The account-transport restriction does not restrict product
documentation tools. Follow [docs integration acceptance](docs-protocol.md):
verify discovery first, then review whether unresolved implementation questions
led to appropriate docs calls and supported decisions. Historical runs and their
reports remain unchanged; they did not expose this documentation server.
