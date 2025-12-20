# MCP Cloud Run Runtime Architecture

**Version:** 1.0
**Date:** 2025-11-14
**Purpose:** Runtime architecture for MCP service on Cloud Run with backend-only access

---

## Overview

The **MCP (Model Context Protocol) service** is deployed to Google Cloud Run as a **backend-only service** that provides tools for Vertex AI agents. It is NOT accessible to the public internet or the React dashboard.

**Key Principles:**
- MCP is backend-only (internal/internal+LB ingress)
- MCP is called by Agent Engine only
- MCP does NOT call the dashboard
- MCP does NOT have public internet access

---

## Cloud Run Service Configuration

### Service Details

| Field | Value | Source |
|-------|-------|--------|
| **Service Name** | `perception-mcp` | Hardcoded in deploy-mcp.yml |
| **Project ID** | `perception-with-intent` | env.GCP_PROJECT_ID |
| **Region** | `us-central1` | env.GCP_REGION |
| **Platform** | Cloud Run (fully managed) | gcloud run deploy |
| **Service Account** | `mcp-service@perception-with-intent.iam.gserviceaccount.com` | env.MCP_SERVICE_ACCOUNT |

### Runtime Configuration

| Setting | Value | Purpose |
|---------|-------|---------|
| **Ingress** | `internal-and-cloud-load-balancing` | Backend-only access |
| **Auth** | `--no-allow-unauthenticated` | Requires authentication |
| **Memory** | 512Mi | Sufficient for RSS parsing |
| **CPU** | 1 vCPU | Light processing |
| **Min Instances** | 0 | Scale to zero when idle |
| **Max Instances** | 10 | Auto-scale under load |
| **Timeout** | 300s (5 minutes) | RSS fetch + processing |
| **Port** | 8080 | Cloud Run standard |

### Environment Variables (Runtime)

| Variable | Value | Purpose |
|----------|-------|---------|
| `ENVIRONMENT` | staging / production | Deployment environment |
| `MCP_SERVICE_NAME` | perception-mcp | Self-identification |

---

## URL Pattern

### Cloud Run URL Structure

After deployment, Cloud Run assigns a stable URL:

```
https://perception-mcp-<hash>-uc.a.run.app
```

Where:
- `perception-mcp` = Service name
- `<hash>` = Cloud Run assigned hash (stable per service)
- `uc` = Region abbreviation (us-central1)
- `a.run.app` = Cloud Run domain

**Example:**
```
https://perception-mcp-abc123-uc.a.run.app
```

This URL is:
- ✅ Stable across deployments (does not change)
- ✅ HTTPS only (TLS 1.2+)
- ❌ NOT publicly accessible (requires authentication)
- ❌ NOT accessible from React dashboard (backend-only)

---

## MCP_BASE_URL Configuration

### Environment Variable: `MCP_BASE_URL`

This is the **single source of truth** for the MCP service URL used by agents.

| Environment | Value | Set Via |
|-------------|-------|---------|
| **Local Development** | `http://localhost:8080` | `.env.local` or shell env |
| **Cloud Run (Production)** | `https://perception-mcp-<hash>-uc.a.run.app` | Agent Engine runtime config |

### Local Development

For local development, set in `.env.local`:

```bash
MCP_BASE_URL=http://localhost:8080
```

Or export in shell:

```bash
export MCP_BASE_URL=http://localhost:8080
uvicorn main:app --port 8080
```

### Production (Cloud Run)

For production, the Agent Engine will be configured with:

```bash
MCP_BASE_URL=https://perception-mcp-<hash>-uc.a.run.app
```

This is set via:
- Agent Engine deployment configuration (agent YAML or runtime env vars)
- Secret Manager (future enhancement)
- Cloud Run service env vars (not recommended for cross-service URLs)

**IMPORTANT:** Never commit the production URL to git. Use environment-specific config.

---

## End-to-End Path (MCP)

### Deployment Flow

```
1. GitHub Actions (deploy-mcp.yml)
   ↓
2. WIF Authentication
   ↓
3. gcloud run deploy perception-mcp
   ↓
4. Cloud Run builds container from app/mcp_service
   ↓
5. Cloud Run assigns URL: https://perception-mcp-<hash>-uc.a.run.app
   ↓
6. Service starts with internal-only ingress
```

### Runtime Flow

