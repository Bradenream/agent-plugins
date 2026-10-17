# Quality and unfamiliar-task acceptance — 2026-10-16

The identity and unsupported-promise fixes held up in live conversations.
Six of eight initial scenarios met the tested acceptance requirements.
Two exposed additional problems: a rigid form misplaced answers,
and a calculator repeated answers and tool calls. Both collection retests passed.
The handoff defect required three fresh repair attempts; the third passed the
independent checks. Both original failures and the first two failed repairs
remain in the evidence.

This is a follow-up to the [first live acceptance run](2026-10-16-live-product.md),
using unfamiliar customer tasks rather than the earlier appointment/order journey.
It is regression evidence, not a reliability percentage or a launch certification.

## Method

- All authoring actors used **gpt-6-luna with low reasoning**, fresh ephemeral
  contexts, copied skill libraries, and normal automatic approval review.
  These settings describe the authoring agent; the created Voiceflow agents
  used their saved runtime model settings, including `voiceflow-core-4.2`.
- Host: Codex CLI `0.162.0-alpha.2`, macOS `26.4`. Account surfaces: Voiceflow
  CLI `0.287.0` and the hosted account MCP. CLI reused native OAuth; MCP reused
  the sign-in the user completed for the earlier run. No credentials were copied.
- Baseline repo commit: `5b810d89706b7ccadaf71d87a661afca2e3d1335`. All candidates
  are development snapshots of package **0.2.2**, not separate public releases.
  Eight actors copied snapshot A before follow-up edits. Two collection retests
  used B; sequential handoff repairs used C, D, and E. Source hashes accompany each run.
- Each actor received a customer request, its own synthetic draft, the library,
  and scope restrictions. Customer requests contained requirements or symptoms,
  not expected outputs or diagnosed causes. Actors did not receive previous
  transcripts or grader files; later skill snapshots intentionally contained
  generalized diagnoses and corrections derived from observed failures. Existing-agent
  extension was repeated twice per transport, each in a fresh seeded draft.
- The verifier independently read saved resources, inspected pure function code,
  executed calculations, compiled drafts, and ran conversations with fresh users.
  Calculations were checked against actual conversation state, not answer text
  alone. Retrieval included a unique synthetic guide reference.

The [protocol](../quality-product-protocol.md) records fixtures, criteria, and
follow-up probes. Local raw traces remain ignored. The committed
[evidence](2026-10-16-quality-product.json) contains sanitized conversations,
resource comparisons, tool bindings, source hashes, and raw-evidence hashes.

## Initial eight runs

| Case | CLI | MCP | Independent evidence |
| --- | --- | --- | --- |
| New business: banner design brief | Pass | **Fail: collection** | Both global prompt layers and greetings use Mosslight, and neither promises production or delivery. MCP's form places answers in the wrong fields. |
| Existing print calculator, first run | Pass | Pass | Two calculations and missing-dimension recovery; latest values captured; existing rack/pickup routes preserved. |
| Existing print calculator, repeat | Pass | **Fail: repeated answers/calls** | Math and captures work on both; the MCP agent runs the first calculation three times and repeats its answer. |
| Repair unsupported hall capabilities | Pass | Pass | Both prompt layers repaired; guide retrieval and Q&A work; occupancy/staff promises removed; closing workflow preserved. |

Initial actor durations ranged from 68 to 406 seconds. They include discovery
and approval overhead and exclude fixture preparation and independent checks.
Every actor compiled and ran at least one conversation itself. Those self-checks
did not catch every issue; they are recorded separately from verifier checks.

### Identity and truthful completion

The new-business actors changed the actual global `prompt` and main-agent
`instructions`, not just a playbook name. Fresh greetings identified Mosslight;
the sample-brand challenge was rejected. Completion and follow-up answers said
the brief had not been sent, production had not started, and Friday delivery
could not be promised. The calculator drafts similarly denied sending print jobs.

Both hall repairs removed live-occupancy and staff-notification promises from
both prompt layers. Independent retrieval found the original unique guide,
and conversations answered west-alcove and two-game questions correctly.
Neither repair added a duplicate document or needless Q&A playbook. The existing
closing workflow still returned its exact text and ended.

The CLI repair actor noticed unsupported location detail in its own first test
and tightened knowledge-source instructions. It explicitly reported that its
last correction had not been rerun; the verifier tested that final saved version.
A greeting still offered help with opening hours, which were absent from the
guide. Added questions about hours and pets produced honest unknown answers in
both repairs. This supports factual restraint in the tested answers, not perfect
greeting copy or a universal hallucination claim.

### Collection failure and retests

The first MCP actor built an unconditional message/listen sequence. It ignored
the hanging location already supplied in the initiating request, asked again,
then captured colours as location, width as colours, and a question as width.
It displayed that malformed summary and ended the workflow. A later main-agent
reply corrected the summary, but that does not make the failed completion pass.

The revised skills distinguish flexible conversation from deterministic steps:
retain supplied details, ask only what is missing, and handle questions or
corrections instead of treating every next turn as a valid field answer.

