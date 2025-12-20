#!/usr/bin/env bash
set -euo pipefail

# Trigger E2E Ingestion via Vertex AI Agent Engine
# This script invokes the deployed Agent Engine app to run a full ingestion cycle

: "${VERTEX_PROJECT_ID:?VERTEX_PROJECT_ID is required}"
: "${VERTEX_LOCATION:?VERTEX_LOCATION is required}"
: "${VERTEX_AGENT_ID:?VERTEX_AGENT_ID is required - get from: gcloud alpha aiplatform agents list}"

USER_ID="${USER_ID:-smoke-test-user}"
TRIGGER="${TRIGGER:-manual_e2e_test}"

echo "=========================================="
echo "Triggering E2E Ingestion via Agent Engine"
echo "=========================================="
echo "Project:   ${VERTEX_PROJECT_ID}"
echo "Location:  ${VERTEX_LOCATION}"
echo "Agent ID:  ${VERTEX_AGENT_ID}"
echo "User ID:   ${USER_ID}"
echo "Trigger:   ${TRIGGER}"
echo "=========================================="
echo ""

# Prepare request payload
REQUEST_PAYLOAD=$(cat <<EOF
{
  "user_query": "Run a full ingestion cycle now for E2E testing.",
  "mode": "system_command",
  "command": "run_daily_ingestion",
  "user_id": "${USER_ID}",
  "trigger": "${TRIGGER}",
  "params": {
    "verbose": true
  }
}
EOF
)

echo "Sending request to Agent Engine..."
echo ""

# Invoke agent via ADK CLI (if available)
if command -v adk >/dev/null 2>&1; then
  echo "Using ADK CLI..."

  # Create temp file for request
  TEMP_REQUEST=$(mktemp)
  echo "$REQUEST_PAYLOAD" > "$TEMP_REQUEST"

  adk agents invoke \
    --project="${VERTEX_PROJECT_ID}" \
    --location="${VERTEX_LOCATION}" \
    --agent-id="${VERTEX_AGENT_ID}" \
    --request-file="$TEMP_REQUEST"

  rm -f "$TEMP_REQUEST"

else
  echo "WARNING: ADK CLI not found. Falling back to gcloud..."
  echo ""

  # Use gcloud aiplatform command
  gcloud alpha aiplatform agents predict \
    --project="${VERTEX_PROJECT_ID}" \
    --location="${VERTEX_LOCATION}" \
    --agent="${VERTEX_AGENT_ID}" \
    --json-request="$REQUEST_PAYLOAD"
fi

echo ""
echo "=========================================="
echo "Request sent!"
echo "=========================================="
echo ""
echo "Check results:"
echo "1. Firestore ingestion_runs collection:"
echo "   gcloud firestore documents list --collection=ingestion_runs --limit=1"
echo ""
echo "2. Cloud Logging:"
echo "   gcloud logging read 'resource.type=\"aiplatform.googleapis.com/Agent\"' --limit=20"
echo ""
echo "3. MCP Service logs:"
echo "   gcloud logging read 'resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"perception-mcp\"' --limit=10"
echo ""
