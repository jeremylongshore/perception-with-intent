# Perception With Intent - Observability & Monitoring

**Document ID:** 6767-AT-ARCH-observability-and-monitoring
**Version:** 1.0
**Date:** 2025-11-15
**Phase:** MCP Cloud Run Validation + Observability
**Category:** Architecture

---

## Executive Summary

Perception's MCP service runs exclusively on Google Cloud Run with comprehensive observability through Cloud Logging, Cloud Run metrics, and structured request logging. This document provides verification commands, monitoring strategies, and operational checklists for maintaining service health.

**Key Facts:**
- **MCP Service:** `perception-mcp` on Cloud Run (us-central1)
- **Service URL:** `https://perception-mcp-348724539390.us-central1.run.app`
- **Logging:** Structured JSON logs in Cloud Logging
- **Metrics:** Cloud Run automatic metrics (requests, latency, errors)
- **NO Local MCP:** Localhost MCP is NOT a valid deployment or test path

---

## Observability Stack

### Cloud Logging

All MCP service logs flow to Cloud Logging with structured JSON payloads:

**Log Types:**
- **Application Logs**: Uvicorn INFO logs, custom application logs
- **Request Logs**: HTTP method, path, status code, latency
- **Error Logs**: Exceptions, stack traces (severity ERROR/CRITICAL)
- **Startup Logs**: Container startup, health probe results

**Sample Structured Log:**
```yaml
jsonPayload:
  latency_ms: 270
  message: Request completed
  method: POST
  path: /mcp/tools/fetch_rss_feed
  status_code: 200
resource:
  type: cloud_run_revision
  labels:
    service_name: perception-mcp
    location: us-central1
```

### Cloud Run Metrics

**Automatic Metrics:**
- **Request Count**: Total requests per minute
- **Request Latency**: P50, P95, P99 latency distributions
- **Error Rate**: 4xx and 5xx errors per minute
- **Container CPU**: CPU utilization percentage
- **Container Memory**: Memory usage and limits
- **Instance Count**: Active container instances

**Access Metrics:**
- Cloud Console: Cloud Run > perception-mcp > Metrics
- Metrics Explorer: `resource.type="cloud_run_revision"`

### Error Reporting

Errors logged at severity ERROR or higher automatically appear in Cloud Error Reporting:

**Monitored:**
- Application exceptions
- Import errors
- HTTP 500 errors
- Unhandled promise rejections
- Startup failures

---

## Verification Commands

### 1. Verify Service Deployment

**Command:**
```bash
gcloud run services describe perception-mcp \
  --project=perception-with-intent \
  --region=us-central1 \
  --format='value(status.url,status.conditions[0].status,status.conditions[0].reason)'
```

**Expected Output:**
```
https://perception-mcp-348724539390.us-central1.run.app  True
```

- **URL**: Service endpoint (copy this)
- **Status**: `True` = healthy, `False` = unhealthy
- **Reason**: Empty if healthy, error message if not

### 2. Test Health Endpoint

**Command:**
```bash
curl -sS https://perception-mcp-348724539390.us-central1.run.app/health | jq '.'
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "mcp-service",
  "version": "1.0.0",
  "timestamp": "2025-11-15T00:15:20.586052+00:00"
}
```

### 3. Test MCP Tool Endpoint

**Command:**
```bash
curl -sS -X POST "https://perception-mcp-348724539390.us-central1.run.app/mcp/tools/fetch_rss_feed" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_1_source_harvester",
    "run_id": "smoke_test_run",
    "user_id": "smoke-test-user",
    "feed_url": "https://news.ycombinator.com/rss",
    "time_window_hours": 24,
    "max_items": 5
  }' | jq '.article_count'
```

**Expected Output:**
```
5
```

### 4. Check Cloud Logging

**View Recent Logs:**
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp"' \
  --project=perception-with-intent \
  --limit=10 \
  --format=json
```

**View Request Logs Only:**
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp" AND jsonPayload.path="/mcp/tools/fetch_rss_feed"' \
  --project=perception-with-intent \
  --limit=5
```

**View Errors Only:**
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp" AND severity>=ERROR' \
  --project=perception-with-intent \
  --limit=10
```

**Expected:**
- Recent logs show Uvicorn startup messages
- Request logs show HTTP method, path, status 200
- No ERROR-level logs (empty response = healthy)

### 5. Check Service Status

**Get Service Details:**
```bash
gcloud run services describe perception-mcp \
  --project=perception-with-intent \
  --region=us-central1
