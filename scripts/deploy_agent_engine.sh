#!/usr/bin/env bash
set -euo pipefail

# Deploy Perception Agent Engine to Vertex AI
# Deploys the multi-agent system (Agent 0-8) to Agent Engine

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_ENGINE_APP="$ROOT_DIR/agent_engine_app.py"

: "${VERTEX_PROJECT_ID:?VERTEX_PROJECT_ID is required}"
: "${VERTEX_LOCATION:?VERTEX_LOCATION is required}"

if ! command -v adk >/dev/null 2>&1; then
  echo "ERROR: adk CLI not found. Install with: pip install google-genai[adk]" >&2
  exit 1
fi

if [[ ! -f "$AGENT_ENGINE_APP" ]]; then
  echo "ERROR: Agent Engine app not found at $AGENT_ENGINE_APP" >&2
  exit 1
fi

echo "=========================================="
echo "Deploying Perception to Vertex AI Agent Engine"
echo "=========================================="
echo "Project:       ${VERTEX_PROJECT_ID}"
echo "Location:      ${VERTEX_LOCATION}"
echo "App:           ${AGENT_ENGINE_APP}"
echo "Display Name:  Perception With Intent"
echo "=========================================="

# Deploy Agent Engine app with telemetry
cd "$ROOT_DIR"
adk deploy agent_engine \
  --project="${VERTEX_PROJECT_ID}" \
  --region="${VERTEX_LOCATION}" \
  --display_name="Perception With Intent" \
  "${AGENT_ENGINE_APP}" \
  --trace_to_cloud

echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
echo ""
echo "Verify deployment:"
echo "  gcloud alpha aiplatform agents list \\"
echo "    --project=${VERTEX_PROJECT_ID} \\"
echo "    --location=${VERTEX_LOCATION}"
echo ""
