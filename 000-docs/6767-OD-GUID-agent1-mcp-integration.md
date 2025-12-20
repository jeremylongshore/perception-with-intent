# Agent 1 → MCP Integration Guide

**Version:** 1.0
**Date:** 2025-11-14
**Phase:** 5 (Real MCP Integration Complete)

---

## Overview

This guide explains how **Agent 1 (Source Harvester)** integrates with the **MCP fetch_rss_feed tool** to fetch and normalize news articles.

**Agent 1 Responsibilities:**
- Load configured news sources from CSV or Firestore
- Call MCP tools to fetch content (RSS, API, web)
- Normalize raw article data into standard structure
- Aggregate articles from all sources
- Return structured data to Orchestrator (Agent 0)

**MCP Tool Responsibilities:**
- Fetch RSS/API/web content via HTTP
- Parse and extract article data
- Return normalized JSON
- Handle errors gracefully

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│         Vertex AI Agent Engine                         │
│                                                         │
│  ┌──────────────────────────────────────────────┐     │
│  │  Agent 0 (Orchestrator)                      │     │
│  │  "Start daily ingestion run"                 │     │
│  └───────────────┬──────────────────────────────┘     │
│                  │ A2A call                             │
│                  ↓                                      │
│  ┌──────────────────────────────────────────────┐     │
│  │  Agent 1 (Source Harvester)                  │     │
│  │  agent_1_tools.py:                           │     │
│  │   - load_sources_from_csv()                  │     │
│  │   - fetch_rss(feed_url) → HTTP POST          │     │
│  │   - normalize_article(raw)                   │     │
│  │   - harvest_all_sources()                    │     │
│  └───────────────┬──────────────────────────────┘     │
│                  │ HTTP POST                            │
└──────────────────┼──────────────────────────────────────┘
                   │
                   ↓
┌────────────────────────────────────────────────────────┐
│         MCP Service (FastAPI on Cloud Run)             │
│                                                         │
│  POST /mcp/tools/fetch_rss_feed                        │
│                                                         │
│  ┌──────────────────────────────────────────────┐     │
│  │  routers/rss.py:                             │     │
│  │   1. Validate request                        │     │
│  │   2. Fetch RSS via httpx                     │     │
│  │   3. Parse with feedparser                   │     │
│  │   4. Normalize articles                      │     │
│  │   5. Filter by time window                   │     │
│  │   6. Return JSON                             │     │
│  └───────────────┬──────────────────────────────┘     │
│                  │ HTTP GET                             │
└──────────────────┼──────────────────────────────────────┘
                   │
                   ↓
           RSS Feed Server
           (TechCrunch, The Verge, etc.)
