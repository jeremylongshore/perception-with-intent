#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_CONFIG="$ROOT_DIR/app/jvp_agent/agent.yaml"

if [[ ! -f "$AGENT_CONFIG" ]]; then
  echo "Agent configuration not found at $AGENT_CONFIG" >&2
  exit 1
fi

echo "Starting ADK dev server for JVP (IAMJVP)..."
echo "Agent config: $AGENT_CONFIG"

# Running via uvicorn keeps parity with the new a2a template.
# TODO(ask): replace with `adk api_server` once the CLI supports A2A wrappers.
python -m app.main "$@"
