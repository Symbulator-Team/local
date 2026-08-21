#!/bin/bash
# Double-click this file to run Symbulator 9 locally and open it in
# your browser. macOS may first ask you to confirm it's OK to run a
# downloaded script -- see "If macOS won't run start.command" below.
cd "$(dirname "$0")"
PORT=8000

if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  echo "Python 3 was not found. Install it from https://python.org and try again."
  read -n 1 -s -r -p "Press any key to close this window..."
  exit 1
fi

( sleep 1; open "http://localhost:$PORT/" ) &

echo "Starting Symbulator 9 at http://localhost:$PORT/"
echo "Leave this window open while you use it. Close the window (or press Ctrl+C) to stop."
"$PY" -m http.server "$PORT"
