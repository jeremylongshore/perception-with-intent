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

### Setup & Installation
```bash
# Navigate to project
cd /home/jeremy/000-projects/perception

# Install all dependencies
make install

# Or manually
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Setup GCP
make setup-gcp
# Or manually:
gcloud auth application-default login
gcloud config set project perception-with-intent
```

### Local Development
```bash
# Run agents locally (with in-memory everything)
make dev
# Or: ./scripts/dev_run_adk.sh
# Serves at http://localhost:8080

# Run agent directly with Python
python -m app.main --host 127.0.0.1 --port 8080

# Test specific agent configuration
cd app/perception_agent
python -c "from google.adk.agents import Agent; agent = Agent.from_config_file('agents/agent_0_root_orchestrator.yaml'); print(agent)"
```

### Testing & Quality
```bash
# Run all tests
make test
# Or: pytest tests/ -v --cov=app

# Run linting
make lint
# Or:
flake8 app/ --max-line-length=120
mypy app/
black --check app/

# Format code
make format
# Or: black app/

# Clean build artifacts
make clean
```

### Deploy to Production
```bash
# Just push to main, GitHub Actions does the rest
git add .
git commit -m "feat: ship it"
git push origin main

# Or deploy manually
make deploy
# Or: ./scripts/deploy_agent_engine.sh

# Required env vars for manual deploy:
export VERTEX_PROJECT_ID=perception-with-intent
export VERTEX_LOCATION=us-central1
export VERTEX_AGENT_ENGINE_ID=your-agent-engine-id

# Check GCP authentication
make check-auth
```

### Firebase Dashboard
```bash
cd dashboard

# Install dependencies
npm install

# Development
npm run dev          # Local dev server
npm run build        # Production build
npm run preview      # Test production build
npm run lint         # ESLint checking

# Deploy to Firebase
npm run build
firebase deploy --only hosting

# Dashboard available at:
# https://perception-with-intent.web.app
```

### Terraform Infrastructure
```bash
cd infra/terraform/envs/dev

# Initialize
terraform init

# Plan changes
terraform plan

# Apply infrastructure
terraform apply

# Destroy (careful!)
terraform destroy
```

## Code Architecture

### Project Structure
```
perception/
├── app/
│   ├── perception_agent/          # Main Perception agent system
│   │   ├── agents/                # Agent YAML configurations
│   │   │   ├── agent_0_root_orchestrator.yaml
│   │   │   ├── agent_1_topic_manager.yaml
│   │   │   ├── agent_2_news_aggregator.yaml
│   │   │   ├── agent_3_relevance_scorer.yaml
│   │   │   ├── agent_4_article_analyst.yaml
│   │   │   ├── agent_5_daily_synthesizer.yaml
│   │   │   ├── agent_6_validator.yaml
│   │   │   └── agent_7_storage_manager.yaml
│   │   ├── tools/                 # Tool implementations per agent
│   │   │   ├── orchestration_tools.py    # Agent 0
│   │   │   ├── topic_tools.py            # Agent 1
│   │   │   ├── aggregation_tools.py      # Agent 2
│   │   │   ├── scoring_tools.py          # Agent 3
│   │   │   ├── analysis_tools.py         # Agent 4
│   │   │   ├── synthesis_tools.py        # Agent 5
│   │   │   ├── validation_tools.py       # Agent 6
│   │   │   └── storage_tools.py          # Agent 7
│   │   └── config/
│   │       └── rss_sources.yaml   # RSS feed sources
│   ├── jvp_agent/                 # JVP Base implementation (A2A wrapper)
│   │   ├── agent.yaml             # JVP agent config
│   │   ├── agent.py               # Agent class
│   │   ├── a2a.py                 # A2A protocol wrapper
│   │   ├── config.py              # Configuration
│   │   ├── memory.py              # Context caching & compaction
│   │   ├── prompts/               # System prompts
│   │   └── tools/                 # Strategic orchestrator, RAG search
│   └── main.py                    # Dev entrypoint (uvicorn)
├── agent_engine_app.py            # Production entrypoint (Vertex AI)
├── dashboard/                     # React dashboard
│   ├── src/                       # React components
│   ├── package.json               # NPM dependencies
│   └── vite.config.ts             # Vite config
├── infra/terraform/               # Infrastructure as Code
│   ├── modules/                   # Reusable Terraform modules
│   └── envs/dev/                  # Development environment
├── scripts/                       # Deployment & utility scripts
│   ├── dev_run_adk.sh            # Local development
│   ├── deploy_agent_engine.sh    # Deploy to Vertex AI
│   ├── fmt_vet_lint.sh           # Code formatting
│   └── package_agent.py          # Agent packaging
├── .github/workflows/             # CI/CD pipelines
│   ├── ci.yml                    # Continuous integration
│   ├── deploy-agents.yml         # Agent deployment
│   └── deploy-agent-engine.yml   # Engine deployment
├── requirements.txt               # Python dependencies
└── Makefile                       # Development commands
```

