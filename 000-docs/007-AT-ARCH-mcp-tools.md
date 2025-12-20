# Perception With Intent - MCP Tool Specifications

**Version:** 1.0
**Date:** 2025-11-14
**Phase:** 4 (MCP Tool Architecture + Scaffolding)

---

## Overview

This document defines the 7 MCP (Model Context Protocol) tools that Perception agents use to interact with external systems. Each tool is exposed as an HTTP endpoint running on Cloud Run.

**Architecture Principle:**
- Agents are SMART (orchestrate, decide, analyze)
- MCPs are DUMB (fetch, store, send - no thinking)

---

## MCP Service Architecture

```
Vertex AI Agent Engine (8 Agents)
    ↓ HTTP POST
MCP Service (FastAPI on Cloud Run)
    ↓
7 Tool Endpoints (Routers)
    ↓
External Systems (Firestore, RSS, APIs, Gemini)
```

**Service Details:**
- **Runtime:** Python 3.12 + FastAPI
- **Deployment:** Cloud Run (autoscaling 0-10 instances)
- **Base URL (staging):** `https://mcp-service-HASH-uc.a.run.app`
- **Base URL (prod):** `https://mcp.perception-with-intent.com`
- **Authentication:** Service account tokens (Workload Identity)
- **Observability:** OpenTelemetry traces + structured logging

---

## Tool 1: fetch_rss_feed

### Purpose
Fetch and parse articles from an RSS feed.

### HTTP Endpoint
```
POST /mcp/tools/fetch_rss_feed
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "feed_id": "string",           // Firestore document ID from /sources collection
  "max_articles": 50             // Optional, default 50
}
```

### Response Schema (Success)
```json
{
  "feed_id": "techcrunch_ai",
  "feed_url": "https://techcrunch.com/feed/",
  "fetched_at": "2025-11-14T12:00:00Z",
  "article_count": 23,
  "articles": [
    {
      "title": "OpenAI Announces GPT-5",
      "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
      "published_at": "2025-11-14T10:30:00Z",
      "summary": "OpenAI today announced...",
      "author": "Jane Smith",
      "content_snippet": "First 500 chars of article...",
      "raw_content": "Full HTML content if available",
      "categories": ["AI", "Technology"]
    }
  ]
}
```

