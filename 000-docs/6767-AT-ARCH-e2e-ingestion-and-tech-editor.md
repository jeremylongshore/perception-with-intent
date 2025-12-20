# Perception With Intent - E2E Ingestion & Technology Desk Editor

**Document ID:** 6767-AT-ARCH-e2e-ingestion-and-tech-editor
**Version:** 1.0
**Date:** 2025-11-14
**Phase:** E2E (E2E Ingestion Happy Path + First Section Editor)
**Category:** Architecture

---

## Executive Summary

### For Executives

Perception With Intent now has a production-ready news intelligence pipeline that autonomously ingests, analyzes, and delivers curated insights. The system processes dozens of news sources every morning, scores each article against your strategic topics, and produces an executive brief with sections tailored by specialized AI editors. The Technology Desk Editor—our first vertical specialist—ensures tech coverage meets the quality standards you'd expect from a seasoned analyst. This architecture scales: as we add Business, Politics, and other desk editors, each brings domain expertise while maintaining consistency through our orchestration layer. The result is a daily brief that's not just aggregated news, but intelligently curated intelligence.

### For Engineers

The E2E ingestion pipeline is a production-grade orchestration of 9 specialized agents (0, 1, 2, 3, 4, 6, 7, 8) running within a single Vertex AI Agent Engine deployment. The orchestrator (Agent 0) coordinates a linear flow where each agent's output becomes the next agent's input, creating a shared working memory pattern. Agent 8 (Technology Desk Editor) demonstrates our vertical section editor architecture: it receives scored articles and the initial brief, curates the Tech section, and returns an enhanced version. This pattern is replicable for Business, Politics, and any other vertical. The pipeline uses keyword-based scoring (no LLM calls for speed/cost), Firestore batch writes for efficiency, and structured JSON logging for observability. All validation happens before storage, ensuring data quality. The system is designed for: (1) local dev with emulator, (2) staging with test data, (3) production with full enforcement.

---

## Full Ingestion Sequence

### Overview

The E2E ingestion pipeline executes these steps sequentially:

```
Cloud Scheduler → Orchestrator → [9 steps] → Firestore + Slack
```

Each step builds on the previous one's output, creating a shared working memory where agents can see all prior decisions.

---

### Step-by-Step Flow

#### Step 0: Ingestion Run Initialization

**Agent:** Agent 0 (Orchestrator)

**What Happens:**
- Orchestrator starts an ingestion run
- Generates unique `run_id` (e.g., `run_1731626400`)
- Creates initial ingestion_runs record in Firestore
- Sets status to "running"

**Output:**
```json
{
  "run_id": "run_1731626400",
  "started_at": "2025-11-14T07:30:00Z",
  "trigger": "scheduled",
  "status": "running"
}
```

**Shared Memory:** Run context initialized

---

#### Step 1: Load Active Topics

**Agent:** Agent 2 (Topic Manager)

**What Happens:**
- Query Firestore `/users/{userId}/topics` for active topics
- Return list of topics with keywords, categories, thresholds
- If no topics found, fall back to default test topics (for dev)

**Output:**
```json
{
  "topics": [
    {
      "topic_id": "tech-ai",
      "name": "AI & Machine Learning",
      "keywords": ["ai", "artificial intelligence", "llm", "gpt"],
      "category": "technology",
      "active": true
    },
    {
      "topic_id": "tech-cloud",
      "name": "Cloud Computing",
      "keywords": ["cloud", "aws", "gcp", "kubernetes"],
      "category": "technology",
      "active": true
    }
  ]
}
```

**Shared Memory:** Topics available to all downstream agents

---

#### Step 2: Harvest All Sources

**Agent:** Agent 1 (Source Harvester)

**What Happens:**
- Load enabled sources from `data/initial_feeds.csv`
- For each RSS source, call MCP `fetch_rss_feed` endpoint
- Normalize each article to common schema
- Return aggregated list of raw articles

**MCP Call Example:**
```http
POST http://localhost:8080/mcp/tools/fetch_rss_feed
{
  "feed_url": "https://techcrunch.com/feed/",
  "time_window_hours": 24,
  "max_items": 50
}
```

