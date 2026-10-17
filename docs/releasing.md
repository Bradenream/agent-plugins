# Maintain and release

## Ownership and maintenance

The package is MIT-licensed, copyright Voiceflow, Inc. Braden Ream
([@Bradenream](https://github.com/Bradenream)) currently maintains this repository;
`.github/CODEOWNERS` routes reviews to that account until transfer. The GitHub
location does not change the package's copyright holder.

This is beta software. Fixes target the newest tagged release; older releases
and edited forks have no guaranteed backports. Before the first release, the
implementation branch is a development preview. Package versions follow SemVer:
patches correct guidance or compatible behavior, minors add capabilities, and
breaking changes require an explicit migration note (minor increments while
0.x). Use [CHANGELOG](../CHANGELOG.md) for customer-visible changes. Package
versions and the pinned CLI version are independent.

Support is best effort with no response SLA. Report vulnerabilities through
[SECURITY](../SECURITY.md) and package/product problems through [SUPPORT](../SUPPORT.md).

## Before merging

Read current Voiceflow website docs and released CLI help for changed product
behavior. Run structural validation, unit tests, build, and isolated native host
verification. Require the security scan and Linux, macOS, and Windows CI jobs to pass. Inspect the
archive for license notices, complete references, and unintended material.
Behavioral changes also require the relevant [acceptance cases](../evals/README.md),
with unrun checks recorded honestly.

Use feature branches and obtain the owner's approval before merging. Increment
all four plugin manifests and metadata in the
[documentation workflow](../voiceflow/skills/voiceflow/references/documentation.md)
together when preparing an update. Update the changelog and compatibility matrix;
never rewrite old evaluation reports to imply a rerun.

For a CLI baseline change, review release notes and auth changes, update all six
pinned checksums from the official release, and rerun installers and localhost
contracts. Do not replace checksums merely to bypass a failed download.

## Repository settings before public launch

The current private repository plan does not provide protected-branch rules.
When protection becomes available through publication, transfer, or a plan change:

- Require a pull request and maintainer review for the default/release branch.
- Require the three `checks` jobs (Ubuntu, macOS, Windows) from the validation workflow.
- Require `Secrets and workflow security` from the reusable security workflow.
- Block force pushes and branch deletion, and dismiss stale approvals.
- Verify CODEOWNERS resolves to a maintainer with repository access.
- Enable private vulnerability reporting as an additional route; keep the verified
  security email available independently.
- Enable and verify GitHub secret scanning and push protection. CI catches
  committed leaks after upload; push protection helps stop supported secrets before upload.

Confirm the rules in GitHub after enabling them. Written policy or a CODEOWNERS
file alone is not enforcement. Publication, transfer, and changing a paid plan
are separate owner decisions.

## Prepare a release

A release starts from an approved, clean commit whose package version matches
the changelog. Rebuild from that commit; never reuse local dirty artifacts.

```sh
python3 scripts/prepare_release.py --expected-version 0.4.2 --expected-commit FULL_COMMIT_SHA
```

Use the actual full commit SHA, replacing the example. Preparation verifies
version, clean-source provenance, and file hashes, then writes to `dist/release/`:

- `voiceflow-VERSION.zip`: the portable plugin and native adapters.
- `voiceflow-site-VERSION.zip`: the complete `agents/` website payload.
- `manifest.json`: source commit, package version, and payload hashes.
- `SHA256SUMS`: hashes for both archives, manifest, and release notes.
- `release-notes.md`: the matching changelog entry and source revision.

Preparation does not create a tag, release, or deployment. It rejects stale or
tampered content and an existing output directory. Rebuilding replaces only the
repository's generated `dist/` directory.

Once the workflow is available on the default branch, run **Prepare draft package
release** in GitHub Actions with an approved full commit SHA and package version.
It reruns security and three-platform checks for that commit, prepares and scans
the exact assets with read-only permissions, and creates an **unpublished beta
draft** in a separate write-enabled job that does not execute repository code.
Existing tags/releases are never replaced.
No workflow publishes a release automatically. Review its notes, compatibility
limits, checksums, source commit, and all assets before the owner publishes it.
For a failed or ambiguous run, inspect existing drafts before retrying.

At publication, date the changelog entry in the approved source commit. Keep
released tags and assets immutable; correct mistakes with a new version. GitHub
releases provide the persistent download record; short-lived CI artifacts are
for review only. This repo has not yet published its first release.

## Upgrade, rollback, and transfer

Follow [client updates and removal](../voiceflow/skills/voiceflow-setup/references/clients.md).
Use native host update commands or the standalone installer's `--update`, which
refuses user-edited files. Review changes before updating and preserve local edits.

If a release fails, keep the previous approved website bundle for atomic rollback
and publish a corrective package version. Customers can intentionally reinstall
an earlier package using the same conflict-preserving process, but a website
rollback does not downgrade installed plugins or revoke OAuth access.

When approved for public launch, promote the implementation to the default branch,
remove the temporary repository-access note from the README, and test anonymous
retrieval of the setup guide and its references. Keep experimental paths labeled;
only expand claims after actual host acceptance. Use the
[website publishing contract](website-publishing.md) for the separate site rollout.

Transfer to Voiceflow when approved. Update repository/issue links, reviewer
ownership, and GitHub metadata, then verify redirects and fresh installs. Keep
plugin name `voiceflow`, marketplace name `voiceflow-plugins`, and skill names
stable. Marketplace submission is independent of repository publication.

Docs requests use the existing Knowledge MCP logging, as explained in
[measurement](measurement.md); releases do not add a separate analytics service.