### Agent System Architecture

**Deployment Model:** Monolithic (all agents in one deployment)

All 8 agents deploy as a single unit to Vertex AI Agent Engine but operate independently via A2A Protocol:

```python
# agent_engine_app.py - Production Entry Point
from google.adk.apps import App
from google.adk.agents import Agent

app = App()

# Root orchestrator loads all sub-agents automatically
root_agent = Agent.from_config_file(
    "app/perception_agent/agents/agent_0_root_orchestrator.yaml"
)
app.register_agent(root_agent)
```

**Key Files:**
- `agent_engine_app.py` - Production deployment (Vertex AI Agent Engine)
- `app/main.py` - Local development server (uvicorn)
- `app/jvp_agent/a2a.py` - A2A protocol wrapper for agent communication
- `app/jvp_agent/memory.py` - Context caching and compaction

### Agent Details

**Agent 0: Root Orchestrator** (`agent_0_root_orchestrator.yaml`)
- Role: Editor-in-Chief, coordinates entire workflow
- Tools: `orchestration_tools.py`
- Sub-agents: Manages all 7 specialized agents via A2A Protocol
- Config: `app/perception_agent/agents/agent_0_root_orchestrator.yaml:1`

**Agent 1: Topic Manager** (`agent_1_topic_manager.yaml`)
- Role: Manages tracked topics and keywords
- Tools: `topic_tools.py` - Firestore topic operations
- Data: Reads/writes `topics_to_monitor` collection

**Agent 2: News Aggregator** (`agent_2_news_aggregator.yaml`)
- Role: Fetches news from RSS feeds and APIs
- Tools: `aggregation_tools.py` - RSS fetching, web scraping
- Config: `app/perception_agent/config/rss_sources.yaml`

**Agent 3: Relevance Scorer** (`agent_3_relevance_scorer.yaml`)
- Role: Scores articles for importance
- Tools: `scoring_tools.py` - Relevance algorithms
- Output: Relevance scores (1-10)

**Agent 4: Article Analyst** (`agent_4_article_analyst.yaml`)
- Role: AI-powered article analysis
- Tools: `analysis_tools.py` - Gemini 2.0 Flash for summaries
- Output: Summaries, tags, strategic insights

**Agent 5: Daily Synthesizer** (`agent_5_daily_synthesizer.yaml`)
- Role: Creates executive briefs
- Tools: `synthesis_tools.py` - Daily summary generation
- Output: Executive-level daily briefs

**Agent 6: Validator** (`agent_6_validator.yaml`)
- Role: Data quality assurance
- Tools: `validation_tools.py` - Schema validation
- Ensures: Clean, consistent data

**Agent 7: Storage Manager** (`agent_7_storage_manager.yaml`)
- Role: Saves data to Firestore/BigQuery
- Tools: `storage_tools.py` - Database operations
- Collections: `articles`, `daily_summaries`, `run_metrics`

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

## Development Workflow

### Agent Development
```bash
# 1. Edit agent YAML configuration
vim app/perception_agent/agents/agent_4_article_analyst.yaml

# 2. Implement/modify agent tools
vim app/perception_agent/tools/analysis_tools.py

# 3. Test agent locally
make dev
# Or: python -m app.main

# 4. Run tests
pytest tests/agents/test_article_analyst.py -v

# 5. Format and lint
make format
make lint

# 6. Commit changes
git add .
git commit -m "feat(agent-4): improve article analysis"
git push origin main
```

### Adding a New Agent Tool
```python
# In app/perception_agent/tools/analysis_tools.py
from typing import Dict, Any

async def analyze_sentiment(article_text: str) -> Dict[str, Any]:
    """Analyze article sentiment using Gemini."""
    # Implementation here
    return {
        "sentiment": "positive",
        "score": 0.85,
        "confidence": 0.92
    }
```

### Environment Variables
```bash
# Local Development (not needed)
# - No GCP credentials required
# - In-memory operations

# Production Deployment (required)
VERTEX_PROJECT_ID=perception-with-intent
VERTEX_LOCATION=us-central1
VERTEX_AGENT_ENGINE_ID=your-agent-engine-id

# Optional (for distributed deployments)
AGENT_SPIFFE_ID=spiffe://perception/agent/[name]
FIRESTORE_DATABASE=(default)
```

## Troubleshooting

