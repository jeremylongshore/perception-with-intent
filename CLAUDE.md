# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Perception?

**Perception** is a next-gen AI news intelligence platform that actually makes sense. We track news, analyze it with AI, and deliver insights that matter - no fluff, just strategic intelligence.

**Project:** `perception-with-intent` (GCP)
**Location:** `/home/jeremy/000-projects/perception/`
**Architecture:** Master Orchestrator + MCP Toolboxes + Progressive Hardening
**Philosophy:** Better than JVP + Bob's Brain combined

## The Big Picture

Think of it like this:
- **Firebase** = The friendly face (what humans see)
- **Vertex AI Agent Engine** = The brain (8 specialized agents)
- **Cloud Run MCPs** = The toolboxes (7 isolated services)
- **Firestore/BigQuery** = The memory (where everything lives)

```
Human World (Firebase Dashboard)
    ↓
Agent Brain (Vertex AI Engine - 8 Agents)
    ↓
Tool World (Cloud Run MCPs - 7 Services)
    ↓
Data World (Firestore + BigQuery)
```

Firebase is the ONLY way humans interact with the system. MCPs are the ONLY way agents interact with the outside world. Clean separation, no mess.

## Architecture That Actually Works

### The Master Plan

```
┌────────────────────────────────────────────────────────────────┐
│                    FIREBASE (Human Interface)                   │
│  • Dashboard (React SPA) - Where executives see the magic       │
│  • API Gateway (Cloud Functions) - Ad-hoc queries              │
│  • Authentication (Future Phase 2) - Multi-tenant SaaS         │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ↓ (Humans ask questions here)
┌────────────────────────────────────────────────────────────────┐
│           VERTEX AI AGENT ENGINE (The Brains)                  │
│                                                                  │
│  Agent 0: Editor-in-Chief (Boss Agent)                         │
│    ├─→ Agent 1: Source Collector → NewsIngestionMCP            │
│    ├─→ Agent 2: Topic Manager → TopicsMCP                      │
│    ├─→ Agent 3: Relevance Guru → RelevanceMCP                  │
│    ├─→ Agent 4: Article Analyst → LLMToolsMCP                  │
│    ├─→ Agent 5: Daily Synthesizer → StorageMCP                 │
│    ├─→ Agent 6: Quality Checker → ValidationMCP                │
│    └─→ Agent 7: Delivery Driver → DeliveryMCP                  │
│                                                                  │
│  These agents talk to each other via A2A Protocol              │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ↓ (Agents use tools here)
┌────────────────────────────────────────────────────────────────┐
│         CLOUD RUN MCPs (The Toolboxes)                         │
│                                                                  │
│  Each MCP is a dumb tool that does ONE thing well:            │
│                                                                  │
│  • NewsIngestionMCP - Fetches RSS/APIs/web content             │
│  • TopicsMCP - Manages what we're tracking                     │
│  • RelevanceMCP - Scores articles (is this important?)         │
│  • LLMToolsMCP - AI analysis (summaries, tags, insights)       │
│  • StorageMCP - Saves everything to Firestore/BigQuery         │
│  • ValidationMCP - Makes sure data isn't garbage               │
│  • DeliveryMCP - Sends to Slack/email/webhooks                 │
│                                                                  │
│  MCPs can't think, they just do. Perfect separation.           │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ↓ (Data lives here)
┌────────────────────────────────────────────────────────────────┐
│              DATA LAYER (The Memory)                           │
│                                                                  │
│  • topics_to_monitor - What we're tracking                     │
│  • articles - Everything we've analyzed                        │
│  • daily_summaries - Executive briefs                          │
│  • run_metrics - How well we're doing                          │
└────────────────────────────────────────────────────────────────┘
```

### Daily Workflow (7:30 AM CST)

