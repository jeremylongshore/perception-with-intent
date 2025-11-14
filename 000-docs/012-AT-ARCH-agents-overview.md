# Perception With Intent - Agent Architecture Overview

**Version:** 1.0
**Date:** 2025-11-14
**Status:** Phase 3 - Agent Cards Defined

---

## Overview

Perception With Intent uses **8 distinct agents** deployed within a single Vertex AI Agent Engine instance. Each agent has a clearly defined role, inputs, outputs, and tool set. This is NOT one agent with multiple personalities—these are 8 separate ADK Agent instances coordinated by Agent 0 (the Orchestrator).

**Architecture Pattern:**
- **Monolithic Deployment:** All 8 agents deployed as a single Agent Engine app initially
- **Future:** Can be split into multiple Agent Engine deployments connected via A2A Protocol
- **Communication:** Agents communicate via ADK's A2A mechanisms within the same deployment

---

## Agent 0 – Perception Orchestrator

- **agent_id:** `perception_orchestrator`
- **Role:** Acts as Editor-in-Chief and master coordinator. It runs the end-to-end ingestion workflow: read sources and topics, instruct sub-agents to fetch, filter, summarize, alert, validate, and store data, then log the run.
- **Inputs:**
  - Firestore:
    - `/sources/{sourceId}` – active sources to ingest
    - `/users/{userId}/topics/{topicId}` – topics to consider when ranking relevance
  - Outputs from:
    - Agent 1 (fetched raw articles)
    - Agent 3 (scored articles)
    - Agent 4 (daily brief)
    - Agent 5 (alerts)
- **Outputs:**
  - Triggers writes (via sub-agents 6 & 7) into:
    - `/articles/{articleId}`
    - `/briefs/{briefId}`
    - `/ingestion_runs/{runId}`
  - Returns:
    - A high-level status object for each "daily_ingestion" run (success/failure, counts)
- **Tools Used (logical names):**
  - `agent_0_tools` – orchestration helpers:
    - Start an ingestion run (create `/ingestion_runs/{runId}` stub)
    - Call sub-agents in sequence/parallel
    - Aggregate results for logging/reporting
- **Trigger:**
  - Scheduled (e.g., Cloud Scheduler hitting Agent Engine endpoint each morning)
  - Manual "Run Ingestion Now" trigger from the dashboard backend
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Editor-in-Chief of Perception With Intent.

    Your job is to orchestrate a complete ingestion run each time you are invoked:
    1. Read active sources and user topics.
    2. Ask Source Harvester to fetch raw articles from configured sources.
    3. Ask Relevance & Ranking to score and filter the articles.
    4. Ask Brief Writer to generate an executive daily brief.
    5. Ask Alert & Anomaly Detector to determine whether any alerts should fire.
    6. Ask Validator to verify data structures.
    7. Ask Storage Manager to write validated data to Firestore and finalize the ingestion run record.

    Always:
    - Prefer useful, structured outputs over long prose.
    - Fail loudly with clear error messages if a critical sub-step fails.
  ```

---

## Agent 1 – Source Harvester

- **agent_id:** `perception_source_harvester`
- **Role:** Reads configured sources and fetches raw articles. It is responsible for talking to MCP tools that understand RSS, APIs, or web pages, and returning a normalized list of candidate articles.
- **Inputs:**
  - Firestore:
    - `/sources/{sourceId}` – enabled sources with type, URL, and category
  - Configuration:
    - Initial list of sources seeded from `data/initial_feeds.csv`
  - Orchestrator:
    - Receives a run context (run_id, time window, optional topic hints)
- **Outputs:**
  - Returns to the Orchestrator:
    - A list of normalized article dictionaries:
      - `title`, `url`, `source_id`, `published_at`, `raw_content`, `category`, etc.
  - Optionally writes temporary/raw data to an internal Firestore location in later phases (not required now)
- **Tools Used (logical names):**
  - `agent_1_tools` – source harvesting helpers:
    - `load_sources_from_firestore` – read enabled sources
    - `fetch_rss_feed` – MCP call for RSS
    - `fetch_api_feed` – MCP call for JSON APIs
    - `fetch_webpage` – MCP call for HTML pages
- **Trigger:**
  - Always invoked by the Orchestrator during an ingestion run; never triggered directly by UI
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Source Harvester for Perception With Intent.

    Given an ingestion context, you:
    1. Read enabled sources from Firestore.
    2. For each source, call the appropriate MCP tool (RSS, API, web page).
    3. Normalize all results into a common article structure with:
       - title
       - url
       - source_id
       - published_at (ISO8601)
       - content or excerpt
       - category if known
    4. Return the list of articles to the Orchestrator.

    Do not filter for relevance; return everything you can successfully fetch.
  ```

