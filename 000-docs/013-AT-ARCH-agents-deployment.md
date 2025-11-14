# Perception With Intent - Agent Deployment Architecture

**Version:** 1.0
**Date:** 2025-11-14
**Phase:** 3 (Agent Cards + Runtime Config Complete)

---

## Overview

This document describes how the 8 Perception agents are deployed to Vertex AI Agent Engine and how they communicate with each other and with external systems.

## Deployment Model

### Current: Monolithic Deployment (Phase 3-6)

All 8 agents are deployed as a **single Vertex AI Agent Engine application**.

```
Vertex AI Agent Engine Deployment
│
└── App: perception-agent-engine
    │
    ├── Agent 0: Orchestrator (root)
    │   ├── Sub-Agent 1: Source Harvester
    │   ├── Sub-Agent 2: Topic Manager
    │   ├── Sub-Agent 3: Relevance & Ranking
    │   ├── Sub-Agent 4: Brief Writer
    │   ├── Sub-Agent 5: Alert & Anomaly
    │   ├── Sub-Agent 6: Validator
    │   └── Sub-Agent 7: Storage Manager
    │
    └── Communication: ADK internal A2A (same process)
```

**Benefits:**
- Simpler deployment and debugging
- Lower latency (in-process communication)
- Single deployment artifact
- Easier development iteration

**Limitations:**
- Agents share same resource limits
- Cannot scale agents independently
- All agents restart on any code change

---

## Future: Distributed Deployment (Phase 7+)

Each agent can be deployed as an **independent Agent Engine instance** communicating via A2A Protocol over HTTP.

```
Cloud Scheduler → Agent 0 (Orchestrator)
                      ↓ (A2A HTTP)
    ┌─────────────────┼─────────────────┐
    ↓                 ↓                 ↓
Agent 1           Agent 2           Agent 3
(Harvester)    (Topic Mgr)       (Relevance)
    ↓                                   ↓
Agent 4                           Agent 5
(Brief)                          (Alerts)
    ↓                                   ↓
Agent 6 ───────────────────────────→ Agent 7
(Validator)                      (Storage)
```