### "It's not working!"
```bash
# Check if agents are running
gcloud run services list --project=perception-with-intent

# Check agent logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50 --project=perception-with-intent

# View specific agent logs
gcloud logging read "resource.labels.service_name=perception-agents" --limit=100

# Test agent locally
curl http://localhost:8080/v1/card
```

### "Deployment failed!"
Check GitHub Actions. WIF probably needs setup:
```bash
# See WIF-SETUP-GUIDE.md for the full thing
gcloud iam workload-identity-pools list --location=global --project=perception-with-intent

# Verify service account
gcloud iam service-accounts list --project=perception-with-intent

# Check GitHub secrets are set
# - GCP_WORKLOAD_IDENTITY_PROVIDER
# - GCP_SERVICE_ACCOUNT_EMAIL
```

### "Local dev broken!"
```bash
# Make sure you're NOT setting prod env vars
unset VERTEX_PROJECT_ID
unset VERTEX_LOCATION
unset VERTEX_AGENT_ENGINE_ID

# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Just run local
make dev
# Or: ./scripts/dev_run_adk.sh
```

### "Tests failing!"
```bash
# Run with verbose output
pytest tests/ -vv

# Run specific test file
pytest tests/agents/test_orchestrator.py -v

# Run with coverage
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser

# Debug test
pytest tests/test_file.py -k test_function_name --pdb
```

### "Import errors!"
```bash
# Common issue: missing google-adk
pip install google-genai[adk]>=0.6.0

# Or reinstall all requirements
pip install -r requirements.txt

# Check installed packages
pip list | grep google
```

### Common Issues

| Issue | Solution |
|-------|----------|
| `ImportError: google-adk` | `pip install google-genai[adk]>=0.6.0` |
| Docker permission denied | `sudo systemctl start docker` |
| Firestore connection fails | Check `GOOGLE_APPLICATION_CREDENTIALS` |
| Agent 0 can't find sub-agents | Verify YAML paths in `agent_0_root_orchestrator.yaml` |
| Port 8080 already in use | Kill process: `lsof -ti:8080 \| xargs kill -9` |
| Terraform state locked | `terraform force-unlock <LOCK_ID>` |

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

## Key Dependencies

### Python Packages
```txt
google-genai[adk]>=0.6.0                     # Google ADK with AI platform
google-cloud-aiplatform[adk,agent_engines]  # Vertex AI integration
a2a-sdk>=0.3.4                               # Agent-to-Agent protocol
google-cloud-firestore>=2.18.0               # Firestore database
uvicorn[standard]>=0.30.0                    # ASGI server
feedparser>=6.0.11                           # RSS parsing
pydantic>=2.9.0                              # Data validation
pytest>=8.3.0                                # Testing
```

### Dashboard Tech Stack
```json
{
  "react": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "firebase": "^10.7.1",
  "chart.js": "^4.4.1",
  "vite": "^5.0.8",
  "typescript": "^5.2.2",
  "tailwindcss": "^3.3.6"
}
```

## CI/CD Pipeline

### GitHub Actions Workflows

**`.github/workflows/ci.yml`** - Continuous Integration
- Python formatting checks (black, flake8, mypy)
- Terraform init/fmt/validate
- Placeholder ADK validation

**`.github/workflows/deploy-agent-engine.yml`** - Agent Deployment
- Authenticates via Workload Identity Federation (WIF)
- Deploys to Vertex AI Agent Engine
- Required secrets:
  - `GCP_WORKLOAD_IDENTITY_PROVIDER`
  - `GCP_SERVICE_ACCOUNT_EMAIL`

### Manual Deployment
```bash
# Set required environment variables
export VERTEX_PROJECT_ID=perception-with-intent
export VERTEX_LOCATION=us-central1
export VERTEX_AGENT_ENGINE_ID=your-agent-engine-id

# Deploy using script
./scripts/deploy_agent_engine.sh

# Or use Makefile
make deploy
```

## Important Documentation

Project-specific docs (check these for details):
- **AGENTS-DEPLOYMENT.md** - Detailed agent architecture and deployment patterns
- **WIF-SETUP-GUIDE.md** - Workload Identity Federation setup
- **PRODUCT-ROADMAP.md** - Feature roadmap and timeline
- **STATUS.md** - Current project status and TODOs
- **000-docs/** - All technical documentation
- **000-usermanuals/** - User manuals and guides

## The Philosophy

This system combines:
- **JVP's flexibility** (develop locally, deploy anywhere)
- **Bob's Brain enforcement** (production is bulletproof)
- **MCP architecture** (clean separation of concerns)

**Key Principles:**
1. Firebase handles humans
2. Agents handle thinking
3. MCPs handle doing
4. Data lives in Firestore/BigQuery

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
**GCP Project:** `perception-with-intent`
**Dashboard:** https://perception-with-intent.web.app