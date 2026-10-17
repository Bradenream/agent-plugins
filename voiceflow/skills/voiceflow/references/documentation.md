# Answer product questions with the docs MCP

Skills supply the workflow; Voiceflow's website documentation supplies current
product knowledge. For **any Voiceflow how-to, capability, setting, API/CLI,
or error question that the relevant skill does not answer**, consult the docs
MCP before answering, choosing an implementation, or changing configuration.
Do this for your own implementation questions as well as the user's questions.
Also consult it when a skill appears stale, evidence conflicts, or you are unsure.
A source link at the end of a skill is a starting point, not a substitute for
retrieving the answer. Reuse relevant retrieved guidance within the same task;
there is no need to repeat a lookup for every command or fetch an entire manual.

## Choose the documentation tool

Discover the host's actual tool names and input schemas, including deferred
tools. The server is the public **Voiceflow Knowledge MCP** at
`https://www.voiceflow.com/docs/mcp`, with Streamable HTTP and no authentication.
Host prefixes vary. Prefer this server over general web search or remembered
product behavior whenever it is available.

| Question | First tool |
| --- | --- |
| How do I do this? What does this setting mean? How does this API/CLI behavior work? Why this error? | `ask_voiceflow` |
| Find candidate pages, compare approaches, or refine a weak answer | `search_voiceflow` |
| Need the exact example, configuration fields, table, or a cited section | `read_voiceflow_page` |
| What's new, deprecated, removed, or replaced? | `get_voiceflow_changelog` |

Fill required arguments from the live schema. Current tools require `initiator`
(`human` for the user's question, `agent` for your own implementation question),
`purpose` (`answers` for a specific question, `research` for broader exploration),
and `why` (a short description of the task). Ask a focused question in English,
then answer the user in their language. Include relevant product terms and
channel/version context; omit credentials, personal details, customer transcripts,
and private source. These public tools do not need account IDs or tokens.

If the answer is weak, reports `answerable: false`, or points to a better
term/page, refine the question or read that section. A successful tool response
does not necessarily answer the question. Inspect the evidence and apply it;
a token search followed by an unsupported answer does not resolve the question.
Cite the returned documentation URL when explaining product behavior. For an
implementation, use the documented approach and verify the result separately.

## Keep the three sources distinct

- **Skills:** task workflow, preserved state, verification, and scope.
- **Docs MCP:** current product behavior and how-to guidance, including the
  widget, API, CLI, and account MCP. Resources such as `voiceflow://skill` can
  supplement guidance if advertised; resource access is not required.
- **Account MCP / CLI:** the user's actual state and exact operation schemas.
  Inspect live schemas or installed CLI help for arguments before executing.

The account's knowledge-base query tools search the customer's agent content;
they are not the Voiceflow docs MCP. Do not use customer KB queries to learn
Voiceflow. A docs answer cannot verify account access, saved changes, or runtime
behavior. If docs conflict with a skill or tool schema, investigate the specific
discrepancy; do not guess fields or use failed writes to discover a contract.

## If docs MCP is unavailable

Check discovery first. Reuse or connect it through the host-supported
[docs connection path](../../voiceflow-setup/references/mcp.md#documentation-connection)
when available; never require OAuth for this public server. If the host cannot
expose it, or the service fails, use the public Voiceflow website docs or
`vf docs search "<question>" -o json` / `vf docs get <page>` through an available
CLI. Inspect that CLI's help; do not install it solely to answer a docs question.
For temporary failure, allow one bounded retry, respecting retry hints, then
use the fallback. Avoid repeated reconnection or searching unchanged terms.

State the fallback briefly when relevant. If no authoritative source answers the
question, say what is unresolved, complete independent work, and ask only for
missing customer context; do not turn an assumption into a product guarantee.
For another platform's own editor, plans, or deploy behavior, use that platform's
official docs in addition to Voiceflow guidance.

Source: [Knowledge MCP](https://www.voiceflow.com/docs/mcp/knowledge).