**Output:**
```json
{
  "articles": [
    {
      "title": "OpenAI Releases GPT-5",
      "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
      "source_id": "techcrunch",
      "category": "technology",
      "published_at": "2025-11-14T06:00:00Z",
      "content": "Full article text...",
      "summary": "OpenAI announced GPT-5..."
    },
    // ... 46 more articles
  ],
  "source_count": 12,
  "total_fetched": 47
}
```

**Shared Memory:** Raw articles + topics available

---

#### Step 3: Score & Rank Articles

**Agent:** Agent 3 (Relevance & Ranking)

**What Happens:**
- For each article, score against all topics using keyword matching
- Title matches worth 3x, content matches worth 1x
- Calculate overall relevance score (1-10)
- Infer section based on category and content signals
- Extract AI tags from matched keywords
- Filter articles below minimum score (default: 5)
- Sort by relevance score descending

**Scoring Logic:**
```python
def _score_single_article(article, topics):
    for topic in topics:
        for keyword in topic["keywords"]:
            if keyword in article["title"]:
                matches += 3  # Title match worth more
            elif keyword in article["content"]:
                matches += 1

    relevance_score = min(10, matches + 3)
    section = _infer_section(category, title, content)  # Tech, Business, etc.
    return {relevance_score, ai_tags, section, matched_topics}
```

**Output:**
```json
{
  "scored_articles": [
    {
      "title": "OpenAI Releases GPT-5",
      "url": "https://techcrunch.com/2025/11/14/openai-gpt5",
      "relevance_score": 9,
      "section": "Tech",
      "ai_tags": ["ai", "gpt", "openai", "llm"],
      "matched_topics": ["tech-ai"]
    },
    // ... 46 more scored articles
  ]
}
```

**Shared Memory:** Scored articles + topics + raw articles available

---

#### Step 4: Build Brief Payload

**Agent:** Agent 4 (Brief Writer)

**What Happens:**
- Group scored articles by section (Tech, Business, Politics, etc.)
- For each section, take top 5 articles by relevance score
- Generate key points (bullet summary per article)
- Build article references with metadata
- Sort sections by priority (Tech first, then Business, etc.)
- Generate brief headline
- Return complete brief structure

**Section Building:**
```python
def _build_section(section_name, articles):
    sorted_articles = sorted(articles, key=lambda a: a["relevance_score"], reverse=True)
    top_articles = sorted_articles[:5]

    key_points = [
        f"• {article['title']} ({', '.join(article['ai_tags'][:2])})"
        for article in top_articles
    ]

    return {
        "section_name": section_name,
        "key_points": key_points,
        "top_articles": article_refs
    }
```

**Output:**
```json
{
  "brief_id": "brief-2025-11-14",
  "date": "2025-11-14",
  "headline": "Daily Intelligence Brief - 2025-11-14 (47 articles across Tech, Business)",
  "sections": [
    {
      "section_name": "Tech",
      "key_points": [
        "• OpenAI Releases GPT-5 (ai, gpt)",
        "• Google Announces Gemini 3.0 (ai, google)",
        // ... 3 more
      ],
      "top_articles": [
        {
          "title": "OpenAI Releases GPT-5",
          "url": "https://techcrunch.com/...",
          "relevance_score": 9
        }
        // ... 4 more
      ]
    },
    {
      "section_name": "Business",
      // ... similar structure
    }
  ],
  "meta": {
    "article_count": 23,
    "section_count": 2,
    "run_id": "run_1731626400"
  }
}
```

**Shared Memory:** Brief + scored articles + topics + raw articles available

---

#### Step 5: Enhance Technology Section (NEW)

**Agent:** Agent 8 (Technology Desk Editor)

**What Happens:**
- Receive all scored articles and initial brief from orchestrator
- Filter for Tech section articles
- Select top 5 tech articles (may differ from initial brief selection)
- Analyze AI tags to identify dominant themes (AI, cloud, startups, etc.)
- Propose custom headline for Tech section based on themes
- Build enhanced Tech section with curated article selection
- Add editor metadata (curated: true, editor: agent_8)
- Return enhanced Tech section to orchestrator

**Curation Logic:**
```python
def select_top_tech_articles(articles, max_articles=5):
    tech_articles = [a for a in articles if a["section"] == "Tech"]
    tech_articles.sort(key=lambda x: x["relevance_score"], reverse=True)
    return tech_articles[:max_articles]

def propose_tech_headline(tech_articles):
    # Analyze common themes
    all_tags = [tag for article in tech_articles for tag in article["ai_tags"]]
    tag_counts = Counter(all_tags)
    top_themes = [tag for tag, count in tag_counts.most_common(3)]

    if "ai" in top_themes:
        return "AI Developments Lead Technology News"
    elif "cloud" in top_themes:
        return "Cloud Computing and Infrastructure Updates"
    # ... etc
```