---

## Agent 2 – Topic Manager

- **agent_id:** `perception_topic_manager`
- **Role:** Manages what topics the system is monitoring. Provides CRUD operations for user topics and returns the current active topic list when requested by the Orchestrator or Relevance agent.
- **Inputs:**
  - Firestore:
    - `/users/{userId}/topics/{topicId}` – user-specific topics
  - User requests:
    - Create, read, update, delete topic configurations
  - Orchestrator:
    - Request for current active topics during ingestion
- **Outputs:**
  - Returns to caller:
    - List of active topics with keywords, categories, and thresholds
  - Writes to Firestore:
    - `/users/{userId}/topics/{topicId}` – topic CRUD operations
- **Tools Used (logical names):**
  - `agent_2_tools` – topic management helpers:
    - `get_active_topics` – read from Firestore
    - `create_topic` – add new topic
    - `update_topic` – modify existing topic
    - `delete_topic` – remove topic
    - `validate_topic_structure` – ensure topic has required fields
- **Trigger:**
  - Invoked by Orchestrator during ingestion (read-only)
  - Invoked by Dashboard API for topic management (CRUD)
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Topic Manager for Perception With Intent.

    Responsibilities:
    - Manage user topics (create, read, update, delete).
    - Validate topic structures (keywords, categories, thresholds).
    - Provide active topic lists to the Orchestrator and Relevance agent.

    When creating or updating topics:
    - Ensure required fields are present (name, keywords).
    - Validate keyword format and category values.
    - Set reasonable defaults for missing optional fields.
  ```

---

## Agent 3 – Relevance & Ranking

- **agent_id:** `perception_relevance_ranking`
- **Role:** Scores and filters articles by topic relevance. Uses Gemini to analyze article content against user topics and assign relevance scores (1-10). Returns ranked, filtered articles to the Orchestrator.
- **Inputs:**
  - From Orchestrator:
    - List of raw articles from Agent 1 (Source Harvester)
    - List of active topics from Agent 2 (Topic Manager)
  - Firestore (optional):
    - Historical relevance patterns for learning
- **Outputs:**
  - Returns to Orchestrator:
    - Filtered list of articles with:
      - `relevance_score` (1-10)
      - `matched_topics` (array of topic IDs)
      - `matched_keywords` (array of keywords that triggered match)
      - `importance_score` (overall importance calculation)
- **Tools Used (logical names):**
  - `agent_3_tools` – relevance scoring helpers:
    - `score_article_relevance` – use Gemini to score article against topics
    - `match_article_to_topics` – identify which topics match
    - `calculate_importance` – compute overall importance score
    - `filter_by_threshold` – remove articles below relevance threshold
- **Trigger:**
  - Always invoked by Orchestrator during ingestion
  - Never triggered directly by UI or external sources
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Relevance & Ranking specialist for Perception With Intent.

    Given a list of raw articles and active topics:
    1. For each article, use Gemini to analyze content against all topics.
    2. Assign a relevance score (1-10) for each topic match.
    3. Identify which topics and keywords matched.
    4. Calculate an overall importance score.
    5. Filter out articles below the relevance threshold (default: 5).
    6. Return ranked, scored articles to the Orchestrator.

    Be analytical and objective—favor precision over recall.
  ```

---

## Agent 4 – Summarization / Brief Writer

- **agent_id:** `perception_brief_writer`
- **Role:** Generates executive daily briefs from top-ranked articles. Creates concise summaries with key highlights, strategic implications, and metrics. Outputs well-structured briefing documents.
- **Inputs:**
  - From Orchestrator:
    - List of top-scored articles (filtered by Agent 3)
    - Ingestion run metadata (date, source counts, etc.)
  - Firestore (optional):
    - Previous briefs for consistency and trend analysis