### Error Schema
```json
{
  "error": {
    "code": "FEED_FETCH_FAILED",
    "message": "Failed to fetch RSS feed: Connection timeout",
    "feed_id": "techcrunch_ai",
    "details": {
      "http_status": 504,
      "timeout_seconds": 30
    }
  }
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Invalid feed_id or malformed request
- `404` - Feed not found in /sources collection
- `500` - RSS parse error or network failure
- `504` - Feed fetch timeout

### Observability
**Trace Attributes:**
- `mcp.tool.name = fetch_rss_feed`
- `feed.id = {feed_id}`
- `feed.url = {feed_url}`
- `articles.count = {article_count}`

**Logs:**
```json
{
  "severity": "INFO",
  "message": "Fetched RSS feed",
  "feed_id": "techcrunch_ai",
  "article_count": 23,
  "latency_ms": 1240
}
```

---

## Tool 2: fetch_api_feed

### Purpose
Fetch articles from a custom API endpoint (NewsAPI, custom scrapers, etc.).

### HTTP Endpoint
```
POST /mcp/tools/fetch_api_feed
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "feed_id": "string",           // Firestore document ID from /sources collection
  "api_params": {                // Optional, source-specific params
    "keywords": ["AI", "OpenAI"],
    "date_range": "last_24h"
  }
}
```

### Response Schema (Success)
```json
{
  "feed_id": "newsapi_tech",
  "api_url": "https://newsapi.org/v2/everything",
  "fetched_at": "2025-11-14T12:00:00Z",
  "article_count": 15,
  "articles": [
    {
      "title": "Microsoft Launches New AI Tool",
      "url": "https://example.com/article",
      "published_at": "2025-11-14T09:00:00Z",
      "summary": "Microsoft today unveiled...",
      "author": "John Doe",
      "content_snippet": "First 500 chars...",
      "source": "TechCrunch",
      "categories": ["AI", "Microsoft"]
    }
  ]
}
```

### Error Schema
```json
{
  "error": {
    "code": "API_FETCH_FAILED",
    "message": "API returned error: Rate limit exceeded",
    "feed_id": "newsapi_tech",
    "details": {
      "http_status": 429,
      "retry_after_seconds": 60
    }
  }
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Invalid feed_id or params
- `401` - API authentication failed
- `429` - Rate limit exceeded
- `500` - API error or network failure

---

## Tool 3: fetch_webpage

### Purpose
Scrape article content from a given URL (for feeds that only provide snippets).

### HTTP Endpoint
```
POST /mcp/tools/fetch_webpage
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "url": "https://example.com/article",
  "extract_content": true,       // Extract main article content
  "extract_metadata": true       // Extract meta tags, Open Graph, etc.
}
```

### Response Schema (Success)
```json
{
  "url": "https://example.com/article",
  "fetched_at": "2025-11-14T12:00:00Z",
  "status_code": 200,
  "title": "Article Title from <title> tag",
  "content": "Full article text extracted from main content",
  "metadata": {
    "description": "Meta description",
    "keywords": ["AI", "Technology"],
    "author": "Jane Smith",
    "published_at": "2025-11-14T10:00:00Z",
    "og_image": "https://example.com/image.jpg"
  },
  "word_count": 1250
}
```

### Error Schema
```json
{
  "error": {
    "code": "WEBPAGE_FETCH_FAILED",
    "message": "Failed to fetch webpage: 404 Not Found",
    "url": "https://example.com/article",
    "details": {
      "http_status": 404
    }
  }
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Invalid URL
- `404` - Webpage not found
- `500` - Scraping error or network failure

---

## Tool 4: store_articles

### Purpose
Batch write articles to Firestore `/articles` collection.

### HTTP Endpoint
```
POST /mcp/tools/store_articles
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "run_id": "run_1731585600",
  "articles": [
    {
      "title": "OpenAI Announces GPT-5",
      "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
      "source_id": "techcrunch_ai",
      "published_at": "2025-11-14T10:30:00Z",
      "summary": "OpenAI today announced...",
      "content": "Full article text...",
      "ai_summary": "AI-generated 3-sentence summary",
      "ai_tags": ["AI", "OpenAI", "GPT-5"],
      "relevance_score": 9.5,
      "categories": ["AI", "Technology"]
    }
  ]
}
```

### Response Schema (Success)
```json
{
  "run_id": "run_1731585600",
  "stored_count": 23,
  "failed_count": 0,
  "failed_urls": [],
  "storage_stats": {
    "firestore_writes": 23,
    "duplicates_skipped": 2,
    "latency_ms": 450
  }
}
```

### Error Schema
```json
{
  "error": {
    "code": "STORAGE_FAILED",
    "message": "Failed to store articles: Firestore write error",
    "run_id": "run_1731585600",
    "details": {
      "failed_count": 5,
      "failed_urls": [
        "https://example.com/article1",
        "https://example.com/article2"
      ],
      "firestore_error": "DEADLINE_EXCEEDED"
    }
  }
}
```

**HTTP Status Codes:**
- `200` - All articles stored
- `207` - Partial success (some articles failed)
- `400` - Invalid request schema
- `500` - Firestore error

---

## Tool 5: generate_brief

### Purpose
Generate daily executive brief using Gemini 2.0 Flash.

### HTTP Endpoint
```
POST /mcp/tools/generate_brief
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "run_id": "run_1731585600",
  "date": "2025-11-14",
  "top_articles": [
    {
      "title": "OpenAI Announces GPT-5",
      "url": "https://techcrunch.com/...",
      "ai_summary": "OpenAI today announced...",
      "relevance_score": 9.5,
      "categories": ["AI", "Technology"]
    }
  ],
  "max_highlights": 5
}
```

### Response Schema (Success)
```json
{
  "run_id": "run_1731585600",
  "date": "2025-11-14",
  "executive_summary": "Today's intelligence highlights major developments in AI...",
  "highlights": [
    {
      "title": "OpenAI Announces GPT-5",
      "significance": "Major model release with breakthrough capabilities",
      "strategic_implications": "Increased competition in AI space",
      "url": "https://techcrunch.com/..."
    }
  ],
  "topic_breakdown": {
    "AI": 12,
    "Technology": 8,
    "Business": 3
  },
  "total_articles_analyzed": 23,
  "generated_at": "2025-11-14T12:05:00Z"
}
```

### Error Schema
```json
{
  "error": {
    "code": "BRIEF_GENERATION_FAILED",
    "message": "Gemini API error: Rate limit exceeded",
    "run_id": "run_1731585600",
    "details": {
      "gemini_error": "RESOURCE_EXHAUSTED",
      "retry_after_seconds": 30
    }
  }
}
```

**HTTP Status Codes:**
- `200` - Brief generated successfully
- `400` - Invalid request (missing articles, etc.)
- `429` - Gemini rate limit exceeded
- `500` - Gemini API error

---

## Tool 6: log_ingestion_run

### Purpose
Create or update an ingestion run record in Firestore `/ingestion_runs` collection.

### HTTP Endpoint
```
POST /mcp/tools/log_ingestion_run
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "run_id": "run_1731585600",
  "status": "running",           // "running" | "completed" | "failed"
  "stats": {
    "sources_checked": 15,
    "articles_fetched": 47,
    "articles_stored": 45,
    "duplicates_skipped": 2,
    "brief_generated": true,
    "errors": []
  },
  "started_at": "2025-11-14T12:00:00Z",
  "completed_at": "2025-11-14T12:05:00Z"  // Optional, set when status=completed
}
```

### Response Schema (Success)
```json
{
  "run_id": "run_1731585600",
  "logged_at": "2025-11-14T12:05:00Z",
  "firestore_path": "/ingestion_runs/run_1731585600"
}
```

### Error Schema
```json
{
  "error": {
    "code": "LOGGING_FAILED",
    "message": "Failed to log ingestion run: Firestore write error",
    "run_id": "run_1731585600",
    "details": {
      "firestore_error": "PERMISSION_DENIED"
    }
  }
}
```

**HTTP Status Codes:**
- `200` - Logged successfully
- `400` - Invalid request schema
- `500` - Firestore error

---

## Tool 7: send_notification

### Purpose
Send notifications via Slack, email, or webhooks (future implementation).

### HTTP Endpoint
```
POST /mcp/tools/send_notification
Content-Type: application/json
Authorization: Bearer {SERVICE_ACCOUNT_TOKEN}
```

### Request Schema
```json
{
  "channel": "slack",            // "slack" | "email" | "webhook"
  "recipient": "C12345678",      // Slack channel ID, email, or webhook URL
  "message": {
    "title": "Daily Brief Available",
    "body": "Today's intelligence brief is ready with 23 articles analyzed.",
    "url": "https://perception.intentsolutions.io/briefs/2025-11-14"
  },
  "priority": "normal"           // "low" | "normal" | "high"
}
```

### Response Schema (Success)
```json
{
  "notification_id": "notif_abc123",
  "channel": "slack",
  "sent_at": "2025-11-14T12:05:00Z",
  "status": "delivered"
}
```

### Error Schema
```json
{
  "error": {
    "code": "NOTIFICATION_FAILED",
    "message": "Slack API error: Invalid channel",
    "channel": "slack",
    "details": {
      "slack_error": "channel_not_found"
    }
  }
}
```

**HTTP Status Codes:**
- `200` - Notification sent
- `400` - Invalid channel or recipient
- `429` - Rate limit exceeded
- `500` - Delivery service error

**Note:** This tool is a STUB for Phase 4. Full implementation in Phase 6.

---

## Common Error Codes

| Error Code | HTTP Status | Meaning |
|------------|-------------|---------|
| `INVALID_REQUEST` | 400 | Malformed JSON or missing required fields |
| `FEED_NOT_FOUND` | 404 | Source not found in Firestore |
| `FEED_FETCH_FAILED` | 500 | RSS/API fetch error |
| `WEBPAGE_FETCH_FAILED` | 500 | Web scraping error |
| `STORAGE_FAILED` | 500 | Firestore write error |
| `BRIEF_GENERATION_FAILED` | 500 | Gemini API error |
| `LOGGING_FAILED` | 500 | Firestore logging error |
| `NOTIFICATION_FAILED` | 500 | Delivery service error |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `UNAUTHORIZED` | 401 | Invalid or missing service account token |

---

## Authentication

All MCP tools require service account authentication:

```bash
# Get service account token
TOKEN=$(gcloud auth print-identity-token \
  --impersonate-service-account=mcp-service@perception-with-intent.iam.gserviceaccount.com)