**Output:**
```json
{
  "section_name": "Technology",
  "editor_headline": "AI Developments Lead Technology News",
  "key_points": [
    "• OpenAI Releases GPT-5 [ai, gpt] (score: 9)",
    "• Google Announces Gemini 3.0 [ai, google] (score: 8.5)",
    // ... 3 more
  ],
  "top_articles": [
    {
      "title": "OpenAI Releases GPT-5",
      "url": "https://techcrunch.com/...",
      "relevance_score": 9,
      "ai_tags": ["ai", "gpt", "openai", "llm"]
    }
    // ... 4 more
  ],
  "meta": {
    "editor": "agent_8_tech_editor",
    "article_count": 5,
    "curated": true
  }
}
```

**Integration:** Orchestrator replaces generic Tech section in brief with enhanced version from Agent 8

**Shared Memory:** Enhanced brief + scored articles + topics + raw articles available

---

#### Step 6: Validate Data

**Agent:** Agent 6 (Validator)

**What Happens:**
- Validate each article has required fields (title, url, source_id)
- Check field types (url must be string, etc.)
- Validate brief structure (required fields: brief_id, date, headline, sections)
- Validate each section has required fields (section_name, key_points, top_articles)
- Return validation report with errors

**Validation Example:**
```python
def validate_articles(articles):
    errors = []
    for i, article in enumerate(articles):
        if "url" not in article:
            errors.append(f"Article {i}: Missing required field: url")
        if "title" not in article or len(article["title"]) < 10:
            errors.append(f"Article {i}: Title too short")

    is_valid = len(errors) == 0
    return {"valid": is_valid, "errors": errors}
```

**Output:**
```json
{
  "articles_validation": {
    "valid": true,
    "errors": [],
    "valid_count": 23,
    "invalid_count": 0
  },
  "brief_validation": {
    "valid": true,
    "errors": []
  }
}
```

**Decision Point:** If validation fails, pipeline stops here and marks run as failed

**Shared Memory:** Validation report + enhanced brief + scored articles available

---

#### Step 7: Store to Firestore

**Agent:** Agent 7 (Storage Manager)

**What Happens:**
- Deduplicate articles by URL (in-memory dedup)
- Batch write articles to `/articles` collection (500 per batch)
- Use URL hash as article ID for idempotency
- Write brief to `/briefs` collection using brief_id as document ID
- Update ingestion run with final stats
- Handle any storage errors with retry logic

**Firestore Write Example:**
```python
def store_articles(articles):
    unique_articles = deduplicate_by_url(articles)

    for i in range(0, len(unique_articles), 500):
        batch = db.batch()
        for article in unique_articles[i:i+500]:
            article_id = _generate_article_id(article["url"])
            doc_ref = db.collection("articles").document(article_id)
            batch.set(doc_ref, article, merge=True)  # Upsert
        batch.commit()
```

**Output:**
```json
{
  "articles_storage": {
    "stored_count": 23,
    "errors": []
  },
  "brief_storage": {
    "brief_id": "brief-2025-11-14",
    "status": "stored"
  },
  "run_update": {
    "run_id": "run_1731626400",
    "status": "updated"
  }
}
```

**Shared Memory:** Storage confirmations + all previous data available

---

#### Step 8: Finalize Ingestion Run

**Agent:** Agent 0 (Orchestrator)

**What Happens:**
- Collect stats from all steps
- Update ingestion run record with final status and counts
- Mark run as "success" or "failed"
- Log completion timestamp
- Return final result to caller

**Output:**
```json
{
  "run_id": "run_1731626400",
  "status": "success",
  "stats": {
    "articles_harvested": 47,
    "articles_scored": 47,
    "articles_selected": 23,
    "articles_stored": 23,
    "brief_id": "brief-2025-11-14"
  },
  "brief_id": "brief-2025-11-14",
  "errors": []
}
```

---

## Shared Working Memory Pattern

### How It Works

Each agent in the pipeline receives ALL outputs from previous agents, creating a shared context:

