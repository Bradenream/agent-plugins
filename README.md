# Voiceflow for coding agents

Connect Voiceflow once. Then tell your coding agent what you want to build.

This private preview provides one shared skill library for Claude Code, Codex,
and Cursor. It uses Voiceflow's released CLI and browser sign-in, or an existing
working Voiceflow MCP connection. No API key pasted into a conversation, no
project created during setup, and no separate runtime service.

## Try the preview

Give an agent with access to this private repository this prompt:

> Read the setup guide in Bradenream/agent-plugins on branch
> codex/voiceflow-agent-plugin at
> voiceflow/skills/voiceflow-setup/references/setup.md and follow it to connect
> me to Voiceflow. Complete the setup yourself where possible, and then ask
> what I would like to build or improve.

The agent needs an authenticated GitHub connection or local checkout. This is
not yet an anonymous public install. For a checkout, ask it to follow the
[setup guide](voiceflow/skills/voiceflow-setup/references/setup.md).

Successful setup ends with:

> You're connected to Voiceflow. What would you like to build or improve?

## What's included

- Repeatable setup with live, read-only connection verification.
- Fifteen portable skills for setup, building, prompts, workflows, tools,
  knowledge, voice, debugging, transcripts, evaluations, and environments.
- Native Claude Code and Codex packages; a Cursor manifest and standalone
  skill installation for private previews.
- Checksum-verified CLI installers for macOS, Linux, and Windows.
- A reproducible website bundle generated from the same setup guide and skills.

Product guidance comes from the [Voiceflow documentation](https://www.voiceflow.com/docs).
See the [skill index](voiceflow/skills/voiceflow/SKILL.md),
[compatibility](docs/compatibility.md), [release checklist](docs/releasing.md),
and [website publishing contract](docs/website-publishing.md).

## Develop

Python 3.10+ is required for repository checks and builds, not normal CLI
installation or native plugin use. There are no Python package dependencies.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

Output goes to `dist/`. Tests use temporary directories and fake credentials;
they do not sign in or change Voiceflow projects.

This is a personal preview, not a published Voiceflow marketplace listing.
Public release, organization transfer, and the website hookup are separate
steps. See [provenance](docs/provenance.md) for the adaptation history.
