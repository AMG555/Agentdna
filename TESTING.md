# Testing status

## Run automated tests

The core test suite uses Python's standard `unittest` module and does not require pytest:

```bash
cd agentdna
python -m unittest discover -s tests -v
```

The suite currently covers:

- Privacy-safe defaults
- Application allowlisting
- Blocked sensitive apps
- Immediate pause behavior
- Fitness increases after feedback
- Agent death after `NEVER`
- Fitness clamping
- Basic repetition pattern detection
- Empty pattern input

## Full test command

After installing dependencies:

```bash
python -m unittest discover -s tests -v
python -m compileall -q backend
```

## Important limitation

This is not yet a complete production test suite. It does not currently cover native OS permission prompts, real active-window adapters on every platform, the FastAPI routes, WebSocket reconnect behavior, encrypted storage, desktop packaging, native notifications, LLM providers, or reversible automation execution. Those require platform-specific integration and end-to-end tests.
