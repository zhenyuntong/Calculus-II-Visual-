#!/bin/zsh
set -e

PROJECT_DIR="${0:A:h}"
cd "$PROJECT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  osascript -e 'display alert "Python 3 is required" message "Install Python 3, then double-click this launcher again." as critical'
  exit 1
fi

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Preparing Calculus Visualizer for first use…"
  python3 -m venv .venv
fi

if ! .venv/bin/python -c 'import flask, sympy' >/dev/null 2>&1; then
  echo "Installing the small set of required packages…"
  .venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
fi

echo "Starting Calculus Visualizer…"
.venv/bin/python app.py &
APP_PID=$!
trap 'kill "$APP_PID" 2>/dev/null || true' EXIT INT TERM

for attempt in {1..60}; do
  if curl --silent --fail http://127.0.0.1:5050/ >/dev/null 2>&1; then
    open http://127.0.0.1:5050/
    echo "Ready. Keep this window open while you use the app."
    wait "$APP_PID"
    exit $?
  fi
  sleep 0.2
done

echo "The app did not start. Review the message above, then try again."
exit 1
