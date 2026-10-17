# Compatibility and evidence

This is a private preview. Packaging checks are not a claim that every agent
model has completed onboarding successfully.

| Surface | Evidence |
| --- | --- |
| Claude Code 2.1.124 | Isolated marketplace install of 0.3.0, enabled plugin inventory, all 16 skills and Markdown references match source |
| Codex CLI 0.162.0-alpha.2 | Isolated marketplace install of 0.3.0, enabled plugin inventory, all 16 skills and Markdown references match source |
| Cursor | Manifest checked against current documentation; standalone skill installation tested. Interactive discovery has not been tested locally because Cursor is unavailable |
| macOS arm64 | Real checksum-verified CLI install and existing-binary preservation tested |
| Linux x86_64 and Windows x86_64 | Real checksum-verified installers, package checks, and CLI contract checks passed in CI |
| CLI 0.287.0 | Executable help checked; five connection scenarios and four widget request contracts exercised against localhost without contacting Voiceflow |
| Skill installation | Repeat install, conflict preservation, updates, removal, rollback, path protection, complete tree |
| Website bundle | Repeat builds produce identical bytes; every emitted setup link resolves and every artifact hash matches |
| Chat-assistant routing (0.2.0) | Three capability-constrained subagents exercised 12 offline scenarios: seven completed setup and five correctly blocked or requested the missing step; all 12 passed behavioral review |

The baseline review is dated **2026-10-16**. Native host verification checks
installation/discovery files, not model selection or completion quality.
No real OAuth session or customer mutation was performed by this repository's
automated tests. Browser OAuth, fresh-chat skill selection, and representative
product tasks are acceptance checks before a public release.

The [initial complete platform run](https://github.com/Bradenream/agent-plugins/actions/runs/38980919367)
passed on all three operating systems. All 23 local tests passed (the three Unix
installer unit tests are intentionally skipped on Windows, whose actual installer
is tested in its CI job). Downloaded CI artifacts had matching content digests
across Linux, Windows, and macOS, and every manifest file hash was verified.

CLI 0.287.0 has a JSON passthrough/timeout interaction: a response whose body
arrives after its headers can be cancelled before JSON output is consumed,
producing blank output with exit code zero. Setup therefore uses typed TOON
output and explicitly rejects blank output. The HTTP fixture deliberately splits
headers and body to retain regression coverage. This repo does not modify the CLI.

Run the local checks:

```sh
python3 scripts/verify_hosts.py
python3 scripts/verify_cli.py --vf /absolute/path/to/vf
```

The first script creates disposable client configurations. The second uses a
local fixture server and a fake token; it never signs in or contacts Voiceflow.
Neither installs into the user's real skill directory.

See [acceptance cases](../evals/README.md) for the remaining behavior tests.

For 0.2.0, all 32 local tests pass, including fixture boundary checks. The updated
package was installed in isolated Codex and Claude Code profiles, with all 15
skills discovered. The [chat evaluation report](../evals/reports/2026-10-16-chat-setup.md)
records the actual subagent decisions, fixture issues, and limitations. These
simulations do not establish compatibility with any named chat application;
live OAuth and fresh-chat checks remain required before advertising support.

For 0.3.0, all 32 local tests pass. Archive, generated website payload, standalone
installation, and native Codex/Claude caches include the complete widget guide
tree. Widget CLI fixtures verify request paths, version selection, stdin patch
body, and nonempty output. Twelve new widget acceptance cases are specified but
have not been executed as model evaluations or live platform installations;
see the [widget protocol](../evals/widget-protocol.md). No website deployment or
customer-account mutation was part of these checks.

For 0.4.0, all 37 unit tests and all 16 skill validations pass. The docs MCP is bundled in the portable package and Codex/Claude
adapter. Isolated native installs retained both configurations and all 16
skills/references. Standalone skill installation still requires the host's
normal docs connection step. Cursor's declared format is checked against its
current reference; runtime discovery remains untested locally.

A separate public, read-only probe verified Voiceflow Knowledge MCP 2.1.2,
its four tools and required context fields, an `ask_voiceflow` response, and
an exact Widget API page read. The first answer was low-confidence and reported
`answerable: false`; it was not accepted as a complete implementation answer.
No account credentials or customer data were sent. Unit checks include no-auth
docs connection, separate account/docs verification, duplicate rejection, and
explicit web fallback. The new [docs behavior cases](../evals/docs-protocol.md)
remain unrun as model evaluations; earlier live results must not be interpreted
as docs-MCP coverage.
