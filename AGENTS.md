# Working on Voiceflow agent plugins

Keep the canonical guide in `voiceflow/skills/voiceflow-setup/references/setup.md`.
Generate the website copy. Product knowledge comes from Voiceflow website docs;
CLI help describes the installed command contract.

Customer skills must work without private repositories, internal Copilot helpers,
auto-approval hooks, or a new backend. Never run customer writes or sign-in flows
in repository tests. Use temporary host configuration for installation tests.

Keep one shared skill tree. Every relative reference must ship with the package.
Preserve user-edited skills; update conflicts must fail before changing files.
Run `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`,
and `python3 scripts/build.py`. Schema checks do not prove model behavior.
Work on a feature branch; do not publish, transfer, or merge without approval.
