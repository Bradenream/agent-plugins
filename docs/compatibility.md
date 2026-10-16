# Compatibility and evidence

This is a private preview. Packaging checks are not a claim that every agent
model has completed onboarding successfully.

| Surface | Evidence |
| --- | --- |
| Claude Code 2.1.124 | Native manifest validation, isolated marketplace install, enabled plugin inventory, all 15 skill files present |
| Codex CLI 0.162.0-alpha.2 | Isolated marketplace install, enabled plugin inventory, all 15 skill files present |
| Cursor | Manifest checked against current documentation; standalone skill installation tested. Interactive discovery has not been tested locally because Cursor is unavailable |
| macOS arm64 | Real checksum-verified CLI install and existing-binary preservation tested |
| Linux x86_64 and Windows x86_64 | Real checksum-verified installers, package checks, and CLI contract checks passed in CI |
| CLI 0.287.0 | Live executable help checked; five local HTTP scenarios exercised without contacting a Voiceflow account |
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
