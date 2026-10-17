# Install the released CLI

First follow the reuse checks in [setup](setup.md). These scripts download
**v0.287.0** from Voiceflow's official GitHub release and verify the published
SHA-256. They do not sign in, edit profiles, or overwrite an existing binary.

macOS/Linux, with curl, tar, and shasum or sha256sum:

```sh
bash voiceflow/skills/voiceflow-setup/scripts/install-vf.sh
```

Windows PowerShell 5.1+ or PowerShell 7:

```powershell
& ./voiceflow/skills/voiceflow-setup/scripts/install-vf.ps1
```

Resolve script paths from the actual plugin location, not the customer's project.
`VF_INSTALL_DIR` supports a custom directory. Defaults are `~/.local/bin` on
Unix and `%LOCALAPPDATA%\Voiceflow\bin` on Windows. Use the printed absolute path
now; optionally add its directory to this process's PATH. Do not silently edit
persistent profiles. Agents can locate the saved path in later sessions.

For an authorized upgrade, preserve the old binary outside the target path and
restore it if installation fails. Never use sudo to force an install. No binary
from an unverified archive is run. Downloads have timeouts and bounded retries.
Network/checksum failure leaves the destination unchanged. Same-release HTTPS
checksums detect corruption; they are not an independent publisher signature.

For unsupported architecture or restricted shells, explain the obstacle and
consult the [CLI docs](https://www.voiceflow.com/docs/cli/install). Do not
substitute another project's `vf` executable.