```

---

## Tool Chain Execution

### Step-by-Step Flow

1. **Orchestrator triggers Agent 1**
   - Via ADK's internal A2A mechanism
   - Passes `run_id` and configuration

2. **Agent 1 loads sources**
   - Phase 5: From `data/initial_feeds.csv`
   - Phase 6+: From Firestore `/sources` collection
   - Filters for `enabled == true`

3. **Agent 1 calls MCP for each source**
   - `POST /mcp/tools/fetch_rss_feed`
   - Passes `feed_url`, `time_window_hours`, `max_items`
   - Receives JSON response with articles

4. **Agent 1 normalizes articles**
   - Extracts common fields (title, url, published_at, etc.)
   - Adds source metadata (source_id, category)
   - Creates uniform structure for downstream agents

5. **Agent 1 aggregates results**
   - Combines articles from all sources
   - Returns to Orchestrator with stats

6. **Orchestrator passes to Agent 3**
   - Agent 3 (Relevance & Ranking) scores articles
   - Top-ranked articles → Agent 4 (Brief Writer)

---

## Data Flow

### CSV Source → Agent 1 → MCP → Normalized Article

#### 1. CSV Source (data/initial_feeds.csv)

```csv
source_id,name,type,url,category,enabled
techcrunch_ai,TechCrunch AI,rss,https://techcrunch.com/category/artificial-intelligence/feed/,tech,true
```

#### 2. Agent 1 Loads Source

```python
{
  "source_id": "techcrunch_ai",
  "name": "TechCrunch AI",
  "type": "rss",
  "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
  "category": "tech",
  "enabled": true
}
```

#### 3. Agent 1 Calls MCP

**Request:**
```json
POST /mcp/tools/fetch_rss_feed
{
  "feed_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
  "time_window_hours": 24,
  "max_items": 50,
  "request_id": "harvest_techcrunch_ai"
}
```

**Response:**
```json
{
  "feed_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
  "fetched_at": "2025-11-14T12:00:00+00:00",
  "article_count": 23,
  "articles": [
    {
      "title": "OpenAI Announces GPT-5",
      "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
      "published_at": "2025-11-14T10:30:00+00:00",
      "summary": "OpenAI today announced GPT-5...",
      "author": "Jane Smith",
      "content_snippet": "OpenAI today announced...",
      "raw_content": "Full HTML content...",
      "categories": ["AI", "Technology"]
    }
  ]
}
```

#### 4. Agent 1 Normalizes Article

```python
{
  "title": "OpenAI Announces GPT-5",
  "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
  "source_id": "techcrunch_ai",        # Added by normalize_article()
  "category": "tech",                   # Added from CSV source
  "published_at": "2025-11-14T10:30:00+00:00",
  "summary": "OpenAI today announced GPT-5...",
  "content": "Full HTML content...",    # From raw_content or summary
  "content_snippet": "OpenAI today announced...",
  "author": "Jane Smith",
  "categories": ["AI", "Technology"]    # From RSS tags
}
```

#### 5. Agent 1 Returns to Orchestrator

```python
{
  "articles": [
    { /* normalized article 1 */ },
    { /* normalized article 2 */ },
    ...
  ],
  "source_count": 11,          # Number of sources processed
  "total_fetched": 247         # Total articles fetched (before normalization)
}
```

---

## Agent 1 Tools API

### `load_sources_from_csv()` → `List[Dict[str, Any]]`

**Purpose:** Load enabled sources from CSV file.

**CSV Path:** `data/initial_feeds.csv` (relative to repo root)

**Returns:**
```python
[
  {
    "source_id": "techcrunch_ai",
    "name": "TechCrunch AI",
    "type": "rss",
    "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "category": "tech",
    "enabled": True
  },
  ...
]
```

**Filters:** Only sources where `enabled == "true"` (case-insensitive)

**Logging:**
```json
{
  "severity": "INFO",
  "tool": "agent_1",
  "operation": "load_sources_from_csv",
  "sources_loaded": 11
}
```

---

### `fetch_rss(feed_url, time_window_hours, max_items, request_id)` → `List[Dict[str, Any]]`

**Purpose:** Call MCP fetch_rss_feed endpoint and return raw articles.

**Parameters:**
- `feed_url` (str) - RSS feed URL
- `time_window_hours` (int, default 24) - Only fetch articles from last N hours
- `max_items` (int, default 50) - Max articles to return
- `request_id` (str, optional) - Tracking ID for logs

**Returns:** List of raw article dicts from MCP response

**Error Handling:**
- HTTP errors → log and return empty list
- Network errors → log and return empty list
- Never raises exceptions (fail gracefully)

**Logging (Success):**
```json
{
  "severity": "INFO",
  "tool": "agent_1",
  "operation": "fetch_rss",
  "feed_url": "https://techcrunch.com/feed/",
  "article_count": 23
}
```

**Logging (Error):**
```json
{
  "severity": "ERROR",
  "tool": "agent_1",
  "operation": "fetch_rss",
  "feed_url": "https://techcrunch.com/feed/",
  "http_status": 404,
  "error": "Feed not found"
}
```

---

### `normalize_article(raw, source_id, category)` → `Dict[str, Any]`

**Purpose:** Convert raw MCP article to standard structure.

**Parameters:**
- `raw` (Dict) - Raw article from MCP response
- `source_id` (str) - Source identifier
- `category` (str, optional) - Category label

**Returns:**
```python
{
  "title": "Article Title",
  "url": "https://example.com/article",
  "source_id": "techcrunch_ai",
  "category": "tech",
  "published_at": "2025-11-14T10:30:00+00:00",
  "summary": "Article summary...",
  "content": "Full content (raw_content or summary or content_snippet)",
  "content_snippet": "First 500 chars...",
  "author": "Jane Smith",
  "categories": ["AI", "Technology"]
}
```

**Normalization Rules:**
1. `title` - Use raw title or "Untitled"
2. `url` - Use raw URL or empty string
3. `source_id` - From function parameter
4. `category` - From function parameter
5. `published_at` - ISO 8601 from raw
6. `summary` - From raw summary
7. `content` - Prefer raw_content > summary > content_snippet
8. `content_snippet` - From raw
9. `author` - From raw author or None
10. `categories` - From raw categories list

---

### `harvest_all_sources(time_window_hours, max_items_per_source)` → `Dict[str, Any]`

**Purpose:** High-level harvesting function that orchestrates the full process.

**Parameters:**
- `time_window_hours` (int, default 24) - Time window for articles
- `max_items_per_source` (int, default 50) - Max articles per source

**Returns:**
```python
{
  "articles": [
    { /* normalized article 1 */ },
    { /* normalized article 2 */ },
    ...
  ],
  "source_count": 11,
  "total_fetched": 247
}
```

**Process:**
1. Load sources from CSV
2. For each enabled source:
   - If type == "rss": call `fetch_rss()`
   - If type == "api": TODO (Phase 6)
   - If type == "web": TODO (Phase 6)
3. Normalize each raw article
4. Aggregate all articles
5. Return results with stats

**Logging:**
```json
{
  "severity": "INFO",
  "tool": "agent_1",
  "operation": "harvest_all_sources",
  "source_count": 11,
  "total_fetched": 247,
  "articles_after_normalization": 245
}
```

---

## Local Testing

### 1. Start MCP Service

```bash
cd /home/jeremy/000-projects/perception

