# Connect through the CLI

Use this path only when the [setup guide](setup.md) selected a terminal that
can install and run tools in the customer's persistent environment. A temporary
chat sandbox is not such an environment.

Locate `vf`, then run `vf version` and `vf auth login --help`.
The tested baseline is **0.287.0**, with `--agent-mode`, `--no-browser`,
`--login-timeout`, and `workspace list`. Retain a newer compatible installation.
If an existing version lacks these capabilities, explain the needed upgrade;
preserve its location and do not overwrite an unrelated executable.

If absent, use [the verified CLI installer](installation.md). Use its returned
absolute binary path for the rest of this session if it is not on PATH.

Make this live read:

```sh
vf workspace list --agent-mode --no-interactive --timeout 20s --color never -o toon
```

Do not use `whoami` or stored credentials as proof of connection. Do not print
workspace details unless asked. An empty list is a connected account, not a
reason to create a workspace. Classify failures before acting:

Use TOON for this read on CLI 0.287.0. Its JSON passthrough can produce empty
output when a timeout cancels the response before the body is consumed; TOON
uses the fully decoded response. Empty output is not an empty workspace list.

- Missing/expired authentication or HTTP 401: continue to browser sign-in.
- HTTP 403: explain insufficient access; repeated login is not a permission fix.
- Network, rate limit, or service failure: retry a read once after a short
  indicated delay, otherwise report the blocker. Do not erase credentials.
- Invalid response or missing command: inspect help and the failure; do not
  claim connected.

The optional [connection checker](../scripts/check_connection.py) makes this
read without printing its body when Python 3.10+ is already available. It does
not install, log in, or repair anything.

## Sign in only if needed

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

Return to [guidance and completion](setup.md#3-make-guidance-available-in-this-host).
