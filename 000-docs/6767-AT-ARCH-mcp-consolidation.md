# Perception With Intent - MCP Service Consolidation

**Document ID:** 6767-AT-ARCH-mcp-consolidation
**Version:** 1.0
**Date:** 2025-11-14
**Phase:** MCP Consolidation + Cleanup
**Category:** Architecture

---

## Executive Summary

Perception uses **exactly ONE** MCP HTTP service for all external integrations. There are no demo servers, sample MCPs, or background task services. This document establishes the single source of truth for MCP architecture, deployment, and usage.

**Key Facts:**
- **Service Location:** `app/mcp_service/`
- **Framework:** FastAPI
- **Deployment Target:** Cloud Run service `perception-mcp`
- **Local Port:** 8080
- **Production URL:** `https://perception-mcp-[hash]-uc.a.run.app`
- **Ingress:** `internal-and-cloud-load-balancing` (backend-only)
- **Authentication:** No unauthenticated access (IAM-based)

---

## The One MCP Service

### Service Architecture

```
Perception MCP Service (app/mcp_service/)
│
├── main.py                    # FastAPI app entrypoint
├── routers/
│   ├── rss.py                 # fetch_rss_feed tool
│   ├── api.py                 # fetch_api_feed tool
│   ├── webpage.py             # fetch_webpage tool
│   ├── storage.py             # store_articles, log_ingestion_run tools
│   ├── briefs.py              # generate_brief tool
│   ├── logging.py             # log_ingestion_run tool
│   └── notifications.py       # send_notification tool (future)
│
├── requirements.txt           # Python dependencies
└── Dockerfile                 # Cloud Run containerization (auto-generated)
```

### MCP Tools Implemented

| Tool | Router | Endpoint | Status |
|------|--------|----------|--------|
| `fetch_rss_feed` | rss.py | POST /mcp/tools/fetch_rss_feed | ✅ Production |
| `fetch_api_feed` | api.py | POST /mcp/tools/fetch_api_feed | ⚠️ Stub |
| `fetch_webpage` | webpage.py | POST /mcp/tools/fetch_webpage | ⚠️ Stub |
| `store_articles` | storage.py | POST /mcp/tools/store_articles | ⚠️ Stub |
| `generate_brief` | briefs.py | POST /mcp/tools/generate_brief | ⚠️ Stub |
| `log_ingestion_run` | logging.py | POST /mcp/tools/log_ingestion_run | ⚠️ Stub |
| `send_notification` | notifications.py | POST /mcp/tools/send_notification | ⚠️ Future |

**Note:** Stubs return structurally correct fake data for development. Real implementations will be added in future phases.

---

## Network Posture

### Local Development

```bash
# Start MCP service locally
cd app/mcp_service
uvicorn main:app --reload --port 8080

# Service available at
http://localhost:8080

# Health check
curl http://localhost:8080/health

# API docs
http://localhost:8080/docs
```

### Production Deployment

**Cloud Run Configuration:**
```yaml
Service Name: perception-mcp
Project: perception-with-intent
Region: us-central1
Platform: managed
Service Account: mcp-service@perception-with-intent.iam.gserviceaccount.com
Ingress: internal-and-cloud-load-balancing
Authentication: No unauthenticated access
Memory: 512Mi
CPU: 1
Min Instances: 0
Max Instances: 10
Port: 8080
```

**Deployment Command:**
```bash
gcloud run deploy perception-mcp \
  --source app/mcp_service \
  --region us-central1 \
  --project perception-with-intent \
  --ingress internal-and-cloud-load-balancing \
  --no-allow-unauthenticated
```

**CI/CD:** GitHub Actions workflow `.github/workflows/deploy-mcp.yml`

---

## Who Calls the MCP Service

### 1. Perception Agents (Primary Callers)

Agents running in Vertex AI Agent Engine call MCP tools via HTTP:

```python
# In agent_1_tools.py
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8080")

async def fetch_rss(feed_url: str):
    endpoint = f"{MCP_BASE_URL}/mcp/tools/fetch_rss_feed"
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json={"feed_url": feed_url})
        return response.json()
```

**Environment Variables:**
- **Local:** `MCP_BASE_URL=http://localhost:8080`
- **Staging:** `MCP_BASE_URL=https://perception-mcp-staging-[hash]-uc.a.run.app`
- **Production:** `MCP_BASE_URL=https://perception-mcp-[hash]-uc.a.run.app`

### 2. Backend API (Future)

Optional backend API may call MCP tools for ad-hoc queries:

