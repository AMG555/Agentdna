# AgentDNA status — verified during the current validation run

## Verified in this workspace

- `python -m unittest discover -s tests -v`: 8 passed
- `python -m compileall -q backend`: passed
- `node --check app.js`: passed
- Frontend source, backend source, wireframe and architecture files are present.

## Not verified here

- FastAPI server boot, because FastAPI is not installed in this sandbox.
- Native permissions or active-window capture on Windows/macOS/Linux.
- Desktop packaging, installer, signing and auto-update.
- Cloud or local LLM providers.
- Native notifications and automation execution.
- Full API, WebSocket, browser, security and end-to-end tests.

## Product classification

This repository is a privacy-first functional prototype and backend foundation. It is not yet a fully certified production desktop product. It must not be marketed as silently observing a user's computer: monitoring is disabled by default and requires explicit allowlisting plus resume.

## Exact release gate

Do not label a release production-ready until the unverified items above have platform-specific automated tests and a signed desktop build has passed install, permission, restart, privacy, deletion and upgrade tests.