```
1. Agent 1 (Source Harvester) needs to fetch RSS
   ↓
2. Agent 1 tools read MCP_BASE_URL from env
   ↓
3. Agent 1 calls:
      POST {MCP_BASE_URL}/tools/fetch_rss_feed
      Body: {"feed_url": "...", "time_window_hours": 24}
   ↓
4. MCP service (Cloud Run) receives request
   ↓
5. MCP fetches RSS via httpx, parses with feedparser
   ↓
6. MCP normalizes articles to standard schema
   ↓
7. MCP returns JSON:
      {"articles": [...], "metadata": {...}}
   ↓
8. Agent 1 receives articles and processes them
```

### Authentication Flow

```
Agent Engine (Cloud Run)
    ↓ (service-to-service auth)
Cloud Run (perception-mcp)
    ↓ (internal network)
External RSS feed servers
```

- Agent Engine → MCP: Uses service account identity tokens
- MCP → RSS feeds: HTTPS with no authentication (public RSS)

---

## Network Architecture

### Ingress Configuration

**Setting:** `--ingress internal-and-cloud-load-balancing`

This means:
- ✅ Accessible from other Cloud Run services (Agent Engine)
- ✅ Accessible from Cloud Load Balancer (if configured)
- ✅ Accessible from VPC (internal network)
- ❌ NOT accessible from public internet
- ❌ NOT accessible from React dashboard (client-side)

### Why Backend-Only?

1. **Security:** MCP has no user-facing data, only tool execution
2. **Performance:** No CORS overhead, no public DDoS risk
3. **Cost:** Internal traffic is cheaper than egress
4. **Simplicity:** No need for API keys, rate limiting, etc.

### Service Account Permissions

The MCP service account (`mcp-service@perception-with-intent.iam.gserviceaccount.com`) needs:

| Permission | Purpose |
|------------|---------|
| `roles/run.invoker` (on itself) | Self-invocation for health checks |
| `roles/secretmanager.secretAccessor` | Access secrets (future) |
| `roles/logging.logWriter` | Write structured logs |
| `roles/cloudtrace.agent` | Send trace data (future) |

**NOT needed:**
- ❌ Firestore access (agents handle that)
- ❌ BigQuery access (agents handle that)
- ❌ Storage bucket access (agents handle that)

MCP is **dumb** - it just fetches RSS, parses it, and returns JSON. Agents are **smart** - they decide what to do with the data.

---

## Configuration Files

### `.env.local` (Local Development)

Create this file for local development:

```bash
# MCP Service Configuration (Local)
MCP_BASE_URL=http://localhost:8080
ENVIRONMENT=development

# Optional: Enable debug logging
LOG_LEVEL=DEBUG
```

**IMPORTANT:** This file is `.gitignore`d - never commit it.

### `.env.example` (Template)

Create this file to show required env vars:

```bash
# MCP Service Configuration
MCP_BASE_URL=http://localhost:8080  # Local dev
# MCP_BASE_URL=https://perception-mcp-<hash>-uc.a.run.app  # Production (set via runtime config)

ENVIRONMENT=development  # development | staging | production

# Optional: Logging
LOG_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR
```

---

## Deployment Workflow

### Manual Deployment (GitHub Actions)

**File:** `.github/workflows/deploy-mcp.yml`

**Trigger:** Manual only (`workflow_dispatch`)

**Steps:**
1. Print deployment targets (project, region, service, ingress)
2. Authenticate via WIF
3. Deploy to Cloud Run with `--source app/mcp_service`
4. Get service URL
5. Test health endpoint (with authentication)
6. Print deployment summary

**Command:**
```bash
gcloud run deploy perception-mcp \
  --source app/mcp_service \
  --region us-central1 \
  --project perception-with-intent \
  --platform managed \
  --service-account mcp-service@perception-with-intent.iam.gserviceaccount.com \
  --ingress internal-and-cloud-load-balancing \
  --no-allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --port 8080 \
  --set-env-vars "ENVIRONMENT=production,MCP_SERVICE_NAME=perception-mcp"
```

### Local Deployment (Testing)

For local testing:

