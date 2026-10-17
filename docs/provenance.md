# Sources and adaptation

Reviewed 2026-10-16.

## Product knowledge

The Voiceflow website documentation is the product authority. The initial audit
used the website's current docs for CLI, MCP, playbooks, workflows, function/API
tools, references, secrets, knowledge, transcripts, evaluations, tests, and
environments. Each specialist skill links its relevant public documentation.

The current Creator skill library was reviewed at revision
`811c78c61b6c50df69922bf686de12c5779a2cdf`. Its thirteen customer-facing
specialties informed the portable workflows. The internal coach skill was
excluded. Private helper calls, implicit in-app page context, UI suggestion
protocols, and internal tooling dependencies were removed. These are concise
new customer-facing instructions, not a vendored copy of private source files.

Where an older skill conflicted with current website documentation, the website
won. Where command examples lagged the released CLI, the actual executable's
help and schemas determined command syntax. The release baseline is 0.287.0.
No old product-hub content was used.

The request-shape reference added in 0.2.1 comes from authorized live tests of
the public CLI and hosted account MCP, including read-back and conversation
verification. It contains synthetic examples, not private implementation code
or customer resource IDs. The [live acceptance report](../evals/reports/2026-10-16-live-product.md)
records the baseline, corrections, retests, and remaining limits.

## Packaging references

- [Agent Plugins specification](https://agent-plugins.org/)
- [OpenAI plugin authoring](https://developers.openai.com/plugins/build/plugins)
- [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Cursor plugin reference](https://cursor.com/docs/reference/plugins)
- [Cursor skills](https://cursor.com/docs/skills)

Host formats are thin adapters around the same skill tree. No automatic
permission-granting hooks are included.

## CLI supply chain

The native installers use assets from the public Voiceflow CLI v0.287.0 release.
All six SHA-256 values are pinned in the skill bundle, rather than trusting an
unversioned latest installer. The binary remains a separately distributed
Voiceflow component under its own licensing; it is not included in this repo
or its plugin archive.
