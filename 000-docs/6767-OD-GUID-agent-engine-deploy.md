# Perception With Intent - Agent Engine Deployment Guide

**Document ID:** 6767-OD-GUID-agent-engine-deploy
**Version:** 1.0
**Date:** 2025-11-15
**Phase:** Agent Engine Deployment + E2E Ingestion
**Category:** Operational Guide

---

## Executive Summary

This guide explains how to deploy Perception's multi-agent system to Vertex AI Agent Engine. The deployment creates a managed agent application that orchestrates 8 specialized agents (Agent 0-7) plus optional section editors (Agent 8+).

**Key Facts:**
- **Entrypoint:** `agent_engine_app.py` (project root)
- **Target Platform:** Vertex AI Agent Engine (GCP managed service)
- **Deployment Method:** ADK CLI via `scripts/deploy_agent_engine.sh`
- **Agent Count:** 8+ agents (Orchestrator + 7 specialized + section editors)
- **Communication:** A2A Protocol between agents
- **Observability:** Cloud Trace + Cloud Monitoring enabled

---

## Prerequisites

### Required Tools

1. **Google ADK CLI**
   ```bash
   pip install google-genai[adk]>=0.6.0
   ```

2. **Google Cloud SDK**
   ```bash
   gcloud components update
   gcloud auth application-default login
   ```

3. **GCP Project Access**
   - Project: `perception-with-intent`
   - Roles required:
     - `roles/aiplatform.admin` (for Agent Engine deployment)
     - `roles/logging.logWriter` (for Cloud Logging)
     - `roles/monitoring.metricWriter` (for metrics)

### Required Environment Variables

```bash
export VERTEX_PROJECT_ID="perception-with-intent"
export VERTEX_LOCATION="us-central1"
```

**Note:** `VERTEX_AGENT_ENGINE_ID` is NOT required - ADK creates it automatically during first deployment.

---

## Deployment Process

### Method 1: Manual Deployment (Recommended for Testing)

**Step 1:** Set environment variables
```bash
export VERTEX_PROJECT_ID="perception-with-intent"
export VERTEX_LOCATION="us-central1"
```

**Step 2:** Run deployment script
```bash
./scripts/deploy_agent_engine.sh
```

**Expected Output:**
```
==========================================
Deploying Perception to Vertex AI Agent Engine
==========================================
Project:       perception-with-intent
Location:      us-central1
App:           /home/jeremy/000-projects/perception/agent_engine_app.py
Display Name:  Perception With Intent
==========================================

Deploying agent engine...
[ADK deployment progress...]

==========================================
Deployment complete!
==========================================

Verify deployment:
  gcloud alpha aiplatform agents list \
    --project=perception-with-intent \
    --location=us-central1
```

**Step 3:** Verify deployment
```bash
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1
```

**Expected Response:**
```
AGENT_ID: perception-with-intent-<hash>
DISPLAY_NAME: Perception With Intent
STATE: ACTIVE
CREATE_TIME: 2025-11-15T...
```

---

### Method 2: GitHub Actions Workflow

**Trigger:**
```bash
gh workflow run deploy-agent-engine.yml \
  --repo jeremylongshore/perception-with-intent \
  --field project_id=perception-with-intent \
  --field location=us-central1 \
  --field agent_engine_id=<engine-id>
```

**Note:** GitHub Actions requires Workload Identity Federation (WIF) configured with these secrets:
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT_EMAIL`

---

## Agent Engine Architecture

### Application Structure

**Entrypoint:** `agent_engine_app.py`

```python
from google.adk.apps import App
from google.adk.agents import Agent
from google.adk import telemetry

# Configure telemetry
telemetry.enable_cloud_trace(
    project_id="perception-with-intent",
    service_name="perception-agents",
    service_version="1.0.0"
)

# Initialize app
app = App()

