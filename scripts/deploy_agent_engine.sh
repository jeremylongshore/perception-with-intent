#!/usr/bin/env bash
set -euo pipefail

# Deploy the IAMJVP agent to Vertex AI Agent Engine.
# Relies on the ADK CLI; confirm exact command once manuals finalize.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_CONFIG="$ROOT_DIR/app/jvp_agent/agent.yaml"

: "${VERTEX_PROJECT_ID:?VERTEX_PROJECT_ID is required}"
: "${VERTEX_LOCATION:?VERTEX_LOCATION is required}"
: "${VERTEX_AGENT_ENGINE_ID:?VERTEX_AGENT_ENGINE_ID is required}"

if ! command -v adk >/dev/null 2>&1; then
  echo "adk CLI not found. // TODO(ask): confirm installation method (pip, gcloud component)." >&2
  exit 1
fi

echo "Deploying IAMJVP commander to Vertex AI Agent Engine..."
echo "Project: ${VERTEX_PROJECT_ID}"
echo "Location: ${VERTEX_LOCATION}"
echo "Agent Engine ID: ${VERTEX_AGENT_ENGINE_ID}"

# TODO(ask): Validate final flag set with manuals; placeholder below matches current guidance.
adk deploy agent_engine \
  --agent-config "${AGENT_CONFIG}" \
  --project "${VERTEX_PROJECT_ID}" \
  --location "${VERTEX_LOCATION}" \
  --agent-engine-id "${VERTEX_AGENT_ENGINE_ID}"

echo "Deployment command submitted. Verify status in the Google Cloud console."