```

**Key Fields to Check:**
- `status.url`: Service URL
- `status.latestCreatedRevisionName`: Current revision
- `spec.template.spec.containers[0].image`: Deployed container image
- `spec.template.spec.containers[0].ports[0].containerPort`: Should be 8080
- `spec.template.spec.serviceAccountName`: Service account used

---

## How to Verify MCP is Alive

**Checklist:**

1. **Deploy Check**
   ```bash
   gcloud run services describe perception-mcp \
     --project=perception-with-intent \
     --region=us-central1 \
     --format='value(status.url)'
   ```
   - If this fails with "NOT_FOUND", MCP is not deployed
   - If it returns a URL, proceed to next step

2. **Health Check**
   ```bash
   curl -sS https://perception-mcp-348724539390.us-central1.run.app/health
   ```
   - Should return HTTP 200 with `{"status": "healthy"}`
   - If 404, service is deployed but not starting correctly
   - If 502/503, service is crashing on startup

3. **Functional Check**
   - Test `fetch_rss_feed` endpoint (see command above)
   - Should return HTTP 200 with `article_count > 0`
   - If no articles, feed URL may be down (not MCP issue)

4. **Logging Check**
   ```bash
   gcloud logging read \
     'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp"' \
     --project=perception-with-intent \
     --limit=3
   ```
   - Should show recent Uvicorn logs
   - If no logs, service hasn't received requests or crashed

5. **Error Check**
   ```bash
   gcloud logging read \
     'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp" AND severity>=ERROR' \
     --project=perception-with-intent \
     --limit=5
   ```
   - Empty response = no errors (good!)
   - Any errors = investigate stack traces

---

## Production vs Development Testing

### Production Deployment (Cloud Run)

**This is the ONLY valid deployment path:**

```bash
# Deploy via gcloud
gcloud run deploy perception-mcp \
  --source app/mcp_service \
  --region us-central1 \
  --project perception-with-intent \
  --platform managed \
  --ingress all \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --port 8080
```

**Or deploy via GitHub Actions:**
```bash
gh workflow run deploy-mcp.yml \
  --repo jeremylongshore/perception-with-intent \
  --field environment=staging
```

**Testing:**
- Always test against Cloud Run URL
- Use `curl` commands shown above
- Check Cloud Logging for request logs

### Local MCP (NOT SUPPORTED)

**❌ DO NOT DO THIS:**
```bash
# WRONG - Do not run MCP locally
cd app/mcp_service
uvicorn main:app --reload --port 8080
```

**Why Not:**
- Localhost MCP is NOT a valid deployment
- Cannot test Cloud Run behavior locally
- Cloud Logging, IAM, service accounts don't work locally
- No proof of real deployment

**Instead:**
- Deploy to staging Cloud Run
- Test in cloud
- Check real Cloud Logging

---

## Monitoring Best Practices

### 1. Structured Logging

**MCP service emits structured JSON logs:**

```python
logger.info(json.dumps({
    "message": "Request completed",
    "method": request.method,
    "path": request.url.path,
    "status_code": response.status_code,
    "latency_ms": latency_ms
}))
```

**Benefits:**
- Easy filtering in Cloud Logging
- Exportable to BigQuery for analysis
- Automatic indexing on JSON fields

### 2. Request Tracing

**Future: OpenTelemetry Integration**

MCP service has OpenTelemetry dependencies installed but not yet instrumented:

```python
# TODO Phase 5: Enable OpenTelemetry
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# FastAPIInstrumentor.instrument_app(app)
```

**Benefits (when implemented):**
- End-to-end request tracing
- Distributed trace visualization
- Latency waterfall diagrams
- Cross-service dependency mapping

### 3. Error Alerting

**Set up alerts for:**
- Error rate > 5% over 5 minutes
- Request latency P99 > 2 seconds
- Container restarts > 3 in 10 minutes
- Health check failures

**Alert Channels:**
- Email to ops team
- Slack #perception-alerts
- PagerDuty for critical errors

### 4. SLO Monitoring

**Define SLOs:**
- **Availability**: 99.5% uptime (measured via health checks)
- **Latency**: P95 < 500ms for `fetch_rss_feed`
- **Error Rate**: < 1% of requests fail
- **Throughput**: Handle 100 requests/minute without scaling issues

**Monitor with:**
- Cloud Monitoring SLO dashboards
- Weekly SLO reports
- Burn rate alerts for budget violations

---

## Troubleshooting

### Service Returns 404

**Symptom:** All endpoints return 404 Not Found

**Diagnosis:**
```bash
# Check logs for startup errors
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp"' \
  --project=perception-with-intent \
  --limit=20