- **Outputs:**
  - Returns to Orchestrator:
    - Daily brief object with:
      - `date` (YYYY-MM-DD)
      - `executive_summary` (1-2 sentence headline)
      - `highlights` (3-7 key bullet points)
      - `strategic_implications` (per topic if applicable)
      - `metrics` (article counts, top sources, main topics)
  - Will be written to:
    - `/briefs/{briefId}` by Agent 7 (Storage Manager)
- **Tools Used (logical names):**
  - `agent_4_tools` – brief generation helpers:
    - `generate_executive_summary` – create headline summary
    - `extract_highlights` – identify 3-7 key points
    - `analyze_strategic_implications` – assess business impact
    - `calculate_brief_metrics` – compute stats for brief
- **Trigger:**
  - Always invoked by Orchestrator during ingestion
  - Only runs after Agent 3 provides filtered articles
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Brief Writer for Perception With Intent.

    Given top-ranked articles from today's ingestion:
    1. Create a concise executive summary (1-2 sentences).
    2. Extract 3-7 key highlights that decision-makers need to know.
    3. Analyze strategic implications per topic if relevant.
    4. Calculate metrics: article count, top sources, main topics.
    5. Return well-structured brief object to Orchestrator.

    Keep tone neutral and analytical. Focus on what matters, not what's just interesting.
  ```

---

## Agent 5 – Alert & Anomaly Detector

- **agent_id:** `perception_alert_anomaly`
- **Role:** Watches for spikes, sentiment shifts, and threshold violations. Evaluates user-defined alert conditions and detects anomalies in article patterns. Returns list of triggered alerts.
- **Inputs:**
  - From Orchestrator:
    - Current articles and their scores
    - Historical context from previous runs
  - Firestore:
    - `/users/{userId}/alerts/{alertId}` – user-defined alert rules
  - Context:
    - Time-series data for trend analysis
- **Outputs:**
  - Returns to Orchestrator:
    - List of triggered alerts with:
      - `alert_id`
      - `trigger_reason` (spike, sentiment shift, threshold violation)
      - `severity` (low, medium, high)
      - `details` (what changed and why it matters)
- **Tools Used (logical names):**
  - `agent_5_tools` – alert detection helpers:
    - `check_keyword_frequency` – detect spikes in keyword mentions
    - `analyze_sentiment_shift` – identify sentiment changes
    - `evaluate_thresholds` – check user-defined alert conditions
    - `detect_anomalies` – statistical anomaly detection
- **Trigger:**
  - Always invoked by Orchestrator during ingestion
  - Runs after Agent 3 provides scored articles
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Alert & Anomaly Detector for Perception With Intent.

    Given current articles and historical context:
    1. Check for keyword frequency spikes.
    2. Analyze sentiment shifts from baseline.
    3. Evaluate user-defined alert thresholds.
    4. Detect statistical anomalies in article patterns.
    5. Return list of triggered alerts with severity and details.

    Prioritize actionable alerts over noise. False positives waste time.
  ```

---

## Agent 6 – Validator

- **agent_id:** `perception_validator`
- **Role:** Quality control before storage. Validates article schemas, detects duplicates, and verifies data quality. Acts as gatekeeper ensuring only clean, valid data reaches Firestore.
- **Inputs:**
  - From Orchestrator:
    - Articles to validate (from Agents 1 & 3)
    - Brief to validate (from Agent 4)
    - Alerts to validate (from Agent 5)
  - Firestore (for duplicate checking):
    - Existing `/articles/{articleId}` by URL hash
- **Outputs:**
  - Returns to Orchestrator:
    - Validation report with:
      - `valid_articles` (passed all checks)
      - `invalid_articles` (failed validation with reasons)
      - `duplicate_articles` (already exist in Firestore)
      - `data_quality_score` (overall quality metric)
- **Tools Used (logical names):**
  - `agent_6_tools` – validation helpers:
    - `validate_article_schema` – check required fields
    - `detect_duplicates` – URL/hash matching against Firestore
    - `verify_data_quality` – content checks (min length, encoding, etc.)
    - `validate_brief_structure` – ensure brief has required fields
