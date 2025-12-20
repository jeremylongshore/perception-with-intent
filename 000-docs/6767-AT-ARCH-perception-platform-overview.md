# Perception With Intent: Platform Architecture Overview

**Version:** 1.0
**Date:** 2025-11-14
**Classification:** Executive Briefing / Investor Material
**Purpose:** Comprehensive architectural study guide for technical evaluation and strategic positioning

---

## Executive Overview

### What is Perception?

**Perception With Intent** is an enterprise-grade AI news intelligence platform that transforms overwhelming information streams into actionable strategic intelligence. Unlike traditional news aggregators that create more noise, Perception employs a multi-agent AI architecture to deliver signal — the stories that actually matter to decision-makers.

**Core Value Proposition:**
- Executives don't need 10,000 articles. They need the 10 that matter.
- Traditional tools amplify noise. Perception eliminates it.
- Intelligence, not information. Strategy, not summaries.

### How It Works Today

Perception deploys **8 specialized AI agents** on Google Cloud's Vertex AI Agent Engine, each with a specific role in the intelligence pipeline:

| Agent | Role | Function |
|-------|------|----------|
| **Agent 0** | Editor-in-Chief (Orchestrator) | Coordinates daily workflow, manages priorities |
| **Agent 1** | Source Harvester | Fetches articles from RSS, APIs, web sources |
| **Agent 2** | Topic Manager | Tracks what matters to your organization |
| **Agent 3** | Relevance Guru | Scores articles: "Is this worth executive time?" |
| **Agent 4** | Article Analyst | Generates summaries, extracts insights, tags content |
| **Agent 5** | Daily Synthesizer | Creates executive brief: "Here's what matters today" |
| **Agent 6** | Quality Checker | Validates data integrity, flags anomalies |
| **Agent 7** | Delivery Driver | Sends intelligence to Slack, email, dashboard |

**Daily Workflow (Automated):**
1. 7:30 AM CST: Orchestrator wakes up via Cloud Scheduler
2. Source Harvester fetches 500+ articles from configured feeds
3. Relevance Guru scores each article (0-10 scale)
4. Article Analyst processes top 50 articles
5. Quality Checker validates output
6. Daily Synthesizer composes executive brief
7. Delivery Driver sends to Slack + Dashboard
8. **Result:** 5-minute read instead of 2-hour scroll

### Why This Architecture is Enterprise-Grade

**Built on Google Cloud's Premium Infrastructure:**
- **Vertex AI Agent Engine:** Google's managed multi-agent orchestration platform
- **Cloud Run:** Serverless, auto-scaling, zero-ops compute
- **Firestore Native Mode:** Real-time database with ACID guarantees
- **BigQuery:** Unlimited analytics on historical intelligence
- **Gemini 2.0 Flash:** State-of-the-art AI model (not OpenAI)

**Production-Ready Design:**
- Workload Identity Federation (WIF): Keyless GitHub → GCP authentication
- Internal-only MCP services: Backend services never exposed to public internet
- Structured JSON logging: Full observability with Cloud Logging
- Auto-scaling: Scale to zero when idle, infinite when busy
- SPIFFE IDs: Know exactly which service is doing what

### Why This is Uniquely Strong for News Intelligence

**Traditional Approach (Fails at Scale):**
```
RSS Aggregator → Firehose of articles → Overwhelmed executive
```

**Perception Approach (Signal from Noise):**
```
Multi-Agent Pipeline → Relevance Filtering → Strategic Intelligence → Actionable Brief
```

**Key Differentiators:**
1. **Agents think, tools do:** Clean separation of AI reasoning from execution
2. **Horizontal scalability:** Add agents without touching existing ones
3. **Vertical intelligence:** Each agent masters ONE function
4. **Contextual memory:** Agents remember what you care about
5. **Adaptive learning:** System gets smarter about your priorities over time

---