```

**Common Causes:**
- FastAPI app not starting (import errors)
- Router imports failing (check `from routers import ...`)
- Container crashing on startup

**Fix:**
- Check for `ImportError` or `ModuleNotFoundError` in logs
- Verify all dependencies in `requirements.txt`
- Test locally with `python -c "from main import app; print('OK')"`

### Service Returns 502/503

**Symptom:** Bad Gateway or Service Unavailable

**Diagnosis:**
```bash
# Check if containers are starting
gcloud run revisions list \
  --service=perception-mcp \
  --project=perception-with-intent \
  --region=us-central1
```

**Common Causes:**
- Container startup timeout (default 240s)
- Memory limit exceeded
- Listening on wrong port

**Fix:**
- Increase timeout: `--timeout 300`
- Increase memory: `--memory 1Gi`
- Verify `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]`

### No Logs Appearing

**Symptom:** Cloud Logging shows no recent logs

**Diagnosis:**
```bash
# Check if service has received requests
gcloud run services describe perception-mcp \
  --project=perception-with-intent \
  --region=us-central1 \
  --format='value(status.traffic[0].percent)'
```

**Common Causes:**
- No requests sent to service
- Logging disabled (unlikely)
- Service crashed immediately

**Fix:**
- Send test request: `curl https://perception-mcp-348724539390.us-central1.run.app/health`
- Check recent revisions: `gcloud run revisions list`
- Verify service account has logging permissions

### High Latency

**Symptom:** Requests take >2 seconds

**Diagnosis:**
```bash
# Check latency distribution
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp" AND jsonPayload.latency_ms>0' \
  --project=perception-with-intent \
  --limit=20 \
  --format='value(jsonPayload.latency_ms)'
```

**Common Causes:**
- External RSS feed slow to respond
- Cold start (first request after scale to zero)
- CPU throttling (underprovisioned)

**Fix:**
- Set `--min-instances 1` to avoid cold starts
- Increase CPU: `--cpu 2`
- Add timeouts to external HTTP calls

---

## Key Metrics Dashboard

**Access:**
- Cloud Console > Cloud Run > perception-mcp > Metrics
- Or create custom dashboard in Cloud Monitoring

**Recommended Widgets:**
1. **Request Count** (time series)
   - Metric: `run.googleapis.com/request_count`
   - Grouping: `response_code_class`

2. **Request Latency** (heatmap)
   - Metric: `run.googleapis.com/request_latencies`
   - Percentiles: P50, P95, P99

3. **Container Instances** (time series)
   - Metric: `run.googleapis.com/container/instance_count`
   - Shows auto-scaling behavior

4. **Error Rate** (time series)
   - Metric: `run.googleapis.com/request_count`
   - Filter: `response_code >= 400`

5. **Memory Utilization** (gauge)
   - Metric: `run.googleapis.com/container/memory/utilizations`
   - Alert if > 90%

6. **CPU Utilization** (gauge)
   - Metric: `run.googleapis.com/container/cpu/utilizations`
   - Alert if > 80%

---

## Future AAR (MCP Cloud Run Observability) – Placeholder Only

**TODO:** After 1 month of production Cloud Run MCP usage, document:
- Most common errors and resolutions
- P95/P99 latency benchmarks per tool
- Auto-scaling patterns (min/max instances optimizations)
- Cost analysis (requests vs compute time)
- Alerting tuning (false positive rate)

Do NOT create the AAR content in this phase.

---

## Summary

### The Cloud Run Rule

**Perception MCP runs ONLY on Cloud Run:**
- **Code:** `app/mcp_service/` deployed to Cloud Run
- **Deployment:** `gcloud run deploy` or GitHub Actions workflow
- **Testing:** Cloud Run URL only (NO localhost)
- **Logging:** Cloud Logging (structured JSON)
- **Metrics:** Cloud Run automatic metrics

### Verification Checklist

✅ **MCP Deployed:** `gcloud run services describe perception-mcp` returns URL
✅ **Health Check:** `curl /health` returns HTTP 200
✅ **Functional Test:** `curl /mcp/tools/fetch_rss_feed` returns articles
✅ **Logging Active:** Cloud Logging shows recent request logs
✅ **No Errors:** Cloud Logging shows no ERROR-level logs

### What's NOT Valid

❌ No local MCP on localhost:8080
❌ No fake "it would work if deployed"
❌ No testing without real Cloud Run URL
❌ No claiming deployment without `gcloud run services describe` proof

---

**Last Updated:** 2025-11-15
**Phase:** MCP Cloud Run Validation + Observability
**Status:** Service deployed and verified with real HTTP requests and Cloud Logging proof
**Next:** Integrate MCP_BASE_URL into agent runtime configs