# Install dependencies
cd app/mcp_service
pip install -r requirements.txt

# Start service
uvicorn main:app --reload --port 8080
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8080
INFO:     Application startup complete.
```

### 2. Test MCP Endpoint Directly

```bash
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "time_window_hours": 24,
    "max_items": 5
  }'
```

**Expected Response:**
```json
{
  "feed_id": "",
  "feed_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
  "fetched_at": "2025-11-14T12:00:00+00:00",
  "article_count": 5,
  "articles": [...]
}
```

### 3. Test Agent 1 Tools (Python REPL)

```bash
cd /home/jeremy/000-projects/perception
python
```

```python
import asyncio
from app.perception_agent.tools.agent_1_tools import harvest_all_sources

# Test harvest_all_sources
result = asyncio.run(harvest_all_sources(time_window_hours=24, max_items_per_source=5))

print(f"Sources processed: {result['source_count']}")
print(f"Total fetched: {result['total_fetched']}")
print(f"Articles after normalization: {len(result['articles'])}")

# Show first article
if result['articles']:
    article = result['articles'][0]
    print(f"\nFirst article:")
    print(f"  Title: {article['title']}")
    print(f"  Source: {article['source_id']}")
    print(f"  URL: {article['url']}")
    print(f"  Published: {article['published_at']}")
```

**Expected Output:**
```
Sources processed: 11
Total fetched: 55
Articles after normalization: 55

First article:
  Title: OpenAI Announces GPT-5
  Source: techcrunch_ai
  URL: https://techcrunch.com/2025/11/14/openai-gpt5
  Published: 2025-11-14T10:30:00+00:00
```

### 4. Test with curl (Full Integration)

```bash
# Test single feed
curl -X POST http://localhost:8080/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{
    "feed_url": "https://news.ycombinator.com/rss",
    "time_window_hours": 12,
    "max_items": 10,
    "request_id": "test_hn_$(date +%s)"
  }' | jq '.'
```

---

## Environment Configuration

### MCP Service URL

Agent 1 reads the MCP base URL from environment:

```bash
export MCP_BASE_URL=http://localhost:8080  # Local development
export MCP_BASE_URL=https://mcp-service-HASH-uc.a.run.app  # Cloud Run production
```

**Default:** `http://localhost:8080`

**agent_1_tools.py:**
```python
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8080")
endpoint = f"{MCP_BASE_URL}/mcp/tools/fetch_rss_feed"
```

---

## Error Handling Strategy

### MCP Endpoint Failures