```bash
# Start MCP service locally
cd app/mcp_service
source ../../.venv/bin/activate
export MCP_BASE_URL=http://localhost:8080
uvicorn main:app --port 8080 --reload

# Test health endpoint
curl http://localhost:8080/health

# Test fetch_rss_feed
curl -X POST http://localhost:8080/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://news.ycombinator.com/rss",
    "time_window_hours": 24,
    "max_items": 10
  }'
```

---

## Monitoring & Observability

### Health Endpoint

**Endpoint:** `/health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "perception-mcp",
  "version": "1.0.0"
}
```

**Use Cases:**
- GitHub Actions health check after deployment
- Cloud Run health checks
- Agent Engine connectivity verification

### Logging

All MCP operations use structured JSON logging:

```python
logger.info(
    "RSS feed fetched",
    extra={
        "tool": "fetch_rss_feed",
        "feed_url": feed_url,
        "article_count": len(articles),
        "latency_ms": latency_ms,
        "request_id": request_id
    }
)
```

View logs:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=perception-mcp" \
  --project=perception-with-intent \
  --limit=50 \
  --format=json
```

### Metrics (Future)

Cloud Run automatically tracks:
- Request count
- Request latency (p50, p95, p99)
- Error rate
- Instance count
- CPU/memory utilization

Access via Cloud Console → Cloud Run → perception-mcp → Metrics

---

## Troubleshooting

### "Service URL not accessible"

**Symptom:** `curl https://perception-mcp-<hash>-uc.a.run.app/health` fails with 403

**Cause:** Service has `--no-allow-unauthenticated` (backend-only)

**Solution:** Use authenticated request:
```bash
TOKEN=$(gcloud auth print-identity-token)
curl -H "Authorization: Bearer $TOKEN" https://perception-mcp-<hash>-uc.a.run.app/health
```

### "Agent can't reach MCP"

**Symptom:** Agent 1 logs show "Connection refused" or timeout

**Cause:** `MCP_BASE_URL` not set or incorrect

**Solution:**
1. Check Agent Engine env vars:
   ```bash
   gcloud run services describe <agent-service> \
     --region us-central1 \
     --format="value(spec.template.spec.containers[0].env)"
   ```
2. Verify `MCP_BASE_URL` is set to correct Cloud Run URL
3. Redeploy agents with correct env var

### "MCP service crash on startup"

**Symptom:** Cloud Run shows "Service not ready" or "Container crashed"

**Cause:** Missing dependencies or incorrect port

**Solution:**
1. Check logs:
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=perception-mcp" \
     --limit=10
   ```
2. Verify `app/mcp_service/requirements.txt` has all deps
3. Verify `main:app` is correct FastAPI app name
4. Verify port 8080 is exposed in Dockerfile (if using)

---

## Future Enhancements

### Phase 6 (Planned)
- [ ] Add OpenTelemetry tracing
- [ ] Add Prometheus metrics endpoint
- [ ] Add request rate limiting
- [ ] Add circuit breaker for RSS fetch failures
- [ ] Add caching layer (Redis/Memorystore)

### Phase 7 (Planned)
- [ ] Multi-region deployment (us-central1 + us-east1)
- [ ] Load balancer configuration
- [ ] Custom domain (mcp.perception-with-intent.com)
- [ ] VPC connector for private resources

---

## Future AAR (MCP Cloud Run Deploy) – Placeholder Only

**TODO: After first successful deploy and end-to-end ingestion run, document:**

- [ ] Deployment observations
  - [ ] Build time for container
  - [ ] Cold start latency
  - [ ] First request latency
  - [ ] Memory/CPU utilization under load

- [ ] Latency/Error Metrics
  - [ ] RSS fetch latency (p50, p95, p99)
  - [ ] Parsing time per article
  - [ ] Error rate by feed source
  - [ ] Retry behavior on failures

- [ ] Naming and IAM Decisions
  - [ ] Service account permissions review
  - [ ] Ingress configuration validation
  - [ ] Network security posture
  - [ ] Cost analysis (requests, compute, egress)

- [ ] Operational Learnings
  - [ ] How often does service scale to zero?
  - [ ] How long does cold start take?
  - [ ] Any RSS feeds that consistently fail?
  - [ ] Any performance bottlenecks?

**AAR Status:** NOT YET CREATED (placeholder only)

---

**Last Updated:** 2025-11-14
**Status:** Ready for deployment
**Next:** Deploy MCP to Cloud Run and configure MCP_BASE_URL in Agent Engine
