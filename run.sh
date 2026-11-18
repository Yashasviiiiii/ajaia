#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Backend setup ---
cd "$ROOT/backend"
[ -d .venv ] || python3 -m venv .venv
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  source .venv/Scripts/activate  # Git Bash on Windows
fi
pip install -q -r requirements.txt

# --- Frontend setup ---
cd "$ROOT/frontend"
[ -d node_modules ] || npm install

# --- Start both; stop both on Ctrl+C or exit ---
cleanup() {
  trap - INT TERM EXIT
  kill 0 2>/dev/null || true
}
trap cleanup INT TERM EXIT

(cd "$ROOT/backend" && uvicorn app.main:app --reload --port 8000) &
(cd "$ROOT/frontend" && npm run dev) &

echo "App: http://localhost:5173   API: http://localhost:8000/docs"
echo "Login: alice@example.com / bob@example.com / carol@example.com (password123)"
wait