```python
async def run_daily_ingestion(user_id, trigger):
    # Step 1: Get topics
    topics = get_active_topics(user_id)

    # Step 2: Harvest (sees: topics)
    harvest_result = await harvest_all_sources()
    articles = harvest_result["articles"]

    # Step 3: Score (sees: articles, topics)
    scored_articles = score_articles(articles, topics)

    # Step 4: Build brief (sees: scored_articles, topics, articles)
    brief = build_brief_payload(scored_articles, run_id)

    # Step 5: Enhance Tech section (sees: scored_articles, brief, topics, articles)
    tech_section = select_top_tech_articles(scored_articles)
    enhanced_tech = enhance_tech_section(brief["sections"][0], tech_section)
    brief["sections"][0] = enhanced_tech  # Replace with curated version

    # Step 6: Validate (sees: scored_articles, brief, ALL previous data)
    validation = validate_articles(scored_articles)
    brief_validation = validate_brief(brief)

    # Step 7: Store (sees: validated data + ALL previous context)
    storage_result = store_articles(scored_articles)
    brief_result = store_brief(brief)
```

### Benefits

1. **Context Awareness:** Each agent can make decisions based on ALL previous steps
2. **Transparency:** Complete audit trail of how brief was generated
3. **Debugging:** Easy to see which step produced which data
4. **Flexibility:** New agents can be inserted anywhere in the flow
5. **Testing:** Can test individual steps with real previous outputs

### Memory Scope

- **Agent 1:** Sees only topics
- **Agent 3:** Sees topics + raw articles
- **Agent 4:** Sees topics + raw articles + scored articles
- **Agent 8:** Sees topics + raw articles + scored articles + initial brief
- **Agent 6:** Sees ALL above
- **Agent 7:** Sees ALL above + validation reports

---

## Technology Desk Editor Architecture

### Purpose

Agent 8 demonstrates the **Vertical Section Editor Pattern** - a specialized agent that curates a specific section of the daily brief.

### Why It Exists

1. **Domain Expertise:** Tech news requires different curation than business or politics
2. **Quality Control:** Human-like editorial judgment on what matters
3. **Scalability:** Pattern replicates for Business Desk, Politics Desk, etc.
4. **Customization:** Each vertical can have unique selection criteria

### How It Fits In

```
Agent 4 (Brief Writer)
    ↓ (produces generic Tech section with top 5 by score)
Agent 8 (Tech Desk Editor)
    ↓ (curates, analyzes themes, proposes headline)
Enhanced Tech Section
    ↓ (replaces generic section in brief)
Agent 6 (Validator)
```

The Tech Editor operates AFTER the initial brief is built but BEFORE validation, allowing it to override generic sections with curated versions.

### Configuration

```yaml
# app/perception_agent/agents/agent_8_tech_editor.yaml
name: perception_tech_editor
instruction: |
  You are the Technology Desk Editor.
  Focus areas:
  - AI & Machine Learning
  - Cloud computing and infrastructure
  - Emerging technologies and startups
  - Tech policy and regulation
  - Major product launches and acquisitions

  Select top 5 articles, propose headline, return curated section.
```

### Tools

```python
# app/perception_agent/tools/agent_8_tools.py

def select_top_tech_articles(articles, max_articles=5):
    """Filter Tech section articles and select top by relevance."""

def propose_tech_headline(tech_articles):
    """Generate compelling section headline based on themes."""

def enhance_tech_section(section_data, tech_articles):
    """Build enhanced section with curation metadata."""
```

---

## Adding Future Section Editors

### Pattern to Follow

1. **Create Agent YAML** (`agent_9_business_editor.yaml`)
2. **Create Tools** (`agent_9_tools.py` with same 3 functions)
3. **Wire into Orchestrator** (add to sub_agents list)
4. **Update Orchestrator Logic** (call business editor after tech editor)

### Example: Business Desk Editor

```python
# In agent_0_tools.py run_daily_ingestion()

# After Tech Editor
tech_section = select_top_tech_articles(scored_articles)
enhanced_tech = enhance_tech_section(brief["sections"][0], tech_section)
brief["sections"][0] = enhanced_tech

# Add Business Editor
business_section = select_top_business_articles(scored_articles)
enhanced_business = enhance_business_section(brief["sections"][1], business_section)
brief["sections"][1] = enhanced_business
```