```
Cloud Scheduler: "Wake up!"
    ↓
Pub/Sub: "Hey Editor-in-Chief, time to work"
    ↓
Editor-in-Chief: "Alright team, let's go!"
    ↓
1. "Hey TopicsMCP, what are we tracking today?"
2. "NewsIngestionMCP, go fetch everything (parallel)"
3. "RelevanceMCP, score these articles"
4. "LLMToolsMCP, analyze the top ones"
5. "ValidationMCP, make sure it's not garbage"
6. "StorageMCP, save everything"
7. "DeliveryMCP, send the brief to Slack"
    ↓
Executive Dashboard: "New intelligence available!"
```

## Progressive Hardening (Smart Development)

We're not idiots - we develop locally first, then harden for production.

### Level 1: Local Dev (Chill Mode)
- In-memory everything (no GCP needed)
- Manual deployments (just run scripts)
- No enforcement (break things, learn)
- Mock data for MCPs
- `./scripts/dev_run_adk.sh` and you're good

### Level 2: Staging (Warning Mode)
- Real Firestore, test BigQuery
- Drift checks warn but don't block
- Some env vars required
- MCPs use staging secrets
- "Hey, this might be a problem..."

### Level 3: Production (Lockdown Mode)
- Full Bob's Brain rules (R1-R10)
- CI-only deployments (GitHub Actions + WIF)
- Drift detection blocks everything
- SPIFFE IDs everywhere
- MCPs have minimal permissions
- "This shit better work or we're not deploying"

## Tech Stack

### Must Have
- ✅ Google ADK (agents)
- ✅ Vertex AI Agent Engine (orchestration)
- ✅ A2A Protocol (agent communication)
- ✅ Cloud Run (MCP hosting)
- ✅ Firebase (dashboard + API)
- ✅ Firestore (main database)
- ✅ BigQuery (analytics)
- ✅ Gemini 2.0 Flash (AI model)
- ✅ Terraform (infrastructure)
- ✅ WIF (GitHub → GCP auth)

