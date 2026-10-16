# Voiceflow for AI assistants

Connect Voiceflow once. Then tell your assistant what you want to build.

This private preview provides one capability-based setup guide for coding agents
and chat assistants, plus a shared skill library packaged for Claude Code, Codex,
and Cursor. The assistant reuses working connections, chooses the CLI when it has
a persistent customer terminal, or connects hosted MCP through the host's tools
or settings. The user only completes steps the host cannot automate, such as
browser sign-in. Setup does not create a project or require secrets in chat.

## Try the preview

Give an agent with access to this private repository this prompt:

> Read the setup guide in Bradenream/agent-plugins on branch
> codex/voiceflow-agent-plugin at
> voiceflow/skills/voiceflow-setup/references/setup.md and follow it to connect
> me to Voiceflow. Complete the setup yourself where possible, and then ask
> what I would like to build or improve.

The assistant needs an authenticated GitHub reader, local checkout, or the guide
and its linked Markdown supplied as attachments. This is not yet an anonymous
public install. For a checkout, ask it to follow the
[setup guide](voiceflow/skills/voiceflow-setup/references/setup.md).

Successful setup ends with:

> You're connected to Voiceflow. What would you like to build or improve?

## What's included

- Repeatable setup with live, read-only connection verification.
- Hosted MCP setup and recovery for chat assistants, with guidance available
  through Markdown, the website docs, or the existing Knowledge MCP.
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
Chat-host paths are evaluated with capability-constrained subagents; support in
real chat applications requires their own connection and fresh-chat checks.
Public release, organization transfer, and the website hookup are separate
steps. See [provenance](docs/provenance.md) for the adaptation history.
