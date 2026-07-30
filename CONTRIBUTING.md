# Contributing to AgentDNA

Welcome. AgentDNA is an open-source, privacy-first project for building helpful personal automation without hidden surveillance.

## Principles

- Privacy and user consent come before capability.
- Monitoring must be opt-in and visible.
- Metadata minimization is preferred over content collection.
- Every automation must be scoped, permissioned, and reversible.
- Every important behavior should have a test.
- Documentation is part of the feature.

## Getting started

```bash
git clone <repository-url>
cd agentdna
./install.sh
./agentdna-cli.sh test
```

## Good first contributions

- Add a privacy redaction rule.
- Add an operating-system observer adapter.
- Add a pattern detector.
- Improve vector retrieval or evaluation.
- Add an LLM provider adapter.
- Add a reversible automation tool.
- Improve accessibility or responsive UI.
- Add unit, API, integration, or end-to-end tests.
- Improve installation and troubleshooting documentation.

## Change process

1. Open an issue for substantial changes.
2. Create a focused branch.
3. Add or update tests.
4. Update documentation.
5. Describe privacy and security implications.
6. Run the complete local check.
7. Open a pull request.

```bash
python -m unittest discover -s tests -v
python -m compileall -q backend
node --check app.js
```

## Pull requests

Please include:

- Problem and motivation
- Design summary
- Tests run
- Screenshots for UI changes
- Privacy impact
- New permissions or data fields
- Backward-compatibility notes

Pull requests that weaken consent, introduce silent collection, expose secrets, or add unrestricted automation will not be accepted.