```python
# Future: Backend API calling MCP
import httpx

async def query_rss_feed(feed_url: str):
    response = await httpx.post(
        f"{MCP_BASE_URL}/mcp/tools/fetch_rss_feed",
        json={"feed_url": feed_url}
    )
    return response.json()
```

### 3. Dashboard (NEVER)

The Firebase dashboard **NEVER** calls MCP directly. Dashboard uses:
- Firebase Cloud Functions for backend logic
- Firestore for data reads
- Real-time subscriptions for live updates

**Why No Direct MCP Access:**
- MCP is backend-only (internal ingress)
- Dashboard is public-facing
- Security: prevent client-side exposure of internal services

---

## Removed/Archived MCPs

**Status:** No legacy or demo MCP services found in this repository.

**Verification:**
```bash
# Searched for extra MCP services
find . -type d -name "*mcp*" | grep -v ".venv" | grep -v node_modules
# Result: Only app/mcp_service/ exists

# Searched for FastAPI apps outside app/mcp_service
find . -name "main.py" | grep -v ".venv"
# Result: app/main.py (JVP agent entrypoint), app/mcp_service/main.py (MCP service)
```

**Conclusion:** Repository is clean. No fake servers, demo MCPs, or background services exist.

---

## Development Workflow

### Starting the MCP Service

```bash
# Terminal 1: Start MCP service
cd /home/jeremy/000-projects/perception
source .venv/bin/activate
cd app/mcp_service
uvicorn main:app --reload --port 8080

# Terminal 2: Test health
curl http://localhost:8080/health

# Expected output:
{
  "status": "healthy",
  "service": "mcp-service",
  "version": "1.0.0",
  "timestamp": "2025-11-14T12:00:00Z"
}
```

### Testing MCP Tools

```bash
# Test fetch_rss_feed
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://techcrunch.com/feed/",
    "time_window_hours": 24,
    "max_items": 10
  }'

# View API docs
open http://localhost:8080/docs
```

### Running Agent Tests with MCP

```bash
# Start MCP service first
cd app/mcp_service && uvicorn main:app --reload --port 8080 &

# Run agent tests
python scripts/run_ingestion_once.py --verbose

# Or run specific agent
python -c "
from app.perception_agent.tools.agent_1_tools import harvest_all_sources
import asyncio
result = asyncio.run(harvest_all_sources())
print(f'Harvested {len(result[\"articles\"])} articles')
"
```

---

## CI/CD Integration

### Deployment Workflow

**File:** `.github/workflows/deploy-mcp.yml`

**Trigger:** Manual workflow dispatch

**Steps:**
1. Print deployment targets (project, region, service name)
2. Authenticate to Google Cloud (WIF)
3. Deploy to Cloud Run from `app/mcp_service/`
4. Get service URL
5. Test health endpoint (authenticated)
6. Output deployment summary

**Environment:**
- **Staging:** For testing before production
- **Production:** Live service for agents

### Smoke Tests

**File:** `.github/workflows/ci-smoke.yml`

**MCP Service Checks:**
```yaml
- name: Install MCP Dependencies
  run: pip install -r app/mcp_service/requirements.txt

- name: Compile MCP Service
  run: python -m compileall app/mcp_service -q

- name: Test MCP Import
  run: python -c "from app.mcp_service.main import app; print('✅ MCP service imports OK')"

- name: Test Uvicorn
  run: cd app/mcp_service && uvicorn main:app --help
```

---

## Security Considerations

### IAM and Service Accounts

**MCP Service Account:**
```
mcp-service@perception-with-intent.iam.gserviceaccount.com
```

**Permissions:**
- Firestore read/write
- Cloud Storage read
- Secret Manager access (for API keys)
- Cloud Logging write

### Ingress Control

**Setting:** `internal-and-cloud-load-balancing`

**What This Means:**
- ✅ Accessible from within GCP (Agent Engine)
- ✅ Accessible via Cloud Load Balancer (for backend API)
- ❌ NOT accessible from public internet
- ❌ NOT accessible from Firebase Dashboard (client-side)

### Authentication

**Setting:** `--no-allow-unauthenticated`

**What This Means:**
- All requests must include IAM bearer token
- Agents authenticate via Agent Engine service account
- No anonymous access allowed

**Example Authenticated Request:**
```bash
# Get bearer token
TOKEN=$(gcloud auth print-identity-token)

# Make authenticated request
curl -H "Authorization: Bearer $TOKEN" \
  https://perception-mcp-[hash]-uc.a.run.app/health
```

---

## Monitoring & Observability

### Structured Logging

All MCP endpoints emit JSON logs:

