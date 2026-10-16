# Maintain and release

## Before each change

Read the relevant Voiceflow website docs and current CLI help. Keep product
behavior in focused skills, command contracts in released help, and host-specific
details in the client reference. Do not duplicate a full API reference.

For a CLI baseline update, review release notes and auth changes, then update
cli-version.txt and all six pinned checksums from the official release. Re-run
platform installers and local HTTP contract checks. Change the validation
baseline deliberately. Never replace checksums based only on a failing download.

## Before merging

Run structural validation, unit tests, build, and native host verification.
Require the Linux, macOS, and Windows CI jobs to pass. Review every generated
file and confirm no credentials, local paths, private data, or unrelated files
are in the plugin archive. Behavioral skill changes also require the relevant
[acceptance cases](../evals/README.md).

Use a feature branch and obtain the owner's approval before merging. Increment
all four plugin manifest versions together when shipping an update. Native
plugin caches use the version; unchanged versions can hide updated content.

## Public release and migration

The repo is currently private under Bradenream. Do not claim public marketplace
availability or an anonymous setup flow yet. When approved:

1. Complete fresh OAuth and fresh-chat acceptance in Claude Code, Codex, and
   Cursor, plus the important product-task cases.
2. Review the MIT-licensed original package content and source provenance for
   public distribution. This package does not vendor private product code.
3. Remove preview-branch wording from the canonical guide and README.
4. Transfer the repository to the approved Voiceflow owner, update repository
   metadata and maintainer links, and verify redirects. Keep the plugin name
   `voiceflow`, marketplace name `voiceflow-plugins`, and skill names stable.
5. Publish an approved version and hook up the website using the
   [publishing contract](website-publishing.md).
6. Submit marketplace listings separately if desired. Local installation works
   before listings exist; acceptance by a marketplace is not automatic.

Rollback by restoring the previous website bundle and releasing a corrective
plugin version. Preserve customer-edited loose skills; do not force replacement.

## Scope

This repo contains instructions and small installation/build utilities. It does
not create a new auth backend, collect telemetry, run a daemon, automatically
update customer tools, or publish Voiceflow projects.