# Call MCP tool
curl -X POST https://mcp-service-HASH-uc.a.run.app/mcp/tools/fetch_rss_feed \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"feed_id": "techcrunch_ai"}'
```

**Service Account IAM Roles:**
- `roles/datastore.user` - Firestore read/write
- `roles/aiplatform.user` - Gemini API access
- `roles/secretmanager.secretAccessor` - API keys for NewsAPI, Slack, etc.

---

## Observability Requirements

### OpenTelemetry Traces

All tools must emit spans:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("fetch_rss_feed")
def fetch_rss_feed(feed_id: str):
    span = trace.get_current_span()
    span.set_attribute("mcp.tool.name", "fetch_rss_feed")
    span.set_attribute("feed.id", feed_id)
    # ... fetch logic ...
    span.set_attribute("articles.count", len(articles))
```

### Structured Logging

All tools must use structured JSON logs:

```python
import logging
import json

logger = logging.getLogger(__name__)

logger.info(json.dumps({
  "severity": "INFO",
  "message": "Fetched RSS feed",
  "mcp_tool": "fetch_rss_feed",
  "feed_id": feed_id,
  "article_count": len(articles),
  "latency_ms": latency
}))
```

**Log Levels:**
- `DEBUG` - HTTP requests, detailed steps
- `INFO` - Successful operations, article counts
- `WARNING` - Retryable errors, rate limits
- `ERROR` - Failed operations, data errors