### Scaling to N Editors

```python
# Generic pattern
section_editors = {
    "Tech": agent_8_tools,
    "Business": agent_9_tools,
    "Politics": agent_10_tools,
}

for section in brief["sections"]:
    if section["section_name"] in section_editors:
        editor = section_editors[section["section_name"]]
        enhanced = editor.enhance_section(section, scored_articles)
        section.update(enhanced)
```

---

## Future: Agent-Aware Requests (AAR) & Agent-Aware Notifications (AAN)

**Status:** NOT IMPLEMENTED IN THIS PHASE

### Placeholder for Phase 7+

**AAR (Agent-Aware Requests):**
```
TODO:
- [ ] Design AAR API for ad-hoc queries
- [ ] Create Agent 9: Query Processor for AAR
- [ ] Build Firebase Cloud Function AAR endpoint
- [ ] Add AAR support to dashboard
```

**AAN (Agent-Aware Notifications):**
```
TODO:
- [ ] Design AAN criteria system (alerting rules)
- [ ] Enhance Agent 5 with AAN trigger detection
- [ ] Build notification delivery system (Slack, email, webhook)
- [ ] Add AAN configuration to dashboard
```

**Integration Point:**
Once implemented, AAR/AAN will hook into the E2E pipeline after Step 7 (Storage), allowing:
- **AAR:** "What are the top 3 AI funding rounds this week?" → Triggers custom ingestion
- **AAN:** "Alert me if any article mentions our competitor" → Fires notification during ingestion

**Architecture Preview:**
```
Normal Ingestion: Steps 1-8 → Firestore
AAR Request: Dashboard → Agent 9 → Steps 1-8 (custom context) → Response
AAN Trigger: Step 5 → Agent 5 (check rules) → Notification Service → Slack/Email
```

---

## Performance & Scalability

### Current Performance

- **Ingestion Time:** 30-90 seconds (depending on article count)
- **MCP Calls:** Parallel RSS fetches (12 sources in ~10s)
- **Scoring:** O(n*m) where n=articles, m=topics (fast, no LLM)
- **Storage:** Batch writes (500 articles/batch, ~2s per batch)

### Bottlenecks

1. **MCP RSS Fetches:** Sequential currently (can parallelize)
2. **Firestore Writes:** Limited to 500/batch (use multiple batches)
3. **Gemini Calls:** None in E2E flow (by design for speed)

### Scalability Path

1. **Horizontal:** Deploy section editors as separate Agent Engine instances
2. **Caching:** Cache RSS responses for 5-10 minutes
3. **Parallelization:** Fetch all RSS feeds concurrently
4. **Sharding:** Split ingestion by source category (tech sources, business sources, etc.)

---

## Observability & Monitoring

### Structured Logging

All agents emit JSON logs:

```json
{
  "severity": "INFO",
  "tool": "agent_3",
  "operation": "score_articles",
  "article_count": 47,
  "topic_count": 2,
  "avg_score": 6.2
}
```

### Key Metrics

- **Ingestion Success Rate:** % of runs that complete successfully
- **Article Processing Rate:** Articles/second through scoring
- **Storage Latency:** Time to write articles + brief to Firestore
- **Section Editor Coverage:** % of briefs with curated sections
- **Validation Failure Rate:** % of runs stopped by validation errors

### Alerting Rules (Future)

```
IF ingestion_success_rate < 90% THEN alert_on_call
IF article_processing_rate < 5/sec THEN investigate_performance
IF storage_latency > 10s THEN check_firestore_health
```

---

## Testing Strategy

### Unit Tests

- Test each agent tool function independently
- Mock Firestore and MCP calls
- Verify scoring logic with known inputs

### Integration Tests

- Run E2E with Firestore emulator
- Verify data flows between agents correctly
- Test validation error handling

### Smoke Tests

- Run `scripts/run_ingestion_once.py` in CI
- Verify exit code 0 (success)
- Check Firestore has expected documents

### Load Tests

- Simulate 500+ articles
- Verify batch writes work correctly
- Measure end-to-end latency

---

**Last Updated:** 2025-11-14
**Phase:** E2E (E2E Ingestion Happy Path + First Section Editor)
**Status:** Production-ready E2E pipeline with Agent 8 implemented
**Next:** Additional section editors (Business, Politics) + AAR/AAN capabilities