Fresh CLI and MCP retests both passed the original brief and identity checks.
They also passed an added interruption case: location and colours in the opening
request, a question about ordering, replacement colours with a width, then a width
correction. Both retained the kitchen location and ended with green/cream and
95 centimetres, without claiming an order. These two targeted retests took 78
and 48 seconds; they are not new held-out generalization samples.

The first CLI build and both retests used the main agent directly. The original
rubric unnecessarily said the procedure must be "registered and reachable."
It was corrected to accept a reachable main-agent procedure: the customer never
required a playbook or workflow. Empty registries and that rubric correction are
recorded. CLI help/debug warnings about no routes did not prevent these actual
conversations from working.

### Existing-agent preservation and handoff defects

All four extension actors retained the global persona, model/voice settings,
unrelated tools, original route entries, original drying playbook, and pickup
workflow. Main routing instructions changed to include the requested calculator.
Pure executions produced area/border pairs **216/60** and **175/64**. Independent
conversation state changed to the second pair, and a missing dimension was
collected before calculating **99/40**. Recall and both old help routes worked.

The second MCP extension nevertheless produced three distinct estimate messages
and three real function executions for one visitor turn. This was a same-turn
handoff loop, not duplicated transport delivery. Its playbook instructed a return
to main after answering; main could route the still-current request back.

A fresh low-reasoning MCP actor repaired a clone using snapshot C. It stopped
the repeated function execution in verifier checks, but the playbook and main
still produced duplicate final answers, including recall. **That first repair
failed the one-answer criterion.** Its own smaller conversation check had not
reproduced the duplication. Correct math and a single tool call were insufficient.

Snapshot D makes answer ownership explicit: if the playbook answers, it waits
for new visitor input and hands off when a new request needs another capability.
If main is to answer, the playbook does not first deliver that same answer.
Debug/evaluation guidance now checks responses, executions, and handoffs together.

The second fresh repair (D) passed the first independent sequence but duplicated
an estimate in an additional same-session route-switch test. **It also failed.**
Both repairs left the playbook's unconditional return instruction intact.
The second actor read the debug skill but did not follow its link to prompting.
Snapshot E therefore puts the corrective rule directly in debug, alongside
same-session routing checks, while preserving legitimate workflow exits.

The third fresh actor (E) removed the conflicting exit from the playbook. Its
71-second run kept calculation code, declarations, tool bindings, captured
variables, identity, model settings, and original help resources intact.
Independent checks then found one answer per request and one tool execution
per new calculation, with no execution for recall. The original calculation,
missing-dimension, honesty, and help checks passed.

An additional fresh conversation exercised calculation → drying advice → recall
→ another calculation → recall → pickup. It returned **104/42**, rack seven,
the same recalled pair, **24/20**, the new recalled pair, then the exact east-desk
message and End. Each turn had one answer; only the two calculations ran the
function. This tests switching out of an active calculator, which fresh help
sessions alone could not establish. The finite passing checks do not prove that
intermittent duplication can never recur.

| Follow-up | Result |
| --- | --- |
| New-business CLI, snapshot B | Pass, including interruptions and corrections |
| New-business MCP, snapshot B | Pass, including interruptions and corrections |
| Handoff repair 1, snapshot C | Fail: duplicate answers remain |
| Handoff repair 2, snapshot D | Fail: additional route-switch probe repeats an answer |
| Handoff repair 3, snapshot E | Pass in independent original and route-switch probes |

## Scope and interpretation

Thirteen low-reasoning authoring runs used thirteen separate drafts in the
disposable project in the user-selected workspace. Final audit found zero
traffic on every draft, unchanged release lists, and unchanged agent
configuration in the Main environment. No publishing, merging, deletion, traffic changes, or out-of-scope
project/environment operations were observed. Raw traces, source snapshots, and
failed drafts are retained for review; no test resources are silently deleted
to improve the result. All 32 repository tests, package validation/build, and
validation of the 15 skill files passed. CI does not run these live evaluations.

State-equality booleans in the evidence are observations, not automatic pass/fail
grades. Updating identity in a new build or fixing misleading instructions must
change those fields. The first new CLI build also disabled an empty knowledge
tool and removed unused web-search metadata while leaving web search disabled.
The hall CLI repair tightened its knowledge tool description. All four extension
runs preserved their unrelated settings and original resources exactly.

Transient problems remain visible: CLI sandbox access to the existing keychain
session required normal approval; some requests needed corrected selectors or
argument shapes. No personal access token workaround or approval bypass was used.
The controller used bounded external timeouts; empty command output was not
accepted as proof of a successful write. Recorded nonzero command chunks can
include multiple commands, so their count is not an API error-rate metric.

These are short synthetic conversations with pure functions and small guides.
The tasks were unfamiliar relative to the earlier test, but deliberately cover
known risks. Follow-up tasks were selected after failures. Results do not prove
production integration behavior, long sessions, broad model reliability, or
real ChatGPT/Claude/Cursor onboarding and fresh-chat persistence. MCP was real,
but hosted inside Codex with local guidance access. Those client acceptance
checks remain the next release gate.
