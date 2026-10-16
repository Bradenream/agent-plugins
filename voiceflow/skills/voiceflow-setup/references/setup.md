# Connect your coding agent to Voiceflow

Prepare Voiceflow for the user. Do the mechanical steps yourself. They should
only need browser sign-in when required, then describe what they want to build.
Keep progress messages short.

## 1. Load and retain the skills

If this guide arrived through an installed plugin, use its adjacent skills.
For the private preview, use an authenticated checkout of
`Bradenream/agent-plugins` on branch `codex/voiceflow-agent-plugin`; never ask for
a GitHub token in chat. Do not assume `main` already contains the preview.

For the published website version, download the sibling `voiceflow.zip` and
`manifest.json` from the same `/agents/` location. Verify the archive's SHA-256
against the manifest before extracting into a user-owned cache outside the
customer's project. It contains a `voiceflow/` plugin. If these files are
unavailable, report that setup has not been published; do not invent a URL.

Follow [client installation](clients.md) for the current agent only. Avoid
installing both a plugin and duplicate loose skills. Read the installed
[entry skill](../../voiceflow/SKILL.md) now, and confirm its linked files exist.
Keep this session usable if the host needs a reload for native discovery. Tell
the user about a pending reload rather than claiming it already happened.

## 2. Reuse a working connection

If authenticated Voiceflow MCP tools are already available, inspect their schemas
and make one read-only workspace-list request. A successful response, including
an empty list, is sufficient. Reuse it and skip CLI installation/sign-in. Add the
CLI later only if needed for a task the existing toolset cannot perform.

Otherwise locate `vf`, then run `vf version` and `vf auth login --help`.
The tested baseline is **0.287.0**, with `--agent-mode`, `--no-browser`,
`--login-timeout`, and `workspace list`. Retain a newer compatible installation.
If an existing version lacks these capabilities, explain the needed upgrade;
preserve its location and do not overwrite an unrelated executable.

If absent, use [the verified CLI installer](installation.md). Use its returned
absolute binary path for the rest of this session if it is not on PATH.

Make this live read:

```sh
vf workspace list --agent-mode --no-interactive --timeout 20s -o json
```

Do not use `whoami` or stored credentials as proof of connection. Do not print
workspace details unless asked. An empty list is a connected account, not a
reason to create a workspace. Classify failures before acting:

- Missing/expired authentication or HTTP 401: continue to browser sign-in.
- HTTP 403: explain insufficient access; repeated login is not a permission fix.
- Network, rate limit, or service failure: retry a read once after a short
  indicated delay, otherwise report the blocker. Do not erase credentials.
- Invalid response or missing command: inspect help and the failure; do not
  claim connected.

The optional [connection checker](../scripts/check_connection.py) makes this
read without printing its body when Python 3.10+ is already available. It does
not install, log in, or repair anything.

## 3. Sign in only if needed

Run as a background task with a bounded 15-minute lifetime. Read JSON events
from stderr while it runs:

```sh
vf auth login --agent-mode --no-browser --login-timeout 15m
```

Show the exact `authorization_url` from `awaiting_authorization`. Ask the user
to sign in or create a Voiceflow account in the browser and approve access.
Wait for that process; do not start competing login flows. Do not save auth URLs
or credentials in the repository. Wait for `signed_in`, then repeat the live
workspace read. A closed browser, expired link, or cancelled login is not success.
Offer one fresh login attempt if needed.

The callback runs on the CLI's machine. For SSH or containers, first establish
supported loopback port forwarding using the current CLI instructions. If the
user's browser cannot reach that listener, explain the limitation and offer
local setup. Never claim a remote loopback URL has completed authentication.

Never ask for passwords, tokens, or secret values in chat. `VF_TOKEN` overrides
stored OAuth credentials; inspect only its presence, not its value. Explain a
stale override before changing it.

## 4. Verify, then hand over

Confirm all three conditions:

1. A live, read-only Voiceflow request succeeded in this session.
2. The entry skill and linked files are readable now.
3. The plugin/skills are registered or saved in the host's persistent skill
   location. Note any pending host reload honestly.

If blocked, state what is missing and the smallest next step. Do not claim
completion yet. Do not select a workspace/project, run a conversation, create
content, or publish during setup.

Once ready, end with exactly:

> You're connected to Voiceflow. What would you like to build or improve?

Wait for the answer. No sample project, task menu, workspace chooser, or extra
discovery interview should come before that question.
