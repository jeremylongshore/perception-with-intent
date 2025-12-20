# Perception With Intent - Dev Ingestion Run Guide

**Document ID:** 6767-OD-GUID-dev-ingestion-run
**Version:** 1.0
**Date:** 2025-11-14
**Phase:** E2E (E2E Ingestion Happy Path + First Section Editor)
**Category:** Operational Guide

---

## Overview

This guide explains how to run a complete ingestion cycle locally for development and testing purposes. The E2E ingestion pipeline runs all agents from source harvesting through brief generation, validation, and storage.

## Prerequisites

### Required Services

1. **MCP Service Running**
   ```bash
   cd app/mcp_service
   source ../../.venv/bin/activate
   uvicorn main:app --reload --port 8080
   ```
   - Should be accessible at `http://localhost:8080`
   - Check health: `curl http://localhost:8080/health`

2. **Firestore** (choose one):
   - **Option A:** Firestore Emulator (recommended for dev)
     ```bash
     firebase emulators:start --only firestore
     export FIRESTORE_EMULATOR_HOST="localhost:8081"
     ```
   - **Option B:** Production Firestore
     ```bash
     gcloud config set project perception-with-intent
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
     ```

3. **RSS Feeds Data**
   - Ensure `data/initial_feeds.csv` exists with enabled feeds
   - Sample feeds are pre-configured in the repo

### Environment Setup

```bash
# Navigate to project root
cd /home/jeremy/000-projects/perception

# Activate virtual environment
source .venv/bin/activate

# Set environment variables
export MCP_BASE_URL="http://localhost:8080"  # MCP service URL
export GOOGLE_CLOUD_PROJECT="perception-with-intent"
export FIRESTORE_EMULATOR_HOST="localhost:8081"  # Optional: for emulator
```

---

## Running Ingestion

### Basic Usage

```bash
python scripts/run_ingestion_once.py
```

This runs a single ingestion cycle with default settings:
- User ID: `system`
- Trigger: `manual_dev`

### With Custom Parameters

```bash
# Run for specific user
python scripts/run_ingestion_once.py --user-id user_12345

# Run with custom trigger
python scripts/run_ingestion_once.py --trigger "testing_e2e"

# Enable verbose logging
python scripts/run_ingestion_once.py --verbose
```

### What Happens During Ingestion

The script executes the following sequence:

1. **Agent 0 (Orchestrator)**
   - Starts ingestion run and generates `run_id`

2. **Agent 2 (Topic Manager)**
   - Loads active topics
   - Falls back to default test topics if none exist

3. **Agent 1 (Source Harvester)**
   - Loads enabled sources from `data/initial_feeds.csv`
   - Calls MCP `fetch_rss_feed` for each source
   - Normalizes articles to common structure

4. **Agent 3 (Relevance & Ranking)**
   - Scores articles against topics (keyword matching)
   - Infers section (Tech, Business, Politics, etc.)
   - Filters articles with relevance score ≥ 5

5. **Agent 4 (Brief Writer)**
   - Groups articles by section
   - Builds brief payload with sections and key points
   - Generates brief headline

6. **Agent 8 (Technology Desk Editor)**
   - Selects top tech articles
   - Proposes custom tech section headline
   - Enhances Tech section with curation metadata

7. **Agent 6 (Validator)**
   - Validates article schema (required fields, types)
   - Validates brief structure (sections, fields)
   - Reports validation errors

8. **Agent 7 (Storage Manager)**
   - Stores validated articles to `/articles` collection
   - Stores brief to `/briefs` collection
   - Updates ingestion run record with final stats

9. **Agent 0 (Orchestrator)**
   - Finalizes ingestion run
   - Returns complete result with stats and errors

---

## Expected Output

### Success

```
============================================================
INGESTION RUN COMPLETE
============================================================
Run ID: run_1731626400
Status: success
Brief ID: brief-2025-11-14

Stats:
  articles_harvested: 47
  articles_scored: 47
  articles_selected: 23
  articles_stored: 23
  brief_id: brief-2025-11-14

============================================================
```

### With Errors

```
============================================================
INGESTION RUN COMPLETE
============================================================
Run ID: run_1731626500
Status: failed
Brief ID: None

Stats:
  articles_harvested: 12
  articles_scored: 12
  articles_selected: 5
  articles_stored: 0
  brief_id: brief-2025-11-14

Errors (2):
  1. Article 3: Missing required field: url
  2. Brief storage failed: Connection refused

============================================================
```

---

## Checking Results

### Firestore Emulator UI

If using emulator, view results at: `http://localhost:4000/firestore`

### Firestore Production