---

## Performance Targets

| Tool | p50 Latency | p95 Latency | Success Rate |
|------|-------------|-------------|--------------|
| fetch_rss_feed | < 1s | < 3s | > 95% |
| fetch_api_feed | < 2s | < 5s | > 95% |
| fetch_webpage | < 2s | < 6s | > 90% |
| store_articles | < 500ms | < 2s | > 99% |
| generate_brief | < 10s | < 30s | > 98% |
| log_ingestion_run | < 200ms | < 1s | > 99% |
| send_notification | < 1s | < 3s | > 95% |

---

## Testing Strategy

### Local Testing
```bash
# Start MCP service locally
cd app/mcp_service
uvicorn main:app --reload --port 8080

# Test each endpoint
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{"feed_id": "techcrunch_ai"}'
```

### Integration Testing
```python
# tests/test_mcp_integration.py
async def test_fetch_rss_feed():
    response = await client.post("/mcp/tools/fetch_rss_feed", json={
        "feed_id": "techcrunch_ai"
    })
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert len(data["articles"]) > 0
```

---

## Deployment

### Cloud Run Configuration
```yaml
# service: mcp-service
runtime: python312
instance_class: F1
scaling:
  min_instances: 0
  max_instances: 10
  target_cpu_utilization: 0.8
env_variables:
  GOOGLE_CLOUD_PROJECT: perception-with-intent
  FIRESTORE_DATABASE: (default)
vpc_access_connector: perception-vpc-connector
```

### Terraform Deployment
```hcl
resource "google_cloud_run_service" "mcp_service" {
  name     = "mcp-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/perception-with-intent/mcp-service:latest"
        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = "perception-with-intent"
        }
      }
      service_account_name = "mcp-service@perception-with-intent.iam.gserviceaccount.com"
    }
  }
}
```

---

## Known Limitations (Phase 4)

1. **No real implementations** - All tools return fake but structurally correct responses
2. **No Firestore integration** - Database calls are stubbed
3. **No HTTP requests** - RSS/API fetches are mocked
4. **No Gemini calls** - Brief generation returns placeholder text
5. **No OpenTelemetry** - Tracing code has TODO comments

**Fix in Phase 5:** Wire up real Firestore, RSS parsing, Gemini API calls

---

## Next Steps

### Phase 5: First MCP Tool Implementation
- Implement `fetch_rss_feed` with real RSS parsing
- Add Firestore source lookup
- Deploy to Cloud Run
- Wire to Agent 1 (Source Harvester)

### Phase 6: Complete MCP Implementation
- Implement remaining 6 tools
- Add OpenTelemetry instrumentation
- End-to-end testing
- Production deployment

---

**Last Updated:** 2025-11-14
**Status:** Phase 4 Complete - MCP Tool Architecture Defined
**Next:** Phase 5 (First MCP Tool Implementation)