```json
{
  "severity": "INFO",
  "message": "Incoming request",
  "method": "POST",
  "path": "/mcp/tools/fetch_rss_feed",
  "client_ip": "10.128.0.5"
}
```

### Key Metrics

- **Request Count:** Total MCP tool invocations
- **Latency:** Per-tool response time
- **Error Rate:** Failed requests per tool
- **Tool Usage:** Which tools are most called

### Cloud Logging Queries

```bash
# View all MCP logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=perception-mcp" --limit=50

# View errors only
gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=perception-mcp AND severity>=ERROR' --limit=20

# View specific tool usage
gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=perception-mcp AND jsonPayload.path="/mcp/tools/fetch_rss_feed"' --limit=10
```

---

## Troubleshooting

### MCP Service Not Starting

**Symptom:** `uvicorn main:app` fails

**Check:**
```bash
cd app/mcp_service
python -c "from main import app; print('OK')"
```

**Common Causes:**
- Missing dependencies: `pip install -r requirements.txt`
- Import errors: Check router imports in main.py
- Port already in use: `lsof -i :8080` and kill process

### Agents Can't Reach MCP

**Symptom:** `Connection refused to http://localhost:8080`

**Check:**
```bash
# Is MCP running?
curl http://localhost:8080/health

# Is MCP_BASE_URL set correctly?
echo $MCP_BASE_URL
```

**Fix:**
```bash
# Start MCP service
cd app/mcp_service && uvicorn main:app --reload --port 8080 &

# Set environment variable
export MCP_BASE_URL=http://localhost:8080
```

### Production MCP Returns 403

**Symptom:** `403 Forbidden` from Cloud Run

**Cause:** Missing IAM authentication

**Fix:**
```bash
# Get bearer token
TOKEN=$(gcloud auth print-identity-token)

# Use token in request
curl -H "Authorization: Bearer $TOKEN" \
  https://perception-mcp-[hash]-uc.a.run.app/health
```

---

## Future AAR Placeholder

### TODO: Production Readiness (Phase 6+)

- [ ] **Replace MCP Stubs with Real Implementations**
  - [ ] Implement real Firestore writes in storage.py
  - [ ] Implement real Gemini calls in briefs.py
  - [ ] Add real web scraping in webpage.py and api.py

- [ ] **Add OpenTelemetry Tracing**
  - [ ] Instrument FastAPI with OpenTelemetry
  - [ ] Add distributed tracing for MCP → Agents flow
  - [ ] Create trace dashboards in Cloud Monitoring

- [ ] **Implement Rate Limiting**
  - [ ] Add per-tool rate limits (e.g., 100 req/min for fetch_rss_feed)
  - [ ] Implement backpressure for expensive operations
  - [ ] Add circuit breakers for external API calls

- [ ] **Add Caching Layer**
  - [ ] Cache RSS feed responses (5-10 min TTL)
  - [ ] Implement cache invalidation strategies
  - [ ] Add cache hit/miss metrics

- [ ] **Harden Security**
  - [ ] Restrict CORS to agent endpoints only (remove `allow_origins=["*"]`)
  - [ ] Add request validation middleware
  - [ ] Implement API key rotation for external services
  - [ ] Add DDoS protection via Cloud Armor

- [ ] **Scale Testing**
  - [ ] Load test with 1000+ concurrent requests
  - [ ] Verify auto-scaling to max instances
  - [ ] Measure cold start latency
  - [ ] Optimize container startup time

---

## Summary

### The One MCP Rule

**Perception uses exactly ONE MCP HTTP service:**
- **Code:** `app/mcp_service/`
- **Deployment:** Cloud Run service `perception-mcp`
- **Port:** 8080 (local and Cloud Run)
- **Ingress:** Backend-only (internal + LB)
- **Authentication:** IAM-based (no anonymous access)

### What's NOT in This Repo

- ❌ No demo MCP servers
- ❌ No sample/test MCP services
- ❌ No background task workers pretending to be MCPs
- ❌ No multiple FastAPI apps competing to be "the MCP"

### What IS in This Repo

- ✅ One production MCP service at `app/mcp_service/`
- ✅ One JVP agent entrypoint at `app/main.py` (for running agents locally)
- ✅ Clean CI/CD deploying only the real MCP service
- ✅ Documentation pointing to the correct MCP service and port

---

**Last Updated:** 2025-11-14
**Phase:** MCP Consolidation + Cleanup
**Status:** Repository verified clean - no fake servers exist
**Next:** Replace MCP stubs with real implementations (Phase 6+)
