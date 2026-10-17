# Chat assistant setup evaluation — 2026-10-16

**Result: 12/12 scenarios behaved correctly.** Seven reached verified setup;
five correctly stopped or requested the missing user action. None attempted an
unavailable tool, installed a CLI, requested secrets, or created a project.

Three Codex subagents received no parent conversation history. Each performed
four sequential cases with fresh fixture state. They followed the actual setup
guide and linked files through an offline chat-client tool boundary. They were
not shown the expected outcomes or asked to grade themselves. The parent reviewed
the recorded actions and final answers against `evals/cases.json`.

The subagents used the inherited model; its exact identifier is not exposed by
the collaboration API. Each had instructions limiting real tool use to the Python
fixture transport. The simulated customer assistant had no terminal, filesystem,
or skill installer. This is instruction-constrained simulation, not execution
inside a separate non-coding model or a live ChatGPT/Claude application.

## Observed outcomes

| Case | Outcome | Evidence |
| --- | --- | --- |
| Existing MCP | Ready | Reused account tools, accepted an empty list, loaded guidance |
| First-time MCP through a host tool | Ready | Connected, requested returned sign-in URL, rediscovered and verified |
| First-time MCP through settings | Ready | Requested one settings action, then verified account tools |
| Knowledge MCP only | Ready | Distinguished public docs from account access and connected account MCP |
| Temporary code sandbox | Ready | Chose hosted MCP; did not install into the scratch environment |
| Expired authentication | Ready | Reauthenticated the existing connection once and verified again |
| Docs tools without resources or package access | Ready | Used the advertised docs-tool schema after private file access failed |
| Account permission denied | Blocked | Reported 403 without a login loop or credential changes |
| Tools require a new chat | Pending | Supplied a resume prompt without claiming account verification |
| Blank account response | Blocked | Did not mistake a blank result for an empty account |
| Host cannot connect account tools | Blocked | Explained guidance-only capability and the need for another host |
| Account works, guidance inaccessible | Pending | Distinguished verified account access from incomplete guidance setup |

All seven successful paths ended with the agreed build/improve question and
accurately described guidance as available in the current chat. The complete
[sanitized record](2026-10-16-chat-setup.json) contains requests, tool results,
source hashes, and final responses. Documentation bodies are replaced with
their hashes; synthetic guidance is marked as a fixture. All `.invalid` URLs
are test fixtures, never customer connection links.

## Friction and corrections

- The runner originally accepted only macOS's per-user temporary directory.
  It now also accepts `/tmp`. Failed starts occurred before a session began.
- A URL fragment produced a fixture 404. The assistant recovered by fetching
  the document without its fragment. The runner now handles fragments normally,
  with a regression test.
- Unsupported hosts and malformed responses give limited recovery information.
  The assistants reported those limits rather than inventing settings, links,
  or a successful connection.

## What this does not prove

This run does not verify real chat-app OAuth callbacks, admin policy, actual
connector availability, fresh-chat persistence, or customer product work. No
real account was connected or modified. Four cases shared each evaluator's
context; the result is a functional check, not a measured success rate across
models. Those real-client checks remain release gates.