Agent 1 **never raises exceptions** when MCP calls fail. Instead:

1. **Log error** (structured JSON)
2. **Return empty list** for that source
3. **Continue processing** remaining sources

**Rationale:** Partial failure is acceptable. If 1 of 11 feeds fails, we still get 10 feeds of data.

**Example:**
```python
# techcrunch_ai fails → returns []
# theverge_ai succeeds → returns 15 articles
# bbc_technology succeeds → returns 20 articles
# Result: 35 total articles (2 sources)
```

### CSV Loading Failures

If CSV file is missing or malformed:

1. **Log error**
2. **Return empty list**
3. **Orchestrator sees zero articles**

**Orchestrator should handle** empty article lists gracefully (skip downstream processing).

---

## Logging Standards

All Agent 1 logs use structured JSON:

```json
{
  "severity": "INFO|WARNING|ERROR",
  "tool": "agent_1",
  "operation": "operation_name",
  "...": "additional context"
}
```

**Operations:**
- `load_sources_from_csv`
- `fetch_rss`
- `harvest_all_sources`

**Log Levels:**
- `INFO` - Normal operations, success
- `WARNING` - No sources found, some feeds failed
- `ERROR` - CSV read error, HTTP error, unexpected exception

---

## Future Enhancements (Phase 6+)

### Firestore Source Loading

Replace CSV with Firestore:

```python
def load_sources_from_firestore() -> List[Dict[str, Any]]:
    from google.cloud import firestore
    db = firestore.Client()
    sources_ref = db.collection('sources')
    query = sources_ref.where('enabled', '==', True)
    return [doc.to_dict() for doc in query.stream()]
```

**Benefits:**
- Dynamic source management via dashboard
- Per-source configuration (refresh rate, filters)
- Source health tracking

### Parallel Fetching

Currently sources are fetched sequentially. Phase 6+ will use `asyncio.gather`:

```python
tasks = [fetch_rss(source['url'], ...) for source in sources if source['type'] == 'rss']
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**Benefits:**
- 10x faster harvesting (11 feeds in parallel vs sequential)
- Reduced total latency

### API and Web Scraping

Add support for non-RSS sources:

```python
if source_type == 'api':
    raw_articles = await fetch_api_feed(source['url'], ...)
elif source_type == 'web':
    raw_articles = await fetch_webpage(source['url'], ...)
```

---

## Known Limitations (Phase 5)

1. **Sequential fetching** - Sources processed one at a time (slow)
2. **CSV-only sources** - No Firestore integration yet
3. **RSS-only** - API and web scraping not implemented
4. **No caching** - Fetches every time (can hit rate limits)
5. **No retry logic** - Single attempt per source
6. **No OpenTelemetry** - Logging only, no distributed tracing

---

## Troubleshooting

### "No sources loaded"

**Symptom:** `sources_loaded: 0` in logs

**Causes:**
- CSV file not found at `data/initial_feeds.csv`
- All sources have `enabled: false`
- CSV malformed

**Fix:**
```bash
# Check CSV exists
ls -la /home/jeremy/000-projects/perception/data/initial_feeds.csv

# Check CSV content
cat /home/jeremy/000-projects/perception/data/initial_feeds.csv

# Verify enabled column has "true" values
```

### "MCP endpoint not responding"

**Symptom:** `Connection refused` or `timeout` errors

**Causes:**
- MCP service not running
- Wrong port (should be 8080)
- Wrong MCP_BASE_URL

**Fix:**
```bash
# Check MCP service is running
ps aux | grep uvicorn

# Check port
curl http://localhost:8080/health

# Start MCP service if needed
cd /home/jeremy/000-projects/perception/app/mcp_service
uvicorn main:app --reload --port 8080
```

### "All articles have empty content"

**Symptom:** Articles returned but `content` field is null/empty

**Causes:**
- RSS feed doesn't provide full content (only snippets)
- MCP normalization rules not handling feed structure

**Fix:**
- Check `content_snippet` field (should have data)
- Phase 6: Use webpage scraping tool to fetch full content

---

**Last Updated:** 2025-11-14
**Status:** Phase 5 Complete - Agent 1 → MCP Integration Working
**Next:** Phase 6 (Firestore Integration + Parallel Fetching)