# Load root orchestrator (Agent 0) with all sub-agents
root_agent = Agent.from_config_file(
    "app/perception_agent/agents/agent_0_root_orchestrator.yaml"
)
app.register_agent(root_agent)
```

**Key Points:**
- Single `App()` instance registered to Agent Engine
- Root orchestrator (`agent_0_root_orchestrator.yaml`) is the entry point
- All sub-agents (Agent 1-8+) are loaded via YAML config references
- Agents communicate via A2A Protocol (not direct Python calls)

### Deployed Agents

**Agent 0: Root Orchestrator**
- Config: `app/perception_agent/agents/agent_0_root_orchestrator.yaml`
- Tools: `app/perception_agent/tools/agent_0_tools.py`
- Role: Coordinates entire workflow, manages run lifecycle

**Agent 1: Source Harvester**
- Config: `app/perception_agent/agents/agent_1_source_harvester.yaml`
- Tools: `app/perception_agent/tools/agent_1_tools.py`
- Role: Fetches RSS feeds, API feeds, web content via MCP

**Agent 2: Topic Manager**
- Config: `app/perception_agent/agents/agent_2_topic_manager.yaml`
- Tools: `app/perception_agent/tools/agent_2_tools.py`
- Role: Loads and manages tracked topics

**Agent 3: Relevance & Ranking**
- Config: `app/perception_agent/agents/agent_3_relevance_ranking.yaml`
- Tools: `app/perception_agent/tools/agent_3_tools.py`
- Role: Scores articles, infers sections, filters by relevance

**Agent 4: Brief Writer**
- Config: `app/perception_agent/agents/agent_4_brief_writer.yaml`
- Tools: `app/perception_agent/tools/agent_4_tools.py`
- Role: Builds daily brief payload with sections

**Agent 5: Alert & Anomaly Detector** (Future)
- Config: `app/perception_agent/agents/agent_5_alert_anomaly.yaml`
- Tools: `app/perception_agent/tools/agent_5_tools.py`
- Role: Detects breaking news, anomalies

**Agent 6: Validator**
- Config: `app/perception_agent/agents/agent_6_validator.yaml`
- Tools: `app/perception_agent/tools/agent_6_tools.py`
- Role: Validates article and brief schemas

**Agent 7: Storage Manager**
- Config: `app/perception_agent/agents/agent_7_storage_manager.yaml`
- Tools: `app/perception_agent/tools/agent_7_tools.py`
- Role: Writes to Firestore, updates ingestion run records

**Agent 8: Technology Desk Editor** (Optional)
- Config: `app/perception_agent/agents/agent_8_tech_editor.yaml`
- Tools: `app/perception_agent/tools/agent_8_tools.py`
- Role: Curates and enhances Technology section

---

## Verifying Deployment

### Check Agent Engine Status

**Command:**
```bash
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1
```

**What to Look For:**
- `STATE: ACTIVE` - Agent Engine is running
- `DISPLAY_NAME: Perception With Intent` - Correct app deployed
- `AGENT_ID` - Copy this for future operations

### Check Agent Engine Logs

**Command:**
```bash
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/Agent" AND resource.labels.agent_id="<AGENT_ID>"' \
  --project=perception-with-intent \
  --limit=10
```

**Expected:**
- Startup logs showing "Perception Agent Engine starting..."
- "Root orchestrator loaded with all sub-agents"
- "Ready to receive tasks via A2A Protocol"

### Test Agent Engine Health

**Simple Health Check:**
```bash
# Using ADK CLI (if available)
adk agents invoke \
  --project=perception-with-intent \
  --location=us-central1 \
  --agent-id=<AGENT_ID> \
  --query="System status check"
```

**Expected Response:**
```json
{
  "status": "online",
  "agents_loaded": 8,
  "root_orchestrator": "agent_0_root_orchestrator",
  "ready": true
}
```

---

## Troubleshooting

### Deployment Fails: "adk CLI not found"

**Error:**
```
ERROR: adk CLI not found. Install with: pip install google-genai[adk]
```

**Solution:**
```bash
pip install google-genai[adk]>=0.6.0
adk --version
```

### Deployment Fails: "Permission Denied"

**Error:**
```
ERROR: User does not have permission to create agents in project perception-with-intent
```

**Solution:**
```bash
# Grant required IAM roles
gcloud projects add-iam-policy-binding perception-with-intent \
  --member="user:jeremy@intentsolutions.io" \
  --role="roles/aiplatform.admin"
