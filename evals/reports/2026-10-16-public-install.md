# Public repository installation verification — 2026-10-16

Source: [`2f418543b0dca4329c0477c89b69fb95abb5c330`](https://github.com/Bradenream/agent-plugins/commit/2f418543b0dca4329c0477c89b69fb95abb5c330),
package candidate **0.4.2**. The owner made the repository public. These checks
used the public default branch, not a locally copied working tree.

## Anonymous access and installation

- Cloned the public HTTPS repository with a clean child environment, no GitHub
  credential variables, disabled global/system Git configuration, no credential
  helper, and terminal authentication prompts disabled.
- Retrieved 64 README, skill, reference, license, and adapter/configuration files
  directly from their commit-pinned raw GitHub URLs without authentication.
  Every response was HTTP 200, was not HTML, and matched the checkout byte for byte.
- Package validation confirmed all sixteen skills, manifests, checksums, and
  local references.
- Installed all sixteen standalone skills into disposable Claude, Codex, and
  Cursor target directories. Every source file matched. Repeated installation
  and removal both succeeded without leaving managed files behind.
- Installed the native package in disposable Codex and Claude profiles. Both
  reported the enabled plugin; all sixteen skills, Markdown references, license
  notices, and both docs MCP configurations matched the anonymous checkout.

No real client profile, Voiceflow account, OAuth session, or customer project was
changed. Cursor native discovery remains unverified. This verifies public access
and package installation, not fresh-account onboarding, automatic skill selection
in a later conversation, or a newly published marketplace listing.

## Public GitHub protections

Verified through the repository administration API:

- Secret scanning and secret push protection enabled; no open secret-scanning
  alerts were returned at verification time.
- Private vulnerability reporting enabled.
- All outside contributors' workflows require maintainer approval.
- [Default-branch ruleset](https://github.com/Bradenream/agent-plugins/rules/25289649)
  active, with an empty bypass list: pull requests, resolved review threads,
  stale-review dismissal, all four strict checks bound to GitHub Actions,
  and protection against force pushes and branch deletion.
- Zero required approvals and no mandatory code-owner/last-pusher approval,
  following the owner's sole-maintainer decision. This does not grant additional
  collaborators access or waive the owner's approval for agent-driven merges.

The maintenance update aligns the release guard with this policy; its live
read-only verification accepted the protected default branch. It does not
create a tag, release, paid plan, marketplace listing, or website deployment.

Settings and alert counts are a point-in-time observation, not proof against
future changes or unknown secret formats. See [compatibility](../../docs/compatibility.md)
for the remaining client and product acceptance limits.
