#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
. "$ROOT/.venv/bin/activate"
case "${1:-help}" in
  start) exec python -m uvicorn backend.main:app --host 127.0.0.1 --port "${PORT:-8000}" ;;
  test) python -m unittest discover -s tests -v ;;
  compile) python -m compileall -q backend && echo "Backend compilation passed" ;;
  health) curl -fsS "http://127.0.0.1:${PORT:-8000}/api/health" ;;
  pause) curl -fsS -X POST "http://127.0.0.1:${PORT:-8000}/api/privacy/pause" ;;
  privacy) curl -fsS "http://127.0.0.1:${PORT:-8000}/api/privacy" ;;
  help|*) echo "Usage: $0 {start|test|compile|health|pause|privacy}" ;;
esac
