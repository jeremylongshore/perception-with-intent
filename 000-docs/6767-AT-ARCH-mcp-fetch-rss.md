# MCP Tool: fetch_rss_feed - Technical Specification

**Version:** 1.0
**Date:** 2025-11-14
**Phase:** 5 (Real RSS Implementation Complete)

---

## Overview

The `fetch_rss_feed` MCP tool fetches and normalizes articles from RSS feeds. It is the first production-ready MCP tool in the Perception system.

**Purpose:**
- Fetch RSS feeds via HTTP
- Parse RSS/Atom XML
- Normalize article data
- Filter by time window
- Return structured JSON

**Endpoint:** `POST /mcp/tools/fetch_rss_feed`

---

## Request Schema

```json
{
  "feed_url": "https://techcrunch.com/feed/",
  "time_window_hours": 24,
  "max_items": 50,
  "request_id": "harvest_techcrunch_ai_20251114"
}
```

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `feed_url` | string | Yes | - | RSS/Atom feed URL |
| `time_window_hours` | int | No | 24 | Only return articles published in last N hours (1-720) |
| `max_items` | int | No | 50 | Maximum articles to return (1-500) |
| `request_id` | string | No | null | Optional tracking ID for logging |

---

## Response Schema (Success)

```json
{
  "feed_id": "",
  "feed_url": "https://techcrunch.com/feed/",
  "fetched_at": "2025-11-14T12:00:00+00:00",
  "article_count": 23,
  "articles": [
    {
      "title": "OpenAI Announces GPT-5",
      "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
      "published_at": "2025-11-14T10:30:00+00:00",
      "summary": "OpenAI today announced GPT-5, the next generation...",
      "author": "Jane Smith",
      "content_snippet": "OpenAI today announced GPT-5...",
      "raw_content": "Full HTML content if available",
      "categories": ["AI", "Technology"]
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `feed_id` | string | Empty in Phase 5 (no Firestore lookup yet) |
| `feed_url` | string | The RSS feed URL that was fetched |
| `fetched_at` | string | ISO 8601 timestamp when fetch completed |
| `article_count` | int | Number of articles returned |
| `articles` | array | List of normalized article objects |

### Article Object

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Article title (required) |
| `url` | string | Article URL (required) |
| `published_at` | string | ISO 8601 publish timestamp (or fetch time if unavailable) |
| `summary` | string\|null | Article summary from RSS |
| `author` | string\|null | Author name if available |
| `content_snippet` | string\|null | First 500 chars of content |
| `raw_content` | string\|null | Full HTML content if provided in feed |
| `categories` | array | List of category/tag strings |

---

## Error Responses

### HTTP 504 - Feed Fetch Timeout

```json
{
  "error": {
    "code": "FEED_FETCH_FAILED",
    "message": "Feed fetch timeout after 30 seconds",
    "feed_url": "https://example.com/feed",
    "details": {
      "timeout_seconds": 30
    }
  }
}
```

### HTTP 404 - Feed Not Found

```json
{
  "error": {
    "code": "FEED_FETCH_FAILED",
    "message": "Feed returned HTTP 404",
    "feed_url": "https://example.com/feed",
    "details": {
      "http_status": 404
    }
  }
}
```

### HTTP 500 - Unexpected Error

```json
{
  "error": {
    "code": "FEED_FETCH_FAILED",
    "message": "Unexpected error: <exception message>",
    "feed_url": "https://example.com/feed"
  }
}
```

---

## Normalization Rules

### Published Date

The tool tries multiple fields to extract the publish date:

1. `entry.published_parsed` (time.struct_time) → convert to ISO 8601
2. `entry.published` (string) → parse with dateutil
3. `entry.updated_parsed` → fallback
4. Current timestamp → if all else fails

**Output:** Always ISO 8601 with UTC timezone (`2025-11-14T10:30:00+00:00`)

### Categories/Tags

Extracted from:
- `entry.tags` (list of dicts with 'term' field)
- `entry.category` (string)

Deduplicated and returned as string list.

### Content Snippet

Preference order:
1. `entry.summary` (truncated to 500 chars)
2. `entry.description` (truncated to 500 chars)
3. None

### Raw Content

Full HTML content if provided:
- `entry.content[0].value` (for Atom feeds)
- Otherwise None

---

## Time Window Filtering

Articles are filtered **after** parsing based on `published_at`:

```python
article_time = datetime.fromisoformat(published_at)
cutoff_time = datetime.now(tz=timezone.utc) - timedelta(hours=time_window_hours)

if article_time >= cutoff_time:
    include_article()
