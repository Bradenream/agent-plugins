# Contributing

Describe the customer problem and expected behavior before changing a skill.
Keep setup focused on connection and the user's next request. Product advice
must cite current Voiceflow documentation; exact API fields must match supported
CLI help or MCP schemas.

Use short skill entrypoints and linked references for conditional detail.
Do not add internal tools, private repository dependencies, permission-bypass
hooks, or dependencies just to format a document.

Run the checks in [README](README.md) and add behavior tests for scripts with new
failure modes. For instruction changes, update and run the relevant
[acceptance cases](evals/README.md). Record model, host version, fixture,
observed actions, and limitations; do not label static checks as model evals.

Use synthetic data in issues and fixtures. Never attach credentials or customer
transcripts. Submit changes on a feature branch with a concise description and
verification evidence.