```

### Agent Engine Not Listed

**Symptom:** `gcloud alpha aiplatform agents list` returns empty

**Common Causes:**
1. Wrong project/location specified
2. Deployment still in progress (wait 2-3 minutes)
3. Deployment failed silently

**Diagnosis:**
```bash
# Check all regions
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=-

# Check deployment logs
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/AgentEngine"' \
  --project=perception-with-intent \
  --limit=20
```

### Agent Fails to Load Sub-Agents

**Symptom:** Logs show "Failed to load agent config: agent_1_source_harvester.yaml"

**Common Causes:**
- YAML config path is wrong in `agent_0_root_orchestrator.yaml`
- Agent config files not included in deployment package

**Solution:**
```bash
# Verify all agent configs exist
ls -la app/perception_agent/agents/*.yaml

# Check root orchestrator sub_agents list
cat app/perception_agent/agents/agent_0_root_orchestrator.yaml | grep -A 20 "sub_agents:"
```

### Telemetry Not Showing Up

**Symptom:** No traces or metrics in Cloud Console

**Diagnosis:**
```bash
# Check if telemetry is enabled in agent_engine_app.py
grep -A 10 "enable_cloud_trace" agent_engine_app.py

# Verify IAM permissions for logging/monitoring
gcloud projects get-iam-policy perception-with-intent \
  --filter="bindings.role:roles/logging.logWriter" \
  --flatten="bindings[].members"
```

**Solution:**
Ensure `agent_engine_app.py` has:
```python
telemetry.enable_cloud_trace(
    project_id="perception-with-intent",
    service_name="perception-agents",
    service_version="1.0.0"
)
```

---

## Updating Deployed Agent Engine

### Redeploying After Code Changes

When agent code or configs change:

```bash
# 1. Update code locally
git pull origin main

# 2. Re-run deployment script
export VERTEX_PROJECT_ID="perception-with-intent"
export VERTEX_LOCATION="us-central1"
./scripts/deploy_agent_engine.sh

# 3. Verify new version deployed
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1 \
  --format="value(updateTime)"
```

**Note:** Redeployment updates the existing Agent Engine instance. No need to delete/recreate.

### Rolling Back

To revert to a previous version:

```bash
# 1. Checkout previous commit
git checkout <previous-commit-hash>

# 2. Redeploy
./scripts/deploy_agent_engine.sh

# 3. Return to main
git checkout main
```

---

## Agent Engine vs Local Development

### Local Development (For Testing)

**Start Local ADK Server:**
```bash
# From project root
python agent_engine_app.py
```

**Characteristics:**
- ✅ Fast iteration (no deploy wait)
- ✅ Easy debugging (local logs)
- ❌ No Cloud Trace/Monitoring
- ❌ No A2A Protocol (direct Python calls)
- ❌ Different behavior than production

**Use For:**
- Testing individual agent logic
- Debugging tool implementations
- Quick prototyping

### Agent Engine Deployment (Production)

**Deploy to Vertex AI:**
```bash
./scripts/deploy_agent_engine.sh
```

**Characteristics:**
- ✅ Real A2A Protocol
- ✅ Full Cloud Trace/Monitoring
- ✅ Production-identical behavior
- ❌ Slower iteration (2-3 min deploy)
- ❌ Requires GCP quota/permissions

**Use For:**
- E2E testing
- Production deployments
- Validating A2A communication
- Performance/scaling tests

---

## Next Steps

After successful Agent Engine deployment:

1. **Test E2E Ingestion**
   - Use `scripts/run_ingestion_via_agent_engine.sh`
   - Verify data lands in Firestore
   - Check Cloud Logging for full trace

2. **Monitor Agent Performance**
   - Cloud Console > Vertex AI > Agents
   - View request latency, error rates
   - Set up alerts for failures

3. **Configure MCP Integration**
   - Ensure `MCP_BASE_URL` env var set to Cloud Run URL
   - Test agent → MCP → Firestore flow
   - Verify no localhost fallbacks

---

**Last Updated:** 2025-11-15
**Phase:** Agent Engine Deployment + E2E Ingestion
**Status:** Deployment script updated, documentation created
**Next:** Deploy Agent Engine and run E2E ingestion test