```bash
# View articles
gcloud firestore documents list --collection=articles --limit=10

# View briefs
gcloud firestore documents list --collection=briefs --limit=5

# View ingestion runs
gcloud firestore documents list --collection=ingestion_runs --limit=5
```

### Query Specific Brief

```python
from google.cloud import firestore

db = firestore.Client()
brief_ref = db.collection('briefs').document('brief-2025-11-14')
brief = brief_ref.get().to_dict()

print(f"Brief: {brief['headline']}")
print(f"Sections: {len(brief['sections'])}")
for section in brief['sections']:
    print(f"  - {section['section_name']}: {len(section['top_articles'])} articles")
```

---

## Troubleshooting

### MCP Service Not Running

**Error:** `Connection refused to http://localhost:8080`

**Solution:**
```bash
cd app/mcp_service
uvicorn main:app --reload --port 8080
```

### No Articles Harvested

**Error:** `No enabled sources found`

**Solution:**
- Check `data/initial_feeds.csv` exists
- Ensure at least one feed has `enabled=true`
- Verify CSV format:
  ```csv
  source_id,name,type,url,category,enabled
  techcrunch,TechCrunch,rss,https://techcrunch.com/feed/,technology,true
  ```

### Firestore Permission Denied

**Error:** `Permission denied on Firestore`

**Solution:**
- Set service account credentials:
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
  ```
- Or use emulator:
  ```bash
  export FIRESTORE_EMULATOR_HOST="localhost:8081"
  ```

### Validation Errors

**Error:** `Validation failed, stopping pipeline`

**Check:**
- Review logged validation errors in output
- Common issues:
  - Missing required fields (title, url, source_id)
  - Invalid field types (non-string URL, non-list sections)
  - Empty sections in brief

---

## Development Workflow

### Typical Dev Cycle

1. **Start Services**
   ```bash
   # Terminal 1: MCP Service
   cd app/mcp_service && uvicorn main:app --reload --port 8080

   # Terminal 2: Firestore Emulator (optional)
   firebase emulators:start --only firestore
   ```

2. **Make Code Changes**
   - Edit agent tools in `app/perception_agent/tools/`
   - Edit agent configs in `app/perception_agent/agents/`

3. **Test Changes**
   ```bash
   python scripts/run_ingestion_once.py --verbose
   ```

4. **Inspect Results**
   - Check Firestore emulator UI: http://localhost:4000
   - Review structured logs in terminal
   - Query Firestore collections

5. **Iterate**
   - Fix issues
   - Re-run ingestion
   - Verify fixes

### Smoke Testing

Run quick smoke test to verify all agents functional:

```bash
# Should complete in < 2 minutes with test feeds
time python scripts/run_ingestion_once.py

# Verify exit code
echo $?  # Should be 0 for success
```

---

## Advanced Usage

### Testing Specific Scenarios

**Test with no topics (uses defaults):**
```bash
# Temporarily rename topics in Firestore or use clean emulator
python scripts/run_ingestion_once.py
```

**Test with many articles:**
- Add more feeds to `data/initial_feeds.csv`
- Run ingestion
- Verify batch writes work correctly

**Test validation failures:**
- Modify article normalization to omit required field
- Run ingestion
- Verify pipeline stops and logs errors

### Integration with CI/CD

Add to CI pipeline for smoke testing:

```.github/workflows/ci-smoke.yml
jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Start MCP Service
        run: uvicorn app.mcp_service.main:app --port 8080 &
      - name: Run Ingestion Smoke Test
        run: python scripts/run_ingestion_once.py
```

---

## Monitoring and Observability

### Structured Logs

All logs are JSON-formatted for easy parsing:

```json
{
  "severity": "INFO",
  "tool": "agent_3",
  "operation": "score_articles",
  "article_count": 47,
  "topic_count": 2
}
```

### Key Metrics to Track

- **Articles Harvested:** How many articles fetched
- **Articles Scored:** How many passed through scoring
- **Articles Selected:** How many met relevance threshold
- **Articles Stored:** How many written to Firestore
- **Processing Time:** End-to-end latency

### Log Filtering

```bash
# View only errors
python scripts/run_ingestion_once.py 2>&1 | grep '"severity":"ERROR"'

# View specific agent
python scripts/run_ingestion_once.py 2>&1 | grep '"tool":"agent_3"'

# Track article counts
python scripts/run_ingestion_once.py 2>&1 | grep 'article_count'
```

---

**Last Updated:** 2025-11-14
**Phase:** E2E (E2E Ingestion Happy Path + First Section Editor)
**Next:** Run first ingestion test, verify all agents functional