- **Trigger:**
  - Always invoked by Orchestrator before storage
  - Never triggered directly
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Validator for Perception With Intent.

    Before data is stored:
    1. Validate article schemas (required fields present and correct type).
    2. Detect duplicates by URL hash against existing Firestore data.
    3. Verify data quality (content length, encoding, sanitization).
    4. Validate brief structure has all required fields.
    5. Return validation report with valid/invalid/duplicate classifications.

    Be strict. Better to reject bad data than pollute the database.
  ```

---

## Agent 7 – Storage Manager

- **agent_id:** `perception_storage_manager`
- **Role:** Persists validated data to Firestore. Handles all database writes including articles, briefs, and ingestion run finalization. Ensures transactional consistency and handles errors gracefully.
- **Inputs:**
  - From Orchestrator (via Agent 6):
    - Validated articles
    - Validated brief
    - Ingestion run metadata
  - From Agent 5:
    - Triggered alerts to log
- **Outputs:**
  - Writes to Firestore:
    - `/articles/{articleId}` – article documents
    - `/briefs/{briefId}` – daily brief documents
    - `/ingestion_runs/{runId}` – run completion and stats
  - Returns to Orchestrator:
    - Storage confirmation with:
      - `articles_stored` (count)
      - `brief_stored` (boolean)
      - `run_finalized` (boolean)
      - `errors` (any storage failures)
- **Tools Used (logical names):**
  - `agent_7_tools` – storage helpers:
    - `store_articles` – batch write to `/articles`
    - `store_brief` – write to `/briefs`
    - `log_ingestion_run` – finalize `/ingestion_runs/{runId}`
    - `deduplicate_by_url` – prevent duplicate writes
    - `handle_storage_errors` – retry logic and error logging
- **Trigger:**
  - Always invoked by Orchestrator as final step
  - Only runs after Agent 6 validates data
- **Example Instruction Block (YAML style):**
  ```yaml
  instruction: |
    You are the Storage Manager for Perception With Intent.

    Given validated data from the Orchestrator:
    1. Store articles to /articles collection (batch write).
    2. Store brief to /briefs collection.
    3. Finalize ingestion run record with stats and completion timestamp.
    4. Handle any storage errors with retries and clear logging.
    5. Return storage confirmation with counts and error details.

    Ensure transactional consistency. If writes fail, report clearly and don't mark run as complete.
  ```

---

## Agent Communication Flow

```
User/Scheduler
    ↓
Agent 0 (Orchestrator)
    ├──→ Agent 2 (Topic Manager) → Returns active topics
    ├──→ Agent 1 (Source Harvester) → Returns raw articles
    ├──→ Agent 3 (Relevance & Ranking) → Returns scored articles
    ├──→ Agent 4 (Brief Writer) → Returns daily brief
    ├──→ Agent 5 (Alert & Anomaly) → Returns triggered alerts
    ├──→ Agent 6 (Validator) → Returns validation report
    └──→ Agent 7 (Storage Manager) → Persists to Firestore
```

---

## Deployment Architecture

**Current (Phase 3):**
- Single Agent Engine deployment containing all 8 agents
- Agent 0 references sub-agents via local YAML config paths
- All communication happens via ADK's internal A2A mechanisms

**Future (Phase 7+):**
- Each agent can be deployed as separate Agent Engine instance
- Communication via A2A Protocol over HTTP
- Allows independent scaling and deployment of each agent

---

## File Structure

```
app/perception_agent/
├── agents/
│   ├── agent_0_orchestrator.yaml          # Root orchestrator
│   ├── agent_1_source_harvester.yaml      # Fetches articles
│   ├── agent_2_topic_manager.yaml         # Manages topics
│   ├── agent_3_relevance_ranking.yaml     # Scores articles
│   ├── agent_4_brief_writer.yaml          # Generates briefs
│   ├── agent_5_alert_anomaly.yaml         # Detects alerts
│   ├── agent_6_validator.yaml             # Validates data
│   └── agent_7_storage_manager.yaml       # Persists to Firestore
│
├── tools/
│   ├── agent_0_tools.py                   # Orchestration helpers
│   ├── agent_1_tools.py                   # Source harvesting
│   ├── agent_2_tools.py                   # Topic CRUD
│   ├── agent_3_tools.py                   # Relevance scoring
│   ├── agent_4_tools.py                   # Brief generation
│   ├── agent_5_tools.py                   # Alert detection
│   ├── agent_6_tools.py                   # Validation helpers
│   └── agent_7_tools.py                   # Firestore writes
│
└── prompts/
    └── (Optional: agent-specific prompt templates)
```

---

**Last Updated:** 2025-11-14
**Phase:** 3 (Agent Cards Defined)
**Next:** Phase 4 (MCP Tool Architecture + First Real Tool Wiring)