```

**Example:** If `time_window_hours=24` and current time is `2025-11-14T12:00:00Z`:
- Articles published after `2025-11-13T12:00:00Z` are included
- Older articles are filtered out

---

## Implementation Details

### HTTP Client

- Uses `httpx.AsyncClient` with 30-second timeout
- Follows redirects automatically
- Raises `httpx.HTTPStatusError` on non-2xx responses
- Raises `httpx.TimeoutException` on timeout

### RSS Parsing

- Uses `feedparser` library (universal feed parser)
- Handles RSS 2.0, RSS 1.0, Atom feeds
- Tolerates malformed feeds (`feed.bozo`)
- Returns empty list if feed has no entries

### Error Handling

- Network errors → return 504 or HTTP status from feed
- Parse errors → return empty list (log warning)
- Unexpected errors → return 500 with exception message
- All errors logged as JSON

---

## Logging

All logs are structured JSON with these fields:

### Success Log

```json
{
  "severity": "INFO",
  "message": "RSS feed fetched successfully",
  "mcp_tool": "fetch_rss_feed",
  "feed_url": "https://techcrunch.com/feed/",
  "article_count": 23,
  "latency_ms": 1240,
  "request_id": "harvest_techcrunch_ai"
}
```

### Error Log

```json
{
  "severity": "ERROR",
  "message": "RSS feed HTTP error",
  "feed_url": "https://techcrunch.com/feed/",
  "status_code": 404
}
```

### Warning Log (Malformed Feed)

```json
{
  "severity": "WARNING",
  "message": "Malformed RSS feed",
  "feed_url": "https://example.com/feed",
  "bozo_exception": "XML syntax error at line 42"
}
```

---

## Performance

### Measured Latency (Phase 5 Testing)

| Feed | Latency (p50) | Latency (p95) | Article Count |
|------|---------------|---------------|---------------|
| TechCrunch AI | ~800ms | ~2s | 15-25 |
| The Verge AI | ~600ms | ~1.5s | 10-20 |
| Hacker News | ~400ms | ~1s | 30-50 |

### Timeout

- HTTP timeout: 30 seconds
- Expected response time: < 3s for most feeds
- Slow feeds (> 5s) logged as warnings

---

## CSV-Based Sources (Phase 5)

In Phase 5, sources are loaded from `data/initial_feeds.csv`:

```csv
source_id,name,type,url,category,enabled
techcrunch_ai,TechCrunch AI,rss,https://techcrunch.com/category/artificial-intelligence/feed/,tech,true
theverge_ai,The Verge AI,rss,https://www.theverge.com/rss/ai-artificial-intelligence/index.xml,tech,true
```

**Columns:**
- `source_id` - Unique identifier
- `name` - Human-readable name
- `type` - Always `rss` for this tool
- `url` - RSS feed URL
- `category` - Category label (tech, research, etc.)
- `enabled` - `true` or `false`

**Phase 6 Migration:** Replace with Firestore `/sources` collection queries.

---

## Future Enhancements (Phase 6+)

### Firestore Integration

```python
from google.cloud import firestore

db = firestore.Client()
source_doc = db.collection("sources").document(feed_id).get()
feed_url = source_doc.to_dict()["url"]
```

**Benefits:**
- Dynamic source management
- Per-source configuration (refresh rate, filters)
- Source health tracking

### OpenTelemetry Tracing

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("fetch_rss_feed") as span:
    span.set_attribute("mcp.tool.name", "fetch_rss_feed")
    span.set_attribute("feed.url", request.feed_url)
    span.set_attribute("articles.count", article_count)
    span.set_attribute("latency_ms", latency_ms)
```

**Benefits:**
- Distributed tracing across MCP → Agent → Orchestrator
- Performance profiling
- Error correlation

### Metrics Export

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
article_counter = meter.create_counter("mcp.articles.fetched")
latency_histogram = meter.create_histogram("mcp.fetch_rss.latency_ms")

article_counter.add(article_count, {"feed_url": feed_url})
latency_histogram.record(latency_ms, {"feed_url": feed_url})
```

**Metrics:**
- `mcp.articles.fetched` (counter) - Total articles fetched
- `mcp.fetch_rss.latency_ms` (histogram) - Latency distribution
- `mcp.fetch_rss.errors` (counter) - Error counts by type

---

## Example Requests

### Fetch Latest Articles (Last 24 Hours)

```bash
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "time_window_hours": 24,
    "max_items": 50
  }'
```

### Fetch All Available Articles

```bash
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://news.ycombinator.com/rss",
    "time_window_hours": 720,
    "max_items": 500
  }'
```

### Fetch with Request Tracking

```bash
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "time_window_hours": 12,
    "max_items": 25,
    "request_id": "test_verge_20251114_1200"
  }'
```

---

## Known Limitations (Phase 5)

1. **No Firestore lookup** - `feed_id` field is empty (Phase 6)
2. **No caching** - Every request fetches fresh (Phase 6)
3. **No rate limiting** - Can overwhelm feeds if called too often (Phase 6)
4. **No retry logic** - Single attempt only (Phase 6)
5. **No OpenTelemetry** - Logging only, no traces (Phase 6)

---

## Testing

### Unit Tests

```python
# tests/test_fetch_rss_feed.py
import pytest
from routers.rss import fetch_rss_feed, FetchRSSFeedRequest

@pytest.mark.asyncio
async def test_fetch_techcrunch():
    request = FetchRSSFeedRequest(
        feed_url="https://techcrunch.com/feed/",
        time_window_hours=24,
        max_items=10
    )
    response = await fetch_rss_feed(request)
    assert response.article_count > 0
    assert len(response.articles) <= 10
    assert response.feed_url == request.feed_url
```

### Integration Tests

```bash
# Start MCP service
uvicorn app.mcp_service.main:app --port 8080

# Test endpoint
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{"feed_url": "https://techcrunch.com/feed/", "max_items": 5}'
```

---

**Last Updated:** 2025-11-14
**Status:** Phase 5 Complete - Real RSS Implementation Working
**Next:** Phase 6 (Firestore Integration + OpenTelemetry)