### Never Touch
- ❌ N8N (we're better than that)
- ❌ LangChain (ADK does it better)
- ❌ CrewAI (why would we?)
- ❌ Airtable (Firestore FTW)
- ❌ BrightStream (that old BS is gone)

## Quick Commands

### Get Started
```bash
cd /home/jeremy/000-projects/perception
source .venv/bin/activate
gcloud config set project perception-with-intent
```

### Local Development
```bash
# Run agents locally (with in-memory everything)
./scripts/dev_run_adk.sh

# Test an MCP locally
cd service/mcps/storage_mcp
uvicorn main:app --reload --port 8081

# Docker all the things
docker-compose up -d
docker-compose logs -f
```

### Deploy to Production
```bash
# Just push to main, GitHub Actions does the rest
git add .
git commit -m "feat: ship it"
git push origin main

# Watch the magic
# https://github.com/[your-repo]/actions
```

### Firebase Dashboard
```bash
cd dashboard
npm install
npm run dev  # Local dev

# Deploy
npm run build
firebase deploy --only hosting
```

## Agent Details

### Agent 0: Editor-in-Chief
The boss. Coordinates everything, makes sure the daily workflow runs smooth.

### Agent 1: Source Collector
Fetches news from RSS, APIs, wherever. Uses NewsIngestionMCP as its toolbox.

### Agent 3: Relevance Guru
Scores articles - "Is this worth our time?" Uses RelevanceMCP for the heavy lifting.

### Agent 4: Article Analyst
The smart one. Uses LLMToolsMCP to generate summaries and extract insights.

### Agent 5: Daily Synthesizer
Creates the executive brief. "Here's what actually matters from today."

### Agent 7: Delivery Driver
Gets the intel to humans via DeliveryMCP (Slack, email, whatever).

## MCP Services (The Toolboxes)

Each MCP is a simple Cloud Run service that does ONE thing:

### NewsIngestionMCP
```python
@app.post("/mcp/tools/fetch_rss_feed")
async def fetch_rss(feed_id: str):
    # Just fetch the damn RSS feed
    return {"articles": [...]}
```

### StorageMCP
```python
@app.post("/mcp/tools/save_article")
async def save_article(article: Article):
    # Save to Firestore, no thinking required
    db.collection("articles").add(article.dict())
    return {"status": "saved"}
```

That's it. MCPs are dumb tools. Agents are smart. Firebase is for humans.

## The Data

### What We Track (`topics_to_monitor`)
```javascript
{
  "keywords": ["alex morgan", "uswnt"],
  "category": "sports",
  "active": true
}
```

### What We Find (`articles`)
```javascript
{
  "title": "Breaking: Alex Morgan Retires",
  "summary": "AI-generated 3-sentence summary",
  "source": "ESPN",
  "ai_tags": ["retirement", "soccer", "uswnt"],
  "relevance_score": 9.5
}
```

### What Executives See (`daily_summaries`)
```javascript
{
  "date": "2025-11-13",
  "article_count": 47,
  "highlights": [
    "Major development in women's soccer...",
    "Strategic implications for NWSL..."
  ]
}
```

## Cost Reality

**Monthly burn rate:**
- Cloud Run MCPs: ~$15 (scale to zero FTW)
- Vertex AI Agents: ~$25
- Gemini 2.0 Flash: ~$20
- Firestore: ~$10
- Firebase Hosting: $0 (Spark plan)
- **Total: ~$70/month**

Not bad for executive-level intelligence, right?

## Production Rules (Bob's Brain Style)

When we go to production, these rules are LAW:

- **R2:** Vertex AI Agent Engine only (no alternatives)
- **R3:** MCPs can't import agent code (dumb tools stay dumb)
- **R4:** CI-only deployments (GitHub Actions + WIF)
- **R6:** One docs folder (`000-docs/`)
- **R7:** SPIFFE IDs everywhere (know who's doing what)
- **R8:** Drift detection runs first (blocks everything if violated)
- **R9:** Each MCP gets minimal IAM (principle of least privilege)
- **R10:** Secrets in Secret Manager (never hardcode)

## Troubleshooting

### "It's not working!"
```bash
# Check if agents are running
gcloud run services list --project=perception-with-intent

# Check logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Test an MCP directly
curl https://storage-mcp-[hash]-uc.a.run.app/health
```

### "Deployment failed!"
Check GitHub Actions. WIF probably needs setup:
```bash
# See WIF-SETUP-GUIDE.md for the full thing
gcloud iam workload-identity-pools list --location=global
```

### "Local dev broken!"
```bash
# Make sure you're NOT setting prod env vars
unset VERTEX_PROJECT_ID
unset VERTEX_LOCATION

# Just run local
./scripts/dev_run_adk.sh
```

## Current Status

**Phase 1: Public Showcase** (where we are)
- ✅ Infrastructure ready (Terraform provisioned)
- ✅ WIF configured (keyless auth from GitHub)
- ✅ Dashboard scaffolded
- 🔄 Agents being implemented (3-4 days)
- 🔄 MCPs being built

**Phase 2: SaaS Platform** (future)
- Multi-tenant with Firebase Auth
- Stripe billing
- Custom topics per client
- White-label options

## The Philosophy

This system combines:
- **JVP's flexibility** (develop locally, deploy anywhere)
- **Bob's Brain enforcement** (production is bulletproof)
- **MCP architecture** (clean separation of concerns)

Firebase handles humans. Agents handle thinking. MCPs handle doing.

Simple. Clean. Works.

## External Resources

- **Google ADK:** https://github.com/google/adk-python
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/docs/agents
- **A2A Protocol:** https://cloud.google.com/vertex-ai/docs/agents/a2a
- **Firebase:** https://firebase.google.com/docs
- **JVP Base:** https://github.com/jeremylongshore/intent-agent-model-jvp-base
- **Bob's Brain:** https://github.com/jeremylongshore/bobs-brain

---

**Status:** Getting this online ASAP
**Next:** Deploy agents, test MCPs, ship dashboard
**Timeline:** 3-4 days to Phase 1 launch