**Benefits:**
- Independent scaling per agent
- Deploy updates to individual agents
- Isolate failures (one agent crash doesn't affect others)
- Optimize resources per agent workload

**Migration Path:**
1. Keep agent YAML configs identical
2. Deploy each agent as separate Agent Engine app
3. Update orchestrator sub_agents config to use HTTP A2A endpoints
4. Test each agent independently
5. Gradually migrate from monolithic to distributed

---

## Agent Runtime Architecture

### File Structure

```
app/
├── agent_engine_app.py                  # Main entrypoint
│
└── perception_agent/
    ├── agents/                          # Agent YAML configs
    │   ├── agent_0_orchestrator.yaml
    │   ├── agent_1_source_harvester.yaml
    │   ├── agent_2_topic_manager.yaml
    │   ├── agent_3_relevance_ranking.yaml
    │   ├── agent_4_brief_writer.yaml
    │   ├── agent_5_alert_anomaly.yaml
    │   ├── agent_6_validator.yaml
    │   └── agent_7_storage_manager.yaml
    │
    ├── tools/                           # Agent tools (Python)
    │   ├── agent_0_tools.py
    │   ├── agent_1_tools.py
    │   ├── agent_2_tools.py
    │   ├── agent_3_tools.py
    │   ├── agent_4_tools.py
    │   ├── agent_5_tools.py
    │   ├── agent_6_tools.py
    │   └── agent_7_tools.py
    │
    └── prompts/                         # (Optional) Prompt templates
```

### Agent Loading Sequence

1. **Agent Engine starts** → calls `agent_engine_app.py`
2. **Load orchestrator** → reads `agent_0_orchestrator.yaml`
3. **Load sub-agents** → orchestrator config references 7 sub-agent YAMLs
4. **Initialize tools** → each agent loads its tools module
5. **Ready** → orchestrator exposes HTTP endpoint for invocation

---

## Agent Communication

### Internal A2A (Monolithic)

Agents communicate via ADK's internal A2A mechanism:

```python
# Agent 0 calls Agent 1 (Source Harvester)
result = await self.call_sub_agent(
    agent_name="perception_source_harvester",
    message={"action": "harvest", "run_id": run_id}
)
```

**Characteristics:**
- In-process function calls
- Sub-microsecond latency
- Automatic serialization/deserialization
- Built-in error handling

### HTTP A2A (Distributed - Future)

Agents communicate via A2A Protocol over HTTP:

```python
# Agent 0 calls Agent 1 via HTTP
result = await self.call_agent(
    endpoint="https://agent-1-harvester-xxx.run.app/a2a",
    message={"action": "harvest", "run_id": run_id}
)
```

**Characteristics:**
- HTTP/HTTPS requests
- ~10-50ms latency
- Standard AgentCard + A2A Protocol
- Service-to-service authentication

---

## External Integrations

### MCP Tools (Cloud Run Services)

Agents call MCP tools via HTTP:

```
Agent 1 (Harvester)
    ↓ HTTP POST
MCP: NewsIngestionMCP
    ↓
Fetches RSS feed
    ↓
Returns articles
    ↑
Agent 1 (Harvester)
```

**MCP Tool Endpoints (Phase 4+):**
- `fetch_rss_feed` → NewsIngestionMCP
- `fetch_api_feed` → NewsIngestionMCP
- `fetch_webpage` → NewsIngestionMCP
- `store_articles` → StorageMCP
- `store_brief` → StorageMCP
- `log_ingestion_run` → StorageMCP

### Firestore Access

Agents read/write Firestore via tools:

```
Agent 7 (Storage Manager)
    ↓
agent_7_tools.py
    ↓
Firestore Client SDK
    ↓
/articles/{articleId}
/briefs/{briefId}
/ingestion_runs/{runId}
```

**Access Pattern:**
- Tools modules use Firestore SDK
- Service account authentication
- Batch writes for efficiency
- Error handling with retries

---

## Deployment Workflow

### Local Development

```bash
# Verify agent configs
cd app
python agent_engine_app.py

# Expected output:
# ✓ All 8 agent YAML configs found
# ✓ Directory structure verified
```

### Deploy to Agent Engine (Future)

```bash
# TODO: Replace with actual ADK deployment commands

# Option 1: ADK CLI
adk deploy \
  --project perception-with-intent \
  --location us-central1 \
  --agent-config app/perception_agent/agents/agent_0_orchestrator.yaml

# Option 2: Terraform (recommended for production)
cd terraform/
terraform apply -target=google_agent_engine_deployment.perception
```

---

## Scaling & Performance

### Monolithic Deployment

**Resource Limits (per Agent Engine instance):**
- CPU: 2-8 vCPUs
- Memory: 4-32 GB
- Concurrent requests: 1-1000
- Cold start: ~5-15 seconds

**Scaling:**
- Horizontal: Multiple instances (load balanced)
- Vertical: Increase CPU/memory per instance
- Autoscaling: Based on request rate

### Distributed Deployment (Future)

**Per-Agent Scaling:**
- Agent 1 (Harvester): 2-10 instances (CPU-intensive)
- Agent 3 (Relevance): 4-20 instances (Gemini calls)
- Agent 4 (Brief Writer): 1-5 instances (less frequent)
- Agent 7 (Storage): 2-10 instances (I/O bound)

**Cost Optimization:**
- Scale each agent independently
- Use Spot/Preemptible for non-critical agents
- Cache Agent Engine instances (reduce cold starts)

---

## Observability

### OpenTelemetry Tracing

**Span Structure:**
```
[Orchestrator] daily_ingestion_run
    ├── [Source Harvester] harvest_sources
    │   ├── [MCP] fetch_rss_feed (techcrunch)
    │   ├── [MCP] fetch_rss_feed (theverge)
    │   └── [MCP] fetch_rss_feed (bbc)
    ├── [Relevance] score_articles
    │   └── [Gemini] batch_analyze_relevance
    ├── [Brief Writer] generate_brief
    │   └── [Gemini] create_executive_summary
    ├── [Validator] validate_data
    └── [Storage] persist_to_firestore
        ├── [Firestore] batch_write_articles
        └── [Firestore] write_brief
```

**Trace Attributes:**
- `agent.name` - Agent identifier
- `agent.version` - Agent version
- `run.id` - Ingestion run ID
- `articles.count` - Number of articles processed
- `brief.date` - Brief date
- `error.type` - Error category if failed

### Metrics (Cloud Monitoring)

**Per-Agent Metrics:**
- `agent.requests.count` - Total requests
- `agent.requests.latency` - p50, p95, p99
- `agent.errors.count` - Errors by type
- `agent.tokens.used` - Gemini token consumption

**System Metrics:**
- `ingestion_run.duration_ms` - End-to-end runtime
- `articles.ingested.count` - Articles per run
- `articles.filtered.count` - Articles passing relevance
- `briefs.generated.count` - Briefs created
- `alerts.triggered.count` - Alerts fired

### Logging

**Structured JSON Logs:**
```json
{
  "severity": "INFO",
  "timestamp": "2025-11-14T12:00:00Z",
  "agent_name": "perception_orchestrator",
  "run_id": "run_1731585600",
  "action": "start_ingestion",
  "message": "Starting daily ingestion run"
}
```

**Log Levels:**
- `DEBUG` - Tool function calls, intermediate results
- `INFO` - Agent lifecycle events, run status
- `WARNING` - Validation failures, retryable errors
- `ERROR` - Critical failures, data loss

---

## Security

### Authentication

**Agent-to-Agent (Monolithic):**
- In-process (no auth required)

**Agent-to-Agent (Distributed - Future):**
- Service account impersonation
- SPIFFE IDs for mutual TLS
- IAM-based authorization

**Agent-to-MCP:**
- Service account tokens
- HTTP Bearer authentication
- Restricted to allowed MCP endpoints

**Agent-to-Firestore:**
- Service account with Firestore roles
- Least privilege (read/write only needed collections)

### Secrets Management

**All secrets in Secret Manager:**
- MCP endpoint URLs
- API keys (if needed)
- Service account keys (if not using Workload Identity)

**Access Pattern:**
```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
secret_name = f"projects/{PROJECT_ID}/secrets/mcp-endpoint/versions/latest"
response = client.access_secret_version(request={"name": secret_name})
mcp_url = response.payload.data.decode("UTF-8")
```

---

## Disaster Recovery

### Backup Strategy

**Agent Configs:**
- Git version control (already backed up)
- Tagged releases for rollback

**Firestore Data:**
- Automatic daily backups (Firestore managed)
- Point-in-time recovery (PITR) enabled
- Export to GCS weekly

### Rollback Plan

**If deployment fails:**
1. Agent Engine auto-reverts to previous version
2. Monitor error rates in Cloud Logging
3. Manual rollback via ADK if needed

**If data corruption:**
1. Identify corrupted ingestion run(s)
2. Delete affected documents from Firestore
3. Re-run ingestion for affected dates
4. Validate briefs regenerate correctly

---

## Testing Strategy

### Unit Tests (Per Agent)

Test each agent's tools in isolation:

```bash
# Agent 1 tools
pytest app/perception_agent/tools/test_agent_1_tools.py

# Agent 3 tools
pytest app/perception_agent/tools/test_agent_3_tools.py
```

### Integration Tests (End-to-End)

Test full ingestion workflow:

```bash
# Trigger orchestrator with test data
python tests/integration/test_daily_ingestion.py

# Verify:
# - Articles stored in Firestore
# - Brief generated
# - Ingestion run logged
```

### A2A Communication Tests

Test agent-to-agent calls:

```bash
# Monolithic (local)
python tests/a2a/test_orchestrator_to_harvester.py

# Distributed (staging)
python tests/a2a/test_http_a2a_protocol.py
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] All 8 agent YAML configs validated
- [ ] All tools modules have stubs or implementations
- [ ] OpenTelemetry instrumentation added
- [ ] Secrets configured in Secret Manager
- [ ] Firestore security rules deployed
- [ ] MCP tools deployed and tested

### Deployment

- [ ] Agent Engine app deployed to staging
- [ ] Smoke test: trigger orchestrator
- [ ] Verify traces in Cloud Trace
- [ ] Check logs in Cloud Logging
- [ ] Validate metrics in Cloud Monitoring

### Post-Deployment

- [ ] Monitor error rates for 24 hours
- [ ] Verify daily ingestion runs succeed
- [ ] Check Firestore for expected data
- [ ] Dashboard displays new data correctly

---

## Known Limitations (Phase 3)

1. **Tools are stubs** - No actual implementation yet
   - Fix: Implement tools in Phase 4-5

2. **No MCP connections** - Agents can't fetch real data
   - Fix: Deploy MCP tools in Phase 4

3. **No Firestore integration** - Can't read/write database
   - Fix: Add Firestore SDK calls in Phase 5

4. **ADK entrypoint incomplete** - Can't deploy to Agent Engine yet
   - Fix: Wire up ADK loader/runner functions

5. **No observability** - No traces, metrics, or structured logs
   - Fix: Add OpenTelemetry instrumentation in Phase 5

---

## Next Steps

### Phase 4: MCP Tool Architecture
- Design 7 MCP Cloud Run services
- Define HTTP API contracts
- Document tool schemas

### Phase 5: First MCP Tool Implementation
- Implement `fetch_rss_feed` MCP tool
- Deploy to Cloud Run
- Wire to Agent 1 (Source Harvester)
- Add OpenTelemetry tracing

### Phase 6: Pipeline Documentation
- Visualize 8-agent workflow
- Document data flow
- Error handling paths

### Phase 7: Working Ingestion
- Complete all MCP tool implementations
- Add Firestore integration
- End-to-end test
- Deploy to production

---

**Last Updated:** 2025-11-14
**Status:** Phase 3 Complete - Agent Cards + Runtime Config Ready
**Next:** Phase 4 (MCP Tool Architecture)
