#!/bin/sh
# Runs Symbulator 9 locally and opens it in your browser.
# Works on Linux and macOS. On macOS you can also just double-click
# start.command instead.
cd "$(dirname "$0")"
PORT=8000

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python was not found. Install Python 3 from https://python.org and try again."
  exit 1
fi

(
  sleep 1
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:$PORT/" >/dev/null 2>&1
  elif command -v open >/dev/null 2>&1; then
    open "http://localhost:$PORT/" >/dev/null 2>&1
  fi
) &

echo "Starting Symbulator 9 at http://localhost:$PORT/"
echo "Leave this window open while you use it. Press Ctrl+C to stop."
"$PY" -m http.server "$PORT"