## Core Intelligent Architecture (Today's System)

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  HUMAN INTERFACE LAYER                          │
│                                                                  │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐│
│  │ Firebase Hosting │  │  Slack Bot      │  │ Email Delivery ││
│  │ (React Dashboard)│  │  Integration    │  │   Service      ││
│  └──────────────────┘  └─────────────────┘  └────────────────┘│
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓ (Users query / view intelligence)
┌─────────────────────────────────────────────────────────────────┐
│              VERTEX AI AGENT ENGINE (The Brain)                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Agent 0: Editor-in-Chief (Orchestrator)                  │  │
│  │   • Coordinates daily workflow                            │  │
│  │   • Manages agent priorities                              │  │
│  │   • Handles ad-hoc user queries                           │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                            │
│      ┌──────────────┼──────────────┐                            │
│      │              │              │                            │
│      ↓              ↓              ↓                            │
│  ┌────────┐    ┌────────┐    ┌────────┐                        │
│  │Agent 1 │    │Agent 2 │    │Agent 3 │    (Parallel)          │
│  │Harvest │    │Topics  │    │Relevance│                        │
│  └────┬───┘    └───┬────┘    └───┬────┘                        │
│       │            │             │                              │
│       └────────────┼─────────────┘                              │
│                    ↓                                             │
│  ┌────────┐    ┌────────┐    ┌────────┐                        │
│  │Agent 4 │    │Agent 5 │    │Agent 6 │                        │
│  │Analyze │    │Synthesize│  │Validate│                        │
│  └────┬───┘    └───┬────┘    └───┬────┘                        │
│       │            │             │                              │
│       └────────────┼─────────────┘                              │
│                    ↓                                             │
│            ┌───────────────┐                                     │
│            │   Agent 7     │                                     │
│            │   Deliver     │                                     │
│            └───────┬───────┘                                     │
│                    │                                             │
│  All agents communicate via A2A Protocol                        │
│  (Agent-to-Agent: Google's inter-agent messaging)               │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ↓ (Agents call MCP tools)
┌─────────────────────────────────────────────────────────────────┐
│          CLOUD RUN MCP SERVICES (The Toolbox)                   │
│                                                                  │
│  MCP = Model Context Protocol (dumb tools, not AI)              │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │ NewsIngestionMCP│  │  TopicsMCP     │  │ RelevanceMCP     │ │
│  │ • Fetch RSS     │  │ • Read topics  │  │ • Score articles │ │
│  │ • Parse feeds   │  │ • Update topics│  │ • Rank by score  │ │
│  └────────────────┘  └────────────────┘  └──────────────────┘ │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │  LLMToolsMCP   │  │  StorageMCP    │  │ ValidationMCP    │ │
│  │ • Summarize    │  │ • Save to DB   │  │ • Check quality  │ │
│  │ • Extract tags │  │ • Read from DB │  │ • Flag errors    │ │
│  └────────────────┘  └────────────────┘  └──────────────────┘ │
│                                                                  │
│  ┌────────────────┐                                             │
│  │  DeliveryMCP   │                                             │
│  │ • Send to Slack│                                             │
│  │ • Send email   │                                             │
│  │ • Webhook push │                                             │
│  └────────────────┘                                             │
│                                                                  │
│  Ingress: internal-and-cloud-load-balancing ONLY               │
│  Auth: No unauthenticated access                               │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ↓ (Data persists here)
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Firestore Native Mode (Real-Time + ACID)                 │  │
│  │                                                            │  │
│  │  • topics_to_monitor      - What we're tracking          │  │
│  │  • articles               - Everything we've analyzed     │  │
│  │  • daily_summaries        - Executive briefs             │  │
│  │  • run_metrics            - How well we're doing         │  │
│  │  • agent_memory           - Working memory               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ BigQuery (Analytics + Long-Term Memory)                   │  │
│  │                                                            │  │
│  │  • articles_archive       - All articles ever processed  │  │
│  │  • relevance_scores       - Historical scoring patterns  │  │
│  │  • topic_trends           - Topic evolution over time    │  │
│  │  • agent_performance      - Which agents are effective   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### The 8 Specialized Agents (Detail)

#### Agent 0: Editor-in-Chief (Orchestrator)

**Role:** Chief executive of the intelligence pipeline

**Responsibilities:**
- Coordinates daily 7:30 AM workflow execution
- Manages priorities across all agents
- Handles ad-hoc queries from users ("What's happening with Tesla?")
- Decides which agents to invoke and in what order
- Monitors overall system health

**Technology:**
- Vertex AI Agent Engine deployment
- A2A protocol for agent-to-agent communication
- Event-driven via Pub/Sub triggers
- Gemini 2.0 Flash model

**Example Orchestration Flow:**
```
1. Receive Pub/Sub trigger: "daily_run_7:30am"
2. Call Agent 2: "What are we tracking today?"
3. Call Agent 1: "Fetch articles for these topics" (parallel)
4. Call Agent 3: "Score these 500 articles"
5. Call Agent 4: "Analyze top 50 articles"
6. Call Agent 6: "Validate the output"
7. Call Agent 5: "Create daily brief"
8. Call Agent 7: "Deliver to Slack + Dashboard"
9. Log metrics to Firestore
```

#### Agent 1: Source Harvester

**Role:** Fetch articles from the world

**Responsibilities:**
- Load configured news sources (RSS, APIs, web scraping)
- Fetch latest articles from each source
- Normalize article metadata (title, URL, date, author)
- Handle malformed feeds gracefully
- Track source reliability metrics

**Technology:**
- Calls NewsIngestionMCP via HTTP
- CSV-based source config (Phase 1-2) → Firestore sources (Phase 3+)
- Time window filtering (last 24 hours by default)
- Async/await for parallel fetching

**Example Tool Call:**
```python
await fetch_rss(
    feed_url="https://techcrunch.com/feed/",
    time_window_hours=24,
    max_items=50
)
# Returns: List of 50 articles from last 24 hours
```

#### Agent 2: Topic Manager

**Role:** Track what matters

**Responsibilities:**
- Maintain list of topics organization cares about
- Add new topics based on user requests
- Archive stale topics
- Provide topic context to other agents
- Generate topic trend reports

**Technology:**
- Calls TopicsMCP for CRUD operations
- Firestore `topics_to_monitor` collection
- Supports keywords, categories, priority levels
- Topic expiration rules

**Example Topics:**
```json
{
  "topic_id": "ai-regulation-2025",
  "keywords": ["AI regulation", "AI safety", "AI governance"],
  "category": "technology",
  "priority": "high",
  "active": true,
  "created_at": "2025-01-01T00:00:00Z"
}
```

#### Agent 3: Relevance Guru

**Role:** Separate signal from noise

**Responsibilities:**
- Score each article on 0-10 scale
- Factors: topic match, source authority, recency, uniqueness
- Filter out duplicates and low-value content
- Rank articles by strategic importance
- Learn from user feedback (future)

**Technology:**
- Calls RelevanceMCP for scoring algorithms
- Uses Gemini 2.0 Flash for semantic understanding
- Scoring rubric customizable per organization
- Stores scores in Firestore for learning

**Scoring Rubric (Example):**
```
Topic Match:     0-3 points (Does this match our topics?)
Source Authority: 0-2 points (Is this a trusted source?)
Recency:         0-2 points (Is this breaking news?)
Uniqueness:      0-2 points (Is this new information?)
Impact:          0-1 points (Does this affect our business?)
Total:           0-10 points
```

**Output:**
```
500 articles → Relevance scoring → Top 50 articles (score ≥ 7.0)
```

#### Agent 4: Article Analyst

**Role:** Extract intelligence from articles

**Responsibilities:**
- Generate 3-sentence summaries
- Extract key entities (companies, people, locations)
- Tag with categories (technology, regulation, market, etc.)
- Identify sentiment (positive, negative, neutral)
- Flag strategic implications

**Technology:**
- Calls LLMToolsMCP for AI-powered analysis
- Gemini 2.0 Flash for summarization
- Entity extraction via NLP
- Structured output (JSON schema)

**Example Analysis:**
```json
{
  "article_id": "tc-12345",
  "summary": "OpenAI announced GPT-5 with 10x improvement in reasoning. Expected release Q2 2025. Pricing TBD.",
  "entities": {
    "companies": ["OpenAI"],
    "people": ["Sam Altman"],
    "technologies": ["GPT-5"]
  },
  "tags": ["AI", "product-launch", "competitive-intelligence"],
  "sentiment": "neutral",
  "strategic_impact": "high"
}
```

#### Agent 5: Daily Synthesizer

**Role:** Create the executive brief

**Responsibilities:**
- Compose daily intelligence brief (5-minute read)
- Group articles by theme
- Highlight top stories
- Include strategic recommendations
- Format for readability

**Technology:**
- Calls StorageMCP to read analyzed articles
- Uses Gemini 2.0 Flash for synthesis
- Markdown formatting for dashboard
- Slack-optimized formatting for notifications

**Example Brief Structure:**
```markdown
# Daily Intelligence Brief - November 14, 2025

## Top Stories (3)
1. **OpenAI Releases GPT-5** - Major competitive shift in AI market
2. **EU AI Act Enforcement Begins** - Regulatory compliance deadline approaching
3. **Tesla Autonomy Update** - Full Self-Driving v12 rolling out

## By Category

### Technology (5 stories)
- OpenAI GPT-5 announcement
- Google Gemini 3.0 preview
- ...

### Regulation (2 stories)
- EU AI Act enforcement
- ...

## Strategic Implications
- Consider impact of GPT-5 on our product roadmap
- Review EU AI Act compliance status
```

#### Agent 6: Quality Checker

**Role:** Validate everything

**Responsibilities:**
- Check data integrity (no broken URLs, missing fields)
- Detect duplicate articles
- Flag anomalies (unusual source behavior)
- Verify scoring consistency
- Alert on system errors

**Technology:**
- Calls ValidationMCP for validation rules
- Schema validation (Pydantic models)
- Duplicate detection (URL hashing)
- Error thresholds and alerting

**Validation Rules:**
```python
- All articles must have: title, url, published_at
- URLs must be unique (deduplicate)
- Scores must be 0-10
- Summaries must be 50-500 characters
- No profanity in executive brief
```

#### Agent 7: Delivery Driver

**Role:** Get intelligence to humans

**Responsibilities:**
- Send brief to Slack channel
- Email digest to executives
- Update Firebase dashboard
- Trigger webhooks for integrations
- Track delivery success/failure

**Technology:**
- Calls DeliveryMCP for notification services
- Slack Bolt SDK for Slack integration
- SendGrid for email delivery
- Firebase Cloud Functions for real-time dashboard updates

**Example Slack Message:**
```
🗞️ *Daily Intelligence Brief - November 14, 2025*

*Top Stories:*
1. OpenAI Releases GPT-5 - Major competitive shift
2. EU AI Act Enforcement Begins - Compliance deadline
3. Tesla Autonomy Update - FSD v12 rolling out

📊 47 articles analyzed | 8 topics tracked | 3 high-priority alerts

👉 Full brief: https://perception-with-intent.web.app
```

### MCP Toolchain Architecture

**MCP = Model Context Protocol:** Dumb tools that do ONE thing well

**Design Principles:**
1. **Agents think, MCPs do:** Agents orchestrate intelligence, MCPs execute tasks
2. **One tool, one job:** Each MCP has a single responsibility
3. **Backend-only:** MCP services are never exposed to public internet
4. **Minimal IAM:** Each MCP has only the permissions it needs
5. **Idempotent:** Same input → Same output (no side effects)

**MCP Services (7 Total):**

| MCP | Responsibility | Input | Output |
|-----|---------------|-------|--------|
| NewsIngestionMCP | Fetch RSS/API feeds | feed_url, time_window | List of articles |
| TopicsMCP | Manage topics | topic CRUD operations | Topic data |
| RelevanceMCP | Score articles | Article metadata | Relevance score (0-10) |
| LLMToolsMCP | AI analysis | Article text | Summary, tags, entities |
| StorageMCP | Save to Firestore | Article objects | Confirmation |
| ValidationMCP | Check quality | Article objects | Pass/fail + errors |
| DeliveryMCP | Send notifications | Brief text | Delivery status |

**Example MCP API:**
```
POST https://perception-mcp-abc123-uc.a.run.app/tools/fetch_rss_feed

Request:
{
  "feed_url": "https://techcrunch.com/feed/",
  "time_window_hours": 24,
  "max_items": 50
}

Response:
{
  "articles": [
    {
      "title": "OpenAI Releases GPT-5",
      "url": "https://techcrunch.com/...",
      "published_at": "2025-11-14T08:00:00Z",
      "summary": "...",
      "author": "John Doe",
      "categories": ["AI", "Product Launch"]
    },
    ...
  ],
  "metadata": {
    "feed_url": "https://techcrunch.com/feed/",
    "article_count": 47,
    "latency_ms": 274
  }
}
```

### Cloud Run Backend Pattern

**Why Cloud Run for MCPs?**

1. **Serverless:** No servers to manage, auto-scaling, pay-per-request
2. **Internal-only ingress:** Backend services never exposed to public
3. **Sub-second cold starts:** Fast enough for real-time intelligence
4. **Built-in observability:** Logs, metrics, traces out of the box
5. **Cost-effective:** Scale to zero when idle, $0 when not in use

**Security Configuration:**
```bash
gcloud run deploy perception-mcp \
  --ingress internal-and-cloud-load-balancing \
  --no-allow-unauthenticated \
  --service-account mcp-service@perception-with-intent.iam.gserviceaccount.com
```

**This means:**
- ✅ Agent Engine can call MCP (internal network)
- ✅ Cloud Load Balancer can route to MCP (if configured)
- ❌ Public internet CANNOT reach MCP
- ❌ React dashboard CANNOT call MCP directly (must go through agents)

### Firestore Schema

**Collection: `topics_to_monitor`**
```json
{
  "topic_id": "ai-regulation-2025",
  "keywords": ["AI regulation", "AI safety"],
  "category": "technology",
  "priority": "high",
  "active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-11-14T08:00:00Z"
}
```

**Collection: `articles`**
```json
{
  "article_id": "tc-12345-2025-11-14",
  "title": "OpenAI Releases GPT-5",
  "url": "https://techcrunch.com/...",
  "source_id": "techcrunch",
  "category": "technology",
  "published_at": "2025-11-14T08:00:00Z",
  "fetched_at": "2025-11-14T07:30:00Z",
  "relevance_score": 9.2,
  "summary": "OpenAI announced GPT-5...",
  "tags": ["AI", "product-launch"],
  "entities": {
    "companies": ["OpenAI"],
    "people": ["Sam Altman"]
  },
  "strategic_impact": "high"
}
```

**Collection: `daily_summaries`**
```json
{
  "summary_id": "2025-11-14",
  "date": "2025-11-14",
  "article_count": 47,
  "top_stories": [
    {
      "title": "OpenAI Releases GPT-5",
      "url": "...",
      "why_it_matters": "Major competitive shift"
    }
  ],
  "by_category": {
    "technology": [/* articles */],
    "regulation": [/* articles */]
  },
  "strategic_implications": [
    "Review product roadmap impact",
    "Assess competitive positioning"
  ],
  "generated_at": "2025-11-14T08:00:00Z",
  "delivered_to": ["slack", "email", "dashboard"]
}
```

### Shared Working Memory + Long-Term Memory

**Working Memory (Firestore):**
- Real-time access for agents
- Current run state
- Recent articles (last 30 days)
- Active topics
- Delivery status

**Long-Term Memory (BigQuery):**
- Historical articles (all time)
- Trend analysis
- Scoring pattern evolution
- Agent performance metrics
- Topic lifecycle data

**Memory Flow:**
```
Agent processes article → Firestore (working memory)
↓ (daily batch job)
BigQuery (long-term memory) ← Analytics queries
```

### A2A Protocol (Agent-to-Agent Communication)

**What is A2A?**
- Google's protocol for inter-agent communication
- Agents send structured messages to each other
- Orchestrator coordinates, agents execute
- Asynchronous, event-driven architecture

**Example A2A Message:**
```json
{
  "from_agent": "agent_0_orchestrator",
  "to_agent": "agent_1_source_harvester",
  "message_type": "request",
  "operation": "harvest_all_sources",
  "parameters": {
    "time_window_hours": 24,
    "max_items_per_source": 50
  },
  "request_id": "daily_run_2025-11-14_07:30"
}
```

**Response:**
```json
{
  "from_agent": "agent_1_source_harvester",
  "to_agent": "agent_0_orchestrator",
  "message_type": "response",
  "request_id": "daily_run_2025-11-14_07:30",
  "status": "success",
  "result": {
    "articles_fetched": 487,
    "sources_processed": 11,
    "errors": 0
  }
}
```

### Observability / Telemetry Stack

**Current (Phase 1-2):**
- Structured JSON logging (Cloud Logging)
- Cloud Run metrics (latency, error rate, instance count)
- Manual monitoring via Cloud Console

**Future (Phase 3+):**
- OpenTelemetry tracing (full request traces)
- Custom dashboards (Grafana on Cloud Run)
- SLI/SLO tracking (uptime, latency, accuracy)
- Alerting (PagerDuty integration)
- Cost attribution (per-agent cost tracking)

**Example Log Entry:**
```json
{
  "severity": "INFO",
  "timestamp": "2025-11-14T07:30:45.123Z",
  "tool": "agent_1",
  "operation": "fetch_rss",
  "feed_url": "https://techcrunch.com/feed/",
  "article_count": 47,
  "latency_ms": 274,
  "request_id": "daily_run_2025-11-14_07:30"
}
```

---

## Why This Architecture Sells

### 1. Latency Advantages

**Traditional Aggregator:**
```
User opens app → Load 500 articles → Scroll for 2 hours → Still unsure what matters
Time to value: 2+ hours
```

**Perception:**
```
7:30 AM: System processes 500 articles → 8:00 AM: Brief ready → User reads 5 minutes
Time to value: 5 minutes
```

**Why it's fast:**
- Parallel agent execution (8 agents work simultaneously)
- MCP services on Cloud Run (sub-second response times)
- Firestore real-time database (no query lag)
- Pre-computed intelligence (daily run, not on-demand)

### 2. Horizontal Scalability

**Adding new capabilities:**
```
Old way: Rewrite monolithic app → Test everything → Deploy (weeks)
Perception: Add new agent → Wire to orchestrator → Deploy (hours)
```

**Example: Add sentiment analysis**
```
1. Create Agent 8: Sentiment Analyzer
2. Add to orchestrator workflow after Agent 4
3. Deploy new agent YAML
4. Done. No changes to existing agents.
```

**Why it scales:**
- Agents are independent (no tight coupling)
- A2A protocol handles communication (standard interface)
- MCP tools are stateless (infinite horizontal scale)
- Firestore auto-scales (no database tuning needed)

### 3. Extensibility

**Today's use case: Executive news intelligence**

**Tomorrow's use cases (same architecture):**
- Legal intelligence (track court cases, regulatory changes)
- Financial intelligence (earnings, M&A, market moves)
- Competitive intelligence (competitor product launches)
- HR intelligence (industry hiring trends, salary data)
- Sales intelligence (prospect news, buying signals)

**Add new vertical = Add new agent + Configure topics**

No architectural changes needed.

### 4. Enterprise Observability

**What executives see:**
```
Dashboard:
- 47 articles processed today ✅
- 8 topics tracked ✅
- 3 high-priority alerts ⚠️
- Daily brief delivered 8:05 AM ✅
```

**What engineers see:**
```
Cloud Logging:
- Agent 1 latency: 274ms (p95)
- Agent 3 accuracy: 94.2% (last 30 days)
- MCP error rate: 0.03%
- Daily run duration: 4m 23s
```

**What CFOs see:**
```
Cost Dashboard:
- Monthly spend: ~$70
- Per-article cost: $0.003
- Per-user cost: $7/month
- ROI: 100x (saves 10 hours/week @ $100/hour = $1000/week)
```

### 5. Separation of Concerns (Agents Think, MCP Tools Do)

**Why this matters:**

| Layer | Responsibility | Technology | Upgrade Path |
|-------|---------------|------------|--------------|
| Agents | Intelligence, orchestration | Gemini 2.0 Flash | Swap model, no code changes |
| MCP Tools | Execution, data access | Python FastAPI | Update tool, agents unaffected |
| Data | Storage, analytics | Firestore + BigQuery | Scale storage, no app changes |

**Example: Upgrade to GPT-5 (hypothetically)**
```
1. Change agent model config: gemini-2.0-flash → gpt-5
2. Redeploy agents
3. Done. No MCP changes. No schema changes.
```

### 6. Zero-Public-Attack-Surface Cloud Run MCP Pattern

**Traditional API:**
```
Public Internet → API Gateway → Backend Services
↑ (Attack surface: Entire internet)
```

**Perception MCP:**
```
Agent Engine (internal) → Cloud Run MCP (internal-only ingress) → Firestore
↑ (Attack surface: Zero. No public exposure.)
```

**Security benefits:**
- No API keys to leak
- No rate limiting needed (internal traffic only)
- No DDoS risk
- No CORS complexity
- Reduced compliance burden (HIPAA, SOC 2, etc.)

### 7. Why This is Better Than a Single Mega-Agent

**Mega-Agent Approach (Fails):**
```
Prompt:
"You are a news intelligence system. Fetch articles, score them, analyze them,
create a brief, and send to Slack. Here are 500 articles..."

Result:
- Context window overload (too much data)
- Inconsistent quality (does too many things)
- Hard to debug (black box)
- Can't scale (one agent = one bottleneck)
```

**Multi-Agent Approach (Wins):**
```
Agent 0: "Agent 1, fetch articles"
Agent 1: "Here are 487 articles" (passes to Agent 3)
Agent 3: "Top 50 articles scored" (passes to Agent 4)
Agent 4: "Analysis complete" (passes to Agent 5)
Agent 5: "Brief ready" (passes to Agent 7)
Agent 7: "Delivered to Slack" ✅

Result:
- Each agent masters ONE function
- Parallel execution (8x faster)
- Easy to debug (check each agent's output)
- Easy to scale (add more agents)
```

### 8. Cost Efficiency

**Traditional News Monitoring:**
```
Bloomberg Terminal: $2,000/month per user
Meltwater: $1,500/month per user
Manual analysis: 10 hours/week @ $100/hour = $4,000/month
```

**Perception:**
```
GCP infrastructure: ~$70/month
Supports 10+ users: $7/month per user
ROI: 200x+ for enterprise
```

**Why it's cheap:**
- Cloud Run scales to zero (no idle costs)
- Gemini 2.0 Flash is cheap (not GPT-4)
- Firestore Native Mode is cheap (not dedicated DB)
- Efficient agent design (no redundant work)

### 9. Compliance & Governance

**Enterprise requirements:**
- **Audit logs:** Every agent action logged to Cloud Logging
- **Data residency:** Deploy to specific GCP region (us-central1, eu-west1, etc.)
- **Access control:** IAM roles for who can deploy/modify agents
- **Data retention:** BigQuery for historical data (compliance archives)
- **GDPR compliance:** Data deletion on request (Firestore TTL policies)

### 10. Vendor Lock-In Mitigation

**Current: Google Cloud (Vertex AI, Cloud Run, Firestore)**

**Migration path (if needed):**
- Agents: OpenAI Assistants API, Azure OpenAI, AWS Bedrock
- MCP Services: AWS Lambda, Azure Functions, any Docker platform
- Data: MongoDB, PostgreSQL, Snowflake
- Dashboard: Any React hosting (Vercel, Netlify, AWS S3)

**Portability:**
- Agents are YAML configs (portable)
- MCP services are Docker containers (portable)
- Data is JSON (export/import anywhere)

### 11. Multi-Tenant SaaS Potential

**Today: Single organization (your company)**

**Tomorrow: SaaS platform**
```
Tier 1: Solo ($49/month)
- 1 user
- 5 topics
- Daily brief only

Tier 2: Team ($199/month)
- 10 users
- 20 topics
- Real-time alerts
- Slack integration

Tier 3: Enterprise ($999/month)
- Unlimited users
- Unlimited topics
- Custom agents
- API access
- Dedicated support
```

**Architecture supports multi-tenancy TODAY:**
- Firestore: Tenant ID field on all documents
- Agents: Filter by tenant_id
- MCP Services: Tenant-aware queries
- Dashboard: Tenant selection dropdown

### 12. AI Model Flexibility

**Not locked into one AI provider:**

| Agent | Current Model | Alternative Models |
|-------|--------------|-------------------|
| Agent 4 (Analysis) | Gemini 2.0 Flash | GPT-4o, Claude 3.5 Sonnet |
| Agent 5 (Synthesis) | Gemini 2.0 Flash | GPT-4o, Claude 3.5 Sonnet |
| Agent 3 (Scoring) | Rule-based + Gemini | Pure ML model (fine-tuned) |

**Future: Ensemble approach**
```
Agent 4: Use 3 models (Gemini, GPT, Claude)
Pick best summary via voting mechanism
Result: Higher quality than any single model
```

---

## Expansion Blueprint: The AI Newsroom

### Vision: From 8 Agents to Full Newsroom

**Today:** 8 specialized agents handling generic "news intelligence"

**Tomorrow:** 15-20 vertical-specific "editor" agents, each running their own desk

**Why this matters:**
- Real newsrooms have specialized desks (Business, Tech, Politics, Sports, etc.)
- Each desk has unique expertise, sources, and editorial standards
- Cross-desk collaboration creates comprehensive coverage
- Perception automates this proven organizational model

### The AI Newsroom Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                  EDITOR-IN-CHIEF (Agent 0)                      │
│  • Coordinates all desks                                        │
│  • Sets daily priorities                                        │
│  • Composes final edition                                       │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├───────────────┬───────────────┬──────────────┐
             │               │               │              │
             ↓               ↓               ↓              ↓
    ┌──────────────┐ ┌─────────────┐ ┌────────────┐ ┌────────────┐
    │ BUSINESS DESK│ │  TECH DESK  │ │POLITICS DESK│ │ INT'L DESK │
    │  (Agent 10)  │ │ (Agent 11)  │ │ (Agent 12)  │ │ (Agent 13) │
    └──────────────┘ └─────────────┘ └────────────┘ └────────────┘
             │               │               │              │
             ↓               ↓               ↓              ↓
    ┌──────────────┐ ┌─────────────┐ ┌────────────┐ ┌────────────┐
    │  LOCAL DESK  │ │ SPORTS DESK │ │ CRIME DESK │ │FINANCE DESK│
    │  (Agent 14)  │ │ (Agent 15)  │ │ (Agent 16) │ │ (Agent 17) │
    └──────────────┘ └─────────────┘ └────────────┘ └────────────┘
             │               │               │              │
             ↓               ↓               ↓              ↓
    ┌──────────────┐ ┌─────────────┐ ┌────────────┐
    │ OPINION DESK │ │BREAKING NEWS│ │  [CUSTOM]  │
    │  (Agent 18)  │ │  (Agent 19) │ │ (Agent 20) │
    └──────────────┘ └─────────────┘ └────────────┘
```

### Vertical Editor Agents (10+ Specialized Desks)

#### Agent 10: Business Desk Editor

**Coverage:** Corporate news, earnings, M&A, executive moves, market trends

**Specialized Prompt:**
```
You are the Business Desk Editor for Perception Intelligence.

Your beat:
- Earnings reports and financial results
- Mergers, acquisitions, and corporate restructuring
- Executive appointments and board changes
- Strategic partnerships and investments
- Market-moving business developments

Editorial voice:
- Focus on strategic implications for executives
- Emphasize competitive positioning
- Include financial context (revenue, growth, valuation)
- Flag insider trading implications

Scoring criteria:
- Company size/market cap weight
- Deal size significance
- Competitive intelligence value
- Relevance to portfolio companies
```

**Sources:**
- Wall Street Journal, Financial Times, Bloomberg
- Company press releases (IR websites)
- SEC filings (8-K, 10-K, 10-Q)
- Industry trade publications

**Example Output:**
```
Business Desk - Top 3 Stories Today:

1. **Microsoft Acquires AI Startup for $3B**
   - Strategic play to compete with OpenAI/Google
   - Acqui-hire of 200 ML engineers
   - Integration timeline: Q2 2026
   - *Why it matters:* Consolidation in AI infrastructure

2. **Tesla Q4 Earnings Beat**
   - Revenue: $28.5B (+15% YoY)
   - Automotive margins up to 23%
   - FSD adoption accelerating
   - *Why it matters:* EV profitability proof point

3. **Amazon CEO Stepping Down**
   - Andy Jassy to be replaced by AWS CEO
   - Signals AWS spin-off potential
   - Stock up 4% on news
   - *Why it matters:* Major leadership transition
```

#### Agent 11: Technology Desk Editor

**Coverage:** Product launches, AI breakthroughs, developer tools, cybersecurity

**Specialized Prompt:**
```
You are the Technology Desk Editor for Perception Intelligence.

Your beat:
- Product launches and updates (software, hardware, platforms)
- AI/ML breakthroughs and research
- Developer tools and infrastructure
- Cybersecurity incidents and vulnerabilities
- Platform policy changes

Editorial voice:
- Technical accuracy is paramount
- Explain implications for engineers and product teams
- Include technical specs when relevant
- Flag security/privacy concerns

Scoring criteria:
- Technical innovation level
- Adoption potential
- Competitive landscape impact
- Developer community sentiment
```

**Sources:**
- TechCrunch, The Verge, Ars Technica
- arXiv (AI research papers)
- GitHub trending, Hacker News
- Vendor blogs (Google Cloud, AWS, etc.)

#### Agent 12: Politics Desk Editor

**Coverage:** Legislation, regulation, policy, elections, government actions

**Specialized Prompt:**
```
You are the Politics Desk Editor for Perception Intelligence.

Your beat:
- Federal/state legislation affecting business
- Regulatory agency actions (FTC, SEC, FDA, etc.)
- Executive orders and policy changes
- Elections and political campaigns
- International policy and trade

Editorial voice:
- Nonpartisan, fact-based analysis
- Focus on business implications, not partisan spin
- Include timeline for regulatory changes
- Flag compliance requirements

Scoring criteria:
- Direct business impact
- Timeline urgency (when does this take effect?)
- Industry-specific relevance
- Enforcement likelihood
```

**Sources:**
- Politico, The Hill, Roll Call
- Federal Register (regulations)
- Congressional Research Service
- State legislature trackers

#### Agent 13: International Desk Editor

**Coverage:** Global news, geopolitics, trade, foreign policy, international business

**Specialized Prompt:**
```
You are the International Desk Editor for Perception Intelligence.

Your beat:
- International business developments
- Trade agreements and tariffs
- Geopolitical events affecting markets
- Foreign policy changes
- Global supply chain disruptions

Editorial voice:
- Focus on U.S. business implications
- Include currency/commodity impacts
- Explain regional context for U.S. readers
- Flag supply chain risks

Scoring criteria:
- Direct impact on U.S. companies
- Supply chain significance
- Market volatility potential
- Geopolitical risk level
```

**Sources:**
- Reuters, Associated Press, BBC
- Economist, Foreign Policy
- Regional sources (SCMP, Al Jazeera, etc.)

#### Agent 14: Local/Metro Desk Editor

**Coverage:** City/state news, local business, real estate, transportation

**Specialized Prompt:**
```
You are the Local/Metro Desk Editor for Perception Intelligence.

Your beat:
- Local business openings/closings
- Commercial real estate deals
- Infrastructure projects
- Local regulatory changes
- Community economic development

Editorial voice:
- Focus on local economic impact
- Include neighborhood/district context
- Emphasize job creation/loss
- Flag real estate trends

Scoring criteria:
- Economic impact ($, jobs)
- Relevance to user's location
- Trend indicator value
- Community significance
```

**Sources:**
- Local newspapers, business journals
- City planning departments
- Chamber of Commerce
- Local TV news

#### Agent 15: Sports Desk Editor

**Coverage:** Sports business, athlete news, league decisions, sponsorship deals

**Specialized Prompt:**
```
You are the Sports Desk Editor for Perception Intelligence.

Your beat:
- Sports business deals (team sales, sponsorships)
- Athlete endorsements and contracts
- League policy changes
- Sports betting and media rights
- Venue development

Editorial voice:
- Focus on business side, not game results
- Include financial details (contract values, etc.)
- Emphasize brand/marketing implications
- Flag legal/regulatory issues

Scoring criteria:
- Deal size significance
- Brand impact for sponsors
- Legal/policy implications
- Media/tech innovation
```

**Sources:**
- ESPN, Sports Business Journal
- Team press releases
- League announcements

#### Agent 16: Crime/Public Safety Desk Editor

**Coverage:** Corporate crime, fraud, cybersecurity incidents, regulatory enforcement

**Specialized Prompt:**
```
You are the Crime/Public Safety Desk Editor for Perception Intelligence.

Your beat:
- Corporate fraud and white-collar crime
- Cybersecurity breaches and incidents
- Regulatory enforcement actions
- Product recalls and safety issues
- Class-action lawsuits

Editorial voice:
- Focus on business impact, not sensationalism
- Include legal/compliance implications
- Explain technical details of cyber incidents
- Flag reputational risks

Scoring criteria:
- Company size/prominence
- Financial impact ($, fines)
- Legal precedent significance
- Consumer safety urgency
```

**Sources:**
- Justice Department press releases
- SEC enforcement actions
- Cybersecurity blogs (Krebs on Security, etc.)
- Court filings (PACER)

#### Agent 17: Financial Markets Desk Editor

**Coverage:** Markets, trading, investing, monetary policy, economic indicators

**Specialized Prompt:**
```
You are the Financial Markets Desk Editor for Perception Intelligence.

Your beat:
- Stock market movements and drivers
- Bond yields and interest rates
- Currency and commodity markets
- Federal Reserve policy
- Economic indicators (GDP, inflation, employment)

Editorial voice:
- Focus on market-moving news, not minute-by-minute prices
- Include analyst commentary/consensus
- Explain Fed policy implications
- Flag portfolio positioning signals

Scoring criteria:
- Market impact (volatility, volume)
- Economic indicator significance
- Policy implications
- Consensus vs. surprise
```

**Sources:**
- Bloomberg, MarketWatch, Seeking Alpha
- Federal Reserve statements
- Bureau of Labor Statistics, Census Bureau

#### Agent 18: Opinion/Analysis Desk Editor

**Coverage:** Expert commentary, thought leadership, trend analysis

**Specialized Prompt:**
```
You are the Opinion/Analysis Desk Editor for Perception Intelligence.

Your beat:
- Thought leadership from industry experts
- Long-form analysis and essays
- Trend forecasting and predictions
- Contrarian viewpoints
- Strategic frameworks

Editorial voice:
- Surface diverse viewpoints
- Include author credentials/expertise
- Flag data-backed vs. speculative claims
- Emphasize actionable insights

Scoring criteria:
- Author authority/expertise
- Data quality (if quantitative)
- Strategic relevance
- Contrarian value (challenges consensus)
```

**Sources:**
- Harvard Business Review, McKinsey Insights
- Substack newsletters
- LinkedIn thought leaders
- Academic journals

#### Agent 19: "Rapid Response" Breaking News Editor

**Coverage:** Breaking news, real-time events, crisis monitoring

**Specialized Prompt:**
```
You are the Rapid Response Breaking News Editor for Perception Intelligence.

Your beat:
- Breaking news that requires immediate attention
- Crisis events (natural disasters, incidents, outages)
- Market-moving announcements
- Emergency regulatory actions

Editorial voice:
- Speed is critical, accuracy is paramount
- Include "what we know" vs. "what we don't know"
- Flag developing situations
- Provide immediate action items if relevant

Scoring criteria:
- Urgency level (minutes/hours, not days)
- Direct business impact
- Information completeness
- Action required?
```

**Sources:**
- Twitter (verified accounts)
- Breaking news wires (Reuters, Bloomberg terminal)
- Emergency alert systems

### Cross-Desk Collaboration

**How desks work together:**

**Example: Tesla Announces New Factory in Texas**

1. **Business Desk (Agent 10):** "Major corporate investment - $5B factory"
2. **Tech Desk (Agent 11):** "Manufacturing tech - new battery production line"
3. **Local Desk (Agent 14):** "10,000 new jobs in Austin metro area"
4. **Politics Desk (Agent 12):** "State tax incentives worth $500M approved"
5. **International Desk (Agent 13):** "Shifts supply chain away from China"

**Editor-in-Chief (Agent 0) synthesizes:**
```
LEAD STORY: Tesla's $5B Texas Expansion

Business angle: Major capital investment, aggressive growth strategy
Tech angle: New battery tech could cut EV costs 20%
Local angle: Largest economic development project in Austin history
Policy angle: Texas won with $500M incentive package
Global angle: Reduces China supply chain dependence

Strategic implications:
- EV manufacturing shifting to U.S.
- Battery cost breakthroughs accelerating
- State competition for tech manufacturing intensifying
```

### Vertical Agent Architecture

**Each vertical editor agent has:**

1. **Custom Prompt:** Tailored to beat coverage and editorial voice
2. **Specialized Tools:** Access to vertical-specific data sources
3. **Unique Scoring Lens:** Criteria specific to that vertical
4. **Distinct Editorial Rules:** Voice, style, and presentation standards
5. **Beat-Specific Sources:** RSS feeds, APIs, and web sources

**Example: Business Desk Tools**
```python
# Standard MCP tools (all agents)
- fetch_rss_feed()
- score_article()
- analyze_article()
- store_article()

# Business-specific tools (Agent 10 only)
- fetch_sec_filing()         # Pull 8-K, 10-K filings
- get_earnings_calendar()    # Upcoming earnings dates
- check_insider_trading()    # SEC Form 4 filings
- get_analyst_ratings()      # Wall Street consensus
```

### How the Editor-in-Chief Coordinates

**Daily workflow (with vertical desks):**

```
1. Editor-in-Chief (Agent 0): "All desks, fetch your beat's stories"

2. Parallel execution:
   - Business Desk: Fetches 50 business articles
   - Tech Desk: Fetches 40 tech articles
   - Politics Desk: Fetches 30 politics articles
   - ...10+ desks running in parallel

3. Each desk scores and analyzes its own articles

4. Editor-in-Chief: "Cross-reference for overlaps"
   - Identifies stories covered by multiple desks
   - Flags for collaborative analysis

5. Editor-in-Chief: "Compile sections"
   - Business section (top 5 stories)
   - Tech section (top 5 stories)
   - Politics section (top 3 stories)
   - ...

6. Editor-in-Chief: "Create final edition"
   - Front page: Top 3 cross-desk stories
   - Section pages: Vertical-specific coverage
   - Breaking news: Rapid Response desk alerts

7. Daily Synthesizer (Agent 5): "Format for delivery"
   - Dashboard view (by section)
   - Slack notification (headlines only)
   - Email digest (full text)
```

### Expansion Roadmap (Phase by Phase)

**Phase 3: Add Core Vertical Desks (4 agents)**
- Agent 10: Business Desk
- Agent 11: Tech Desk
- Agent 12: Politics Desk
- Agent 13: International Desk

**Phase 4: Add Supplementary Desks (3 agents)**
- Agent 14: Local Desk
- Agent 15: Sports Desk
- Agent 16: Crime Desk

**Phase 5: Add Premium Desks (3 agents)**
- Agent 17: Financial Markets Desk
- Agent 18: Opinion/Analysis Desk
- Agent 19: Rapid Response Desk

**Phase 6: Custom Vertical Desks (Enterprise Only)**
- Agent 20+: Industry-specific desks
  - Healthcare Desk (pharma, biotech, FDA)
  - Legal Desk (court cases, regulatory actions)
  - Energy Desk (oil, gas, renewables, utilities)
  - Real Estate Desk (commercial, residential, REITs)

### Why This Newsroom Model Sells

**For Executives:**
```
Instead of:
"Here are 500 articles about everything"

You get:
"Business: 5 stories
 Tech: 5 stories
 Politics: 3 stories
 Markets: 2 stories"

Organized. Prioritized. Actionable.
```

**For Industry Verticals:**
```
Healthcare executive gets:
- General news intelligence (8 core agents)
- Healthcare-specific desk (Agent 20: Healthcare Desk)
  • FDA approvals and trials
  • Pharma M&A and partnerships
  • Insurance/reimbursement policy
  • Biotech breakthroughs
```

**For Multi-Tenant SaaS:**
```
Tier 1 (Solo): Core 8 agents only
Tier 2 (Team): Core 8 + 2 vertical desks of your choice
Tier 3 (Enterprise): Core 8 + unlimited vertical desks + custom desks
```

---

## Technical Flow Diagrams

### Today's System (8 Agents)

```
┌──────────────────────────────────────────────────────────┐
│                   DAILY WORKFLOW                         │
└──────────────────────────────────────────────────────────┘

7:30 AM CST - Cloud Scheduler triggers Pub/Sub
    ↓
┌────────────────────────────────────────┐
│ Agent 0: Editor-in-Chief (Orchestrator)│
│ "Let's get today's intelligence"       │
└────────────┬───────────────────────────┘
             │
             ├─→ Agent 2: Topic Manager
             │   "What are we tracking today?"
             │   Returns: 8 active topics
             │
             ├─→ Agent 1: Source Harvester
             │   "Fetch articles for these topics"
             │   Calls: NewsIngestionMCP (11 RSS feeds)
             │   Returns: 487 articles
             │
             ├─→ Agent 3: Relevance Guru
             │   "Score these 487 articles"
             │   Calls: RelevanceMCP
             │   Returns: Top 50 articles (score ≥ 7.0)
             │
             ├─→ Agent 4: Article Analyst
             │   "Analyze these 50 articles"
             │   Calls: LLMToolsMCP (summarize, tag, extract)
             │   Returns: 50 analyzed articles
             │
             ├─→ Agent 6: Quality Checker
             │   "Validate the output"
             │   Calls: ValidationMCP
             │   Returns: ✅ All valid
             │
             ├─→ Agent 5: Daily Synthesizer
             │   "Create the executive brief"
             │   Calls: StorageMCP (read articles)
             │   Calls: LLMToolsMCP (compose brief)
             │   Returns: Daily brief (Markdown)
             │
             └─→ Agent 7: Delivery Driver
                 "Send to Slack + Dashboard"
                 Calls: DeliveryMCP
                 Returns: ✅ Delivered

8:05 AM CST - Executive opens Slack
    ↓
📱 "Daily Intelligence Brief - November 14, 2025"
   47 articles analyzed | 8 topics tracked | 3 alerts
   5-minute read → Coffee → Ready to lead
```

### Future Newsroom (15-20 Agents)

```
┌──────────────────────────────────────────────────────────────────┐
│              THE AI NEWSROOM - DAILY EDITION WORKFLOW            │
└──────────────────────────────────────────────────────────────────┘

7:30 AM - Cloud Scheduler triggers Pub/Sub
    ↓
┌─────────────────────────────────────────┐
│ Agent 0: Editor-in-Chief                │
│ "All desks, gather your stories"        │
└────┬────────────────────────────────────┘
     │
     ├─────────────────┬─────────────────┬────────────────┐
     │                 │                 │                │
     ↓                 ↓                 ↓                ↓
┌──────────┐     ┌──────────┐     ┌──────────┐    ┌──────────┐
│Business  │     │Tech Desk │     │Politics  │    │Int'l     │
│Desk      │     │(Agent 11)│     │Desk      │    │Desk      │
│(Agent 10)│     │          │     │(Agent 12)│    │(Agent 13)│
└────┬─────┘     └────┬─────┘     └────┬─────┘    └────┬─────┘
     │                │                │               │
     │ Fetch 50       │ Fetch 40       │ Fetch 30      │ Fetch 25
     │ business       │ tech           │ politics      │ int'l
     │ articles       │ articles       │ articles      │ articles
     │                │                │               │
     └────────────────┴────────────────┴───────────────┘
                      │
     ┌────────────────┴────────────────┬────────────────┐
     │                                  │                │
     ↓                                  ↓                ↓
┌──────────┐     ┌──────────┐     ┌──────────┐    ┌──────────┐
│Local     │     │Sports    │     │Crime     │    │Finance   │
│Desk      │     │Desk      │     │Desk      │    │Markets   │
│(Agent 14)│     │(Agent 15)│     │(Agent 16)│    │(Agent 17)│
└────┬─────┘     └────┬─────┘     └────┬─────┘    └────┬─────┘
     │                │                │               │
     │ Fetch 20       │ Fetch 15       │ Fetch 10      │ Fetch 30
     │ local          │ sports         │ crime         │ markets
     │ articles       │ articles       │ articles      │ articles
     │                │                │               │
     └────────────────┴────────────────┴───────────────┘
                      │
     ┌────────────────┴────────────────┬
     │                                  │
     ↓                                  ↓
┌──────────┐     ┌──────────┐     ┌──────────┐
│Opinion   │     │Breaking  │     │[Custom]  │
│Desk      │     │News      │     │Desk      │
│(Agent 18)│     │(Agent 19)│     │(Agent 20)│
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     │ Fetch 10       │ Monitor        │ Fetch N
     │ opinion        │ real-time      │ custom
     │ articles       │ alerts         │ articles
     │                │                │
     └────────────────┴────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────┐
│ Agent 0: Editor-in-Chief                │
│ "Cross-reference and identify overlaps" │
└────┬────────────────────────────────────┘
     │
     │ Example overlap detected:
     │ "Tesla Factory" story found in:
     │   - Business Desk: Corporate investment angle
     │   - Tech Desk: Manufacturing tech angle
     │   - Local Desk: Jobs/economic impact angle
     │   - Politics Desk: Tax incentives angle
     │
     ↓
┌─────────────────────────────────────────┐
│ Agent 0: "Compile sections"             │
│                                         │
│ FRONT PAGE (Cross-Desk Stories):       │
│   1. Tesla's $5B Texas Expansion       │
│   2. Fed Raises Rates 0.5%             │
│   3. EU AI Act Enforcement Begins      │
│                                         │
│ BUSINESS SECTION:                       │
│   1. Microsoft AI Acquisition          │
│   2. Amazon CEO Transition             │
│   3. ...                                │
│                                         │
│ TECHNOLOGY SECTION:                     │
│   1. OpenAI GPT-5 Release              │
│   2. Google Gemini 3.0 Preview         │
│   3. ...                                │
│                                         │
│ [All other sections...]                 │
└────┬────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────┐
│ Agent 5: Daily Synthesizer              │
│ "Format final edition"                  │
│                                         │
│ Output formats:                         │
│  • Dashboard: Section-based navigation  │
│  • Slack: Headlines + section links     │
│  • Email: Full text with sections       │
└────┬────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────┐
│ Agent 7: Delivery Driver                │
│ "Publish to all channels"               │
│                                         │
│  ✅ Dashboard updated                   │
│  ✅ Slack notification sent             │
│  ✅ Email digest delivered              │
└─────────────────────────────────────────┘

8:15 AM - Executive opens dashboard
    ↓
📱 "Daily Edition - November 14, 2025"

   FRONT PAGE (3 stories)
   BUSINESS (5 stories)
   TECHNOLOGY (5 stories)
   POLITICS (3 stories)
   MARKETS (2 stories)
   [More sections...]

   Professional. Organized. Actionable.
```

---

## Feature Roadmap

### Phase 1: Foundations (CURRENT - Nov 2025)

**Status:** ✅ Complete

**Deliverables:**
- 8 core agents deployed to Vertex AI Agent Engine
- MCP service (perception-mcp) on Cloud Run
- Firestore schema for articles, topics, summaries
- Firebase Hosting dashboard (React + TypeScript)
- CSV-based source configuration (11 RSS feeds)
- Basic relevance scoring algorithm
- Daily workflow automation (7:30 AM CST)
- Slack integration for brief delivery

**Technical Milestones:**
- ✅ WIF authentication (keyless GitHub → GCP)
- ✅ Internal-only MCP ingress (backend security)
- ✅ Structured JSON logging
- ✅ Cloud Run auto-scaling
- ✅ A2A protocol for agent communication

**Cost:** ~$70/month (Cloud Run + Vertex AI + Firestore)

---

### Phase 2: Instrumentation + Production Hardening (Dec 2025 - Jan 2026)

**Status:** 🔄 In Progress

**Deliverables:**
- OpenTelemetry tracing (full request visibility)
- Custom dashboards (Grafana on Cloud Run)
- SLI/SLO definitions and tracking
- PagerDuty alerting integration
- Cost attribution (per-agent cost tracking)
- Performance baseline (latency p50/p95/p99)
- Firestore sources collection (migrate from CSV)
- Enhanced relevance scoring (user feedback loop)

**Technical Milestones:**
- ✅ Smoke tests (CI without GCP credentials)
- ✅ Deploy workflows (manual + automated)
- 🔄 OpenTelemetry instrumentation
- 🔄 SLI/SLO dashboards
- 🔄 Cost tracking per agent
- 🔄 Firestore migration from CSV

**Cost:** ~$100/month (+monitoring infrastructure)

---

### Phase 3: Multi-Section Newsroom Expansion (Feb - Apr 2026)

**Status:** 📋 Planned

**Deliverables:**
- 4 vertical editor agents (Business, Tech, Politics, Int'l)
- Cross-desk collaboration logic in Editor-in-Chief
- Section-based dashboard navigation
- Vertical-specific scoring criteria
- Beat-specific source configuration
- Multi-section brief formatting

**New Agents:**
- Agent 10: Business Desk Editor
- Agent 11: Technology Desk Editor
- Agent 12: Politics Desk Editor
- Agent 13: International Desk Editor

**Technical Milestones:**
- Vertical agent prompt templates
- Cross-desk story identification algorithm
- Section-based Firestore schema
- Enhanced dashboard UI (section navigation)
- Agent configuration management (YAML per desk)

**Cost:** ~$150/month (+4 additional agents)

---

### Phase 4: Multi-Tenant Media Intelligence Platform (May - Aug 2026)

**Status:** 📋 Planned

**Deliverables:**
- Multi-tenant architecture (tenant_id on all data)
- Firebase Authentication (user login, SSO)
- Tenant management dashboard (admin UI)
- Stripe billing integration
- API access (REST API for integrations)
- White-label dashboard option
- Usage analytics (per-tenant metrics)

**Pricing Tiers:**
- **Solo:** $49/month (1 user, 5 topics, core 8 agents)
- **Team:** $199/month (10 users, 20 topics, +2 vertical desks)
- **Enterprise:** $999/month (unlimited users/topics, custom desks)

**Technical Milestones:**
- Tenant isolation (Firestore security rules)
- User authentication (Firebase Auth)
- Billing system (Stripe subscriptions)
- API gateway (Cloud Endpoints)
- Usage tracking (BigQuery analytics)
- White-label branding (CSS themes)

**Cost:** ~$300/month (multi-tenant infrastructure)

---

### Phase 5: Vertical-Specific Editions (Sep - Dec 2026)

**Status:** 📋 Planned

**Deliverables:**
- Industry-specific agent desks (Healthcare, Legal, Energy, etc.)
- Vertical-specific data sources (e.g., FDA for healthcare)
- Custom scoring models per industry
- Compliance features (HIPAA, SOC 2, etc.)
- Industry benchmarking (compare to peers)
- Vertical-specific brief templates

**Example Verticals:**
- **Healthcare Edition:** FDA approvals, clinical trials, pharma M&A
- **Legal Edition:** Court cases, regulatory actions, legislation
- **Energy Edition:** Oil/gas markets, renewables, utilities
- **Real Estate Edition:** Commercial deals, REITs, development
- **Finance Edition:** Trading, investing, monetary policy

**Technical Milestones:**
- Vertical agent library (template-based creation)
- Industry-specific MCP tools (e.g., FDA API integration)
- Compliance logging (audit trails for regulated industries)
- Custom data source integrations
- Industry-specific analytics

**Cost:** Variable (based on vertical and data source costs)

---

### Phase 6: AI Newsroom Maturity (2027+)

**Status:** 🔮 Vision

**Deliverables:**
- 15-20 vertical desks (full newsroom coverage)
- Ensemble AI models (GPT + Claude + Gemini voting)
- Real-time breaking news alerts (<1 min from publish)
- Predictive intelligence (forecast trends before they happen)
- Natural language queries ("Show me all Tesla news this month")
- Voice interface (Alexa/Google Assistant integration)
- Video summarization (YouTube, earnings calls, etc.)
- Multi-language support (global newsroom)

**Advanced Features:**
- Agent self-improvement (fine-tuning on user feedback)
- Collaborative filtering (learn from all users)
- Topic auto-discovery (find what you didn't know to ask)
- Cross-vertical trend detection (e.g., AI impacting healthcare)
- Sentiment time-series (track opinion shifts)

**Cost:** $500-1000/month (mature platform with all features)

---

## Sales & Positioning Notes

### Why Executives Need Signal, Not Noise

**The Information Overload Problem:**

```
Modern executive's daily information flood:
- 200+ unread emails
- 50+ Slack messages
- 30+ LinkedIn notifications
- 20+ news alerts
- 10+ internal reports

Result: 2-3 hours/day just processing information
        Still miss critical developments
        Burnout, decision fatigue, missed opportunities
```

**The Perception Solution:**

```
Perception's daily intelligence delivery:
- 1 curated brief (5-minute read)
- Top 10 stories that actually matter
- Strategic implications highlighted
- Action items flagged

Result: 5 minutes → Full situational awareness
        No missed critical developments
        Confident, informed decision-making
```

**ROI Calculation:**
```
Executive's time: $200/hour
Hours saved per day: 2 hours
Value per day: $400
Value per month: $8,000 (20 working days)

Perception cost: $49-$999/month
ROI: 8x to 160x
```

### Why This Platform Becomes a Daily Intelligence Asset

**Traditional news tools are PULL (you have to remember to check):**
- Bloomberg Terminal: Log in, search, read
- Google News: Open app, scroll, filter
- Email newsletters: Dig through inbox, find, read

**Perception is PUSH (intelligence comes to you):**
- 8:00 AM: Slack notification arrives
- 8:05 AM: Read 5-minute brief
- 8:10 AM: Ready to lead

**Daily habit formation:**
```
Week 1: "Let me check Perception before my first meeting"
Week 2: "I need to read the brief before I start my day"
Week 4: "I can't make decisions without Perception"
Month 3: "How did I ever lead without this?"
```

**It becomes infrastructure:**
- Like email, Slack, calendar
- Essential, not optional
- High switching cost (users get dependent)
- Network effects (more users = better intelligence)

### How Vertical Editors Enable Industry-Specific Value

**Generic news aggregator:**
```
Healthcare executive sees:
- 500 random articles
- Mix of tech, politics, sports, etc.
- No healthcare-specific context
- Must manually filter for relevance

Value: Low (still doing the work themselves)
```

**Perception with Healthcare Desk:**
```
Healthcare executive sees:
- 10 healthcare stories (FDA, pharma, biotech)
- Healthcare Desk editorial voice
- Regulatory compliance flagged
- Competitive intelligence highlighted

Value: High (true industry-specific intelligence)
```

**Enterprise pricing justification:**
```
Solo tier ($49): Core 8 agents, generic intelligence
Team tier ($199): +2 vertical desks of your choice
Enterprise ($999): Unlimited vertical desks + custom desks

Healthcare company gets:
- Business Desk (M&A, earnings)
- Tech Desk (health tech, AI)
- Politics Desk (FDA, Congress)
- Healthcare Desk (pharma, biotech, trials)
- Legal Desk (compliance, litigation)

= 13 agents vs. 8 agents
= $999/month vs. $49/month
= 20x value, 20x price ✅
```

### Pricing Narratives (Flat Fee + Usage)

**Pricing Philosophy:**

1. **Flat fee for access** (like Netflix, not AWS)
   - Predictable monthly cost
   - No surprise bills
   - Budget-friendly for CFOs

2. **Usage gates** (fair use policy)
   - Solo: 5 topics, 1 user
   - Team: 20 topics, 10 users
   - Enterprise: Unlimited topics, unlimited users

3. **Vertical desks as upsells**
   - Core 8 agents: Base platform
   - +2 desks: Team tier
   - Unlimited desks: Enterprise tier

**Example Pricing Page:**

```
┌──────────────────────────────────────────────────┐
│              PERCEPTION PRICING                  │
└──────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    SOLO      │  │     TEAM     │  │  ENTERPRISE  │
│              │  │              │  │              │
│  $49/month   │  │  $199/month  │  │  $999/month  │
│              │  │              │  │              │
│ 1 user       │  │ 10 users     │  │ Unlimited    │
│ 5 topics     │  │ 20 topics    │  │ Unlimited    │
│ Core 8 agents│  │ Core + 2 desks│  │ All desks   │
│ Daily brief  │  │ Daily + alerts│  │ Custom desks │
│ Slack        │  │ Slack + email │  │ API access   │
│              │  │ Priority      │  │ White-label  │
│              │  │ support       │  │ Dedicated    │
│              │  │              │  │ success mgr  │
└──────────────┘  └──────────────┘  └──────────────┘
```

**Value Proposition by Tier:**

**Solo ($49/month):**
- "Replace Bloomberg Terminal ($2,000/month) for 1/40th the cost"
- "Save 10 hours/week on news monitoring"
- "Get executive-level intelligence, not raw feeds"

**Team ($199/month):**
- "Arm your entire leadership team with the same intelligence"
- "Industry-specific desks for your vertical"
- "Real-time alerts for breaking developments"

**Enterprise ($999/month):**
- "White-label intelligence platform for your organization"
- "Custom desks for your specific needs"
- "API access for workflow integration"
- "Dedicated success manager + custom training"

---

## Competitive Positioning

### vs. Bloomberg Terminal

| Feature | Bloomberg Terminal | Perception |
|---------|-------------------|------------|
| **Price** | $2,000/month/user | $49-999/month (10+ users) |
| **Coverage** | Financial markets | Business + Tech + Politics + More |
| **AI Intelligence** | Basic alerts | Multi-agent analysis |
| **Ease of Use** | Steep learning curve | 5-minute daily brief |
| **Mobile** | Limited | Full (dashboard + Slack) |

**Positioning:** "Executive intelligence for 1/40th the cost"

### vs. Meltwater / Cision

| Feature | Meltwater | Perception |
|---------|-----------|------------|
| **Price** | $1,500/month | $49-999/month |
| **Focus** | Media monitoring | Strategic intelligence |
| **AI** | Basic sentiment | Multi-agent analysis |
| **Noise** | High (thousands of mentions) | Low (top 10 stories) |
| **Actionable** | Manual analysis required | Strategic implications included |

**Positioning:** "Signal, not noise. Intelligence, not mentions."

### vs. Google News / Apple News

| Feature | Google News | Perception |
|---------|-------------|------------|
| **Price** | Free | $49-999/month |
| **Personalization** | Algorithm-driven | Agent-curated |
| **Quality** | Mixed (all sources) | Premium sources only |
| **Analysis** | None | AI-powered summaries + insights |
| **Executive Focus** | Consumer news | Business intelligence |

**Positioning:** "You get what you pay for. Free news is noise. Perception is signal."

---

## Technical FAQs (For Due Diligence)

### Q: Why Google Cloud (not AWS or Azure)?

**A:** Vertex AI Agent Engine is Google-only (no AWS/Azure equivalent)

**Alternatives:**
- AWS: Bedrock Agents (less mature)
- Azure: OpenAI Assistants (different architecture)

**Why we chose Vertex AI:**
1. Best-in-class multi-agent orchestration (A2A protocol)
2. Tight integration with Cloud Run (backend services)
3. Firestore Native Mode (real-time + ACID)
4. Gemini 2.0 Flash (state-of-the-art, cheap)
5. Enterprise-grade observability (Cloud Logging, Trace, Monitoring)

**Portability:** Agents are YAML configs (portable to other platforms)

### Q: What if Gemini 2.0 Flash gets expensive?

**A:** Agents are model-agnostic

**Current:** Gemini 2.0 Flash ($0.00025/1K tokens)

**Alternatives:**
- GPT-4o ($0.005/1K tokens) = 20x more expensive
- Claude 3.5 Sonnet ($0.003/1K tokens) = 12x more expensive
- Open-source (Llama 3, Mistral) = Free (but requires hosting)

**Migration:** Change model config in agent YAML, redeploy

### Q: How does this scale to 100,000 users?

**A:** Horizontally

**Bottlenecks identified:**
1. **Vertex AI Agent Engine:** Auto-scales infinitely (Google-managed)
2. **Cloud Run MCPs:** Auto-scales to 1000s of instances
3. **Firestore:** Auto-scales to millions of QPS (Google-managed)
4. **BigQuery:** Unlimited scale (Google-managed)

**Cost scaling:**
- 1 user: ~$70/month infrastructure
- 100 users: ~$200/month infrastructure (economies of scale)
- 10,000 users: ~$5,000/month infrastructure ($0.50/user)
- 100,000 users: ~$50,000/month infrastructure ($0.50/user)

**Pricing covers cost + margin at all scales**

### Q: What's the data retention policy?

**A:** Configurable per customer

**Default:**
- Firestore (working memory): 30 days
- BigQuery (long-term): Unlimited

**Compliance options:**
- GDPR: Auto-delete user data on request
- HIPAA: BAA available for healthcare customers
- SOC 2: Audit logs retained for 1 year

### Q: Can we deploy in our own GCP project?

**A:** Yes (Enterprise tier)

**Deployment options:**
1. **SaaS (default):** Hosted in Perception's GCP project
2. **Dedicated (Enterprise):** Deployed in customer's GCP project
3. **On-prem (rare):** Self-hosted with support contract

**Dedicated deployment benefits:**
- Full data control (stays in your GCP project)
- Custom compliance requirements
- VPC peering with your systems
- Dedicated resources (no noisy neighbors)

---

**Last Updated:** 2025-11-14
**Version:** 1.0
**Status:** Ready for investor/executive briefings
**Next Steps:** Use for fundraising, partnerships, enterprise sales
