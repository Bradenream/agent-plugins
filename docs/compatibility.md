# Compatibility and evidence

This is a private preview. Packaging checks are not a claim that every agent
model has completed onboarding successfully.

| Surface | Evidence |
| --- | --- |
| Claude Code 2.1.124 | Native manifest validation, isolated marketplace install, enabled plugin inventory, all 15 skill files present |
| Codex CLI 0.162.0-alpha.2 | Isolated marketplace install, enabled plugin inventory, all 15 skill files present |
| Cursor | Manifest checked against current documentation; standalone skill installation tested. Interactive discovery has not been tested locally because Cursor is unavailable |
| macOS arm64 | Real checksum-verified CLI install and existing-binary preservation tested |
| Linux and Windows | CI runs real platform installers and CLI contract checks; see the branch's Actions results for current outcome |
| CLI 0.287.0 | Live executable help checked; five local HTTP scenarios exercised without contacting a Voiceflow account |
| Skill installation | Repeat install, conflict preservation, updates, removal, rollback, path protection, complete tree |
| Website bundle | Repeat builds produce identical bytes; every emitted setup link resolves and every artifact hash matches |

The baseline review is dated **2026-10-16**. Native host verification checks
installation/discovery files, not model selection or completion quality.
No real OAuth session or customer mutation was performed by this repository's
automated tests. Browser OAuth, fresh-chat skill selection, and representative
product tasks are acceptance checks before a public release.

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
