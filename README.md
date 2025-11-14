<div align="center">

# 🔍 Perception

**Executive-Level News Intelligence Without the Fluff**

[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?style=for-the-badge&logo=google-cloud)](https://github.com/google/adk-python)
[![Vertex AI](https://img.shields.io/badge/Vertex%20AI-Agent%20Engine-4285F4?style=for-the-badge&logo=google-cloud)](https://cloud.google.com/vertex-ai/generative-ai/docs/agents)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache--2.0-green?style=for-the-badge)](LICENSE)

[Quick Start](#-quick-start) • [Architecture](#-architecture) • [Deploy](#-deployment) • [Cost](#-cost-reality)

---

**Stop manually checking 50 news sources.** Track what matters, see what's coming, and get strategic intelligence delivered to your dashboard.

![Demo](https://via.placeholder.com/800x400/1a1a1a/4285F4?text=Perception+Dashboard+Demo)

</div>

---

## 🎯 What Is This?

Perception is an **AI-powered news intelligence platform** that transforms information overload into actionable insights.

**The Problem:**
- Executives waste 2+ hours daily scanning news sources
- Important stories get buried in noise
- Pattern recognition happens too late
- No strategic synthesis, just raw feeds

**The Solution:**
Perception monitors everything, filters intelligently using AI, and delivers insights that actually matter—all automatically.

### What Makes It Different

|  | Traditional RSS Readers | AI Summarizers | **Perception** |
|---|---|---|---|
| Multi-source monitoring | ✅ | ✅ | ✅ |
| AI-powered filtering | ❌ | ✅ | ✅ |
| Strategic synthesis | ❌ | ❌ | ✅ |
| Executive dashboard | ❌ | ❌ | ✅ |
| Customizable topics | ❌ | ❌ | ✅ |
| Cost per month | Free | $20-50 | **~$60** |

---

## ⚡ Quick Start

### Prerequisites

```bash
# Required
- Python 3.11+
- Docker Desktop
- Google Cloud account
- Node.js 18+ (for dashboard)

# Get started in 5 minutes
```

### 1. Clone & Install

```bash
git clone https://github.com/[your-username]/perception.git
cd perception

# Install dependencies
make install

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up GCP

```bash
# Authenticate
gcloud auth application-default login
gcloud config set project perception-with-intent

# Deploy infrastructure (one-time setup)
cd infra/terraform/envs/dev
terraform init && terraform apply
```

### 3. Run Locally

```bash
# Start the agent system (in-memory mode, no cloud needed)
make dev

# Agents available at:
# http://localhost:8080/v1/card
```

### 4. Deploy to Production

```bash
# GitHub Actions handles everything
git push origin main

# Dashboard deploys to:
# https://perception-with-intent.web.app
```

**That's it.** Seriously.

---

## 🏗️ Architecture

Perception uses 8 specialized AI agents orchestrated via Google's A2A Protocol on Vertex AI Agent Engine.

```
┌─────────────────────────────────────────────────────────────────┐
│                  FIREBASE (Human Interface)                      │
│  • React Dashboard - Real-time intelligence feed                │
│  • API Gateway - Ad-hoc queries                                  │
│  • Authentication - Multi-tenant (Phase 2)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓ A2A Protocol
┌─────────────────────────────────────────────────────────────────┐
│              VERTEX AI AGENT ENGINE (The Brains)                 │
│                                                                   │
│  Agent 0: Root Orchestrator (The Boss)                           │
│    ├─→ Agent 1: Topic Manager → Firestore                        │
│    ├─→ Agent 2: News Aggregator → NewsIngestionMCP               │
│    ├─→ Agent 3: Relevance Scorer → RelevanceMCP                  │
│    ├─→ Agent 4: Article Analyst → LLMToolsMCP (Gemini)           │
│    ├─→ Agent 5: Daily Synthesizer → StorageMCP                   │
│    ├─→ Agent 6: Validator → ValidationMCP                        │
│    └─→ Agent 7: Storage Manager → Firestore                      │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓ MCP Protocol
┌─────────────────────────────────────────────────────────────────┐
│            CLOUD RUN MCPs (The Toolboxes)                        │
│                                                                   │
│  Each MCP is a dumb tool that does ONE thing well:              │
│  • NewsIngestionMCP - RSS/API fetching                           │
│  • RelevanceMCP - Article scoring                                │
│  • LLMToolsMCP - AI summaries & tags                             │
│  • StorageMCP - Firestore operations                             │
│  • ValidationMCP - Data quality                                  │
│  • DeliveryMCP - Slack/email notifications                       │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                   FIRESTORE (The Memory)                         │
│  • topics_to_monitor - What we track                             │
│  • articles - Analyzed intelligence                              │
│  • daily_summaries - Executive briefs                            │
└─────────────────────────────────────────────────────────────────┘
```

### The Daily Flow

Every morning at 7:30 AM CST:

```
Cloud Scheduler ───> Pub/Sub ───> Root Orchestrator
                                          │
                    ┌─────────────────────┴──────────────────────┐
                    │                                             │
                    ↓                                             ↓
            Topic Manager                                 News Aggregator
         (Fetch keywords)                              (Collect from 15 feeds)
                    │                                             │
                    └─────────────────────┬──────────────────────┘
                                          ↓
                                  Relevance Scorer
                                  (Score & rank)
                                          │
                                          ↓
                                  Article Analyst
                              (Gemini summaries + tags)
                                          │
                                          ↓
                                  Daily Synthesizer
                              (Executive brief)
                                          │
                                          ↓
                                  Storage Manager
                              (Save to Firestore)
                                          │
                                          ↓
                          Dashboard updates automatically
```

---

## 🚀 Deployment

### Phase 1: Public Showcase (Current)

What's shipping now:
- ✅ Public dashboard (no auth required)
- ✅ Example topics (AI, tech, business, sports)
- ✅ Live intelligence feed
- ✅ Company branding
- ✅ Daily executive briefs

**Timeline:** 3-4 days to launch

### Phase 2: SaaS Platform (Future)

Coming next:
- 🔄 User accounts (Firebase Auth)
- 🔄 Custom topics per client
- 🔄 Stripe billing
- 🔄 API access
- 🔄 White-label options

**Timeline:** 3-4 weeks after Phase 1

### Deploy Commands

```bash
# Local development (chill mode)
make dev
# Serves at http://localhost:8080

# Test specific agent
cd app/perception_agent
pytest tests/test_agent_1.py

# Deploy everything (production mode)
make deploy
# GitHub Actions does the rest

# Deploy just dashboard
cd dashboard
npm run build
firebase deploy --only hosting
```

---

## 💰 Cost Reality

**Monthly operational costs** (based on 100 articles/day):

| Component | Monthly Cost |
|-----------|--------------|
| Cloud Run MCPs | ~$15 (scale-to-zero) |
| Vertex AI Agents | ~$25 |
| Gemini 2.0 Flash | ~$20 (analysis only) |
| Firestore | ~$10 |
| Firebase Hosting | **Free** (Spark plan) |
| **Total** | **~$70/month** |

**That's less than your coffee budget** for executive-level intelligence.

### Cost Optimization

- MCPs scale to zero when idle
- Gemini 2.0 Flash is 60% cheaper than GPT-4
- Firebase Hosting free tier covers most traffic
- No Imagen/Lyria costs (text-only analysis)

---

## 🛠️ Development

### Progressive Hardening

We develop loose, deploy tight. Three levels of enforcement:

**Level 1: Local Dev** (Break things freely)
```bash
✓ In-memory everything
✓ No cloud dependencies
✓ Hot reload enabled
✗ No enforcement rules
```

**Level 2: Staging** (Test with caution)
```bash
✓ Real Firestore
✓ Drift warnings (don't block)
✓ Real MCPs
✗ No production data
```

**Level 3: Production** (Zero tolerance)
```bash
✓ Full Bob's Brain enforcement
✓ CI-only deploys
✓ Drift detection blocks everything
✓ SPIFFE IDs required
✓ Zero downtime updates
```

### Key Commands

```bash
# Development
make dev              # Run local ADK server
make test             # Run test suite
make lint             # Run linting

# Deployment
make setup-gcp        # Authenticate GCP
make deploy           # Deploy to production
make docker           # Build Docker image

# Utilities
make clean            # Clean build artifacts
make format           # Auto-format code
make check-auth       # Verify GCP auth
```

### Testing

```bash
# Run all tests
pytest

# Test specific agent
pytest tests/agents/test_article_analyst.py

# Test with coverage
pytest --cov=app --cov-report=html

# Test MCP endpoint
curl http://localhost:8081/mcp/tools/fetch_rss_feed
```

---

## 📊 Dashboard

Live at: **https://perception-with-intent.web.app**

### Features

- **Real-time feed** - Articles update as they're analyzed
- **Topic management** - Add/remove keywords on the fly
- **Daily briefs** - Executive summaries every morning
- **Source analytics** - Track which sources matter
- **Trend visualization** - Spot patterns over time
- **Search & filter** - Find exactly what you need

### Tech Stack

```
Frontend:  React 18 + TypeScript + Vite
Styling:   TailwindCSS
State:     Firebase SDK (real-time)
Charts:    Chart.js
Hosting:   Firebase Hosting
```

---

## 🔧 Configuration

### Topics You Track

Edit in Firestore or via dashboard:

```javascript
{
  "keywords": ["openai", "anthropic", "gemini"],
  "category": "ai",
  "active": true
}
```

### RSS Sources

Add to `app/perception_agent/config/rss_sources.yaml`:

```yaml
sources:
  - name: "TechCrunch"
    url: "https://techcrunch.com/feed/"
    category: "tech"
    active: true
```

### Environment Variables

For production (local dev doesn't need these):

```bash
VERTEX_PROJECT_ID=perception-with-intent
VERTEX_LOCATION=us-central1
FIRESTORE_DATABASE=(default)
AGENT_SPIFFE_ID=spiffe://perception/agent/[name]
```

---

## 🐛 Troubleshooting

### "It's broken!"

```bash
# Check agent logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Test MCP health
curl https://storage-mcp-[hash]-uc.a.run.app/health

# Verify Firestore
firebase firestore:indexes
```

### "Deploy failed!"

Check GitHub Actions. If WIF auth failed:

```bash
gcloud iam workload-identity-pools list --location=global
# See WIF-SETUP-GUIDE.md for full setup
```

### "Local dev not working!"

```bash
# Kill production env vars
unset VERTEX_PROJECT_ID
unset VERTEX_LOCATION

# Just run it
make dev
```

### Common Issues

| Issue | Solution |
|-------|----------|
| `ImportError: google-adk` | `pip install google-adk==1.17.0` |
| Docker permission denied | `sudo systemctl start docker` |
| Firestore connection fails | Check `GOOGLE_APPLICATION_CREDENTIALS` |
| Agent 0 can't find sub-agents | Deploy sub-agents before Agent 0 |

---

## 🎓 Philosophy

Perception isn't another half-assed news aggregator. It combines:

- **JVP's flexibility** — Develop anywhere, deploy anywhere
- **Bob's Brain enforcement** — Production that doesn't break
- **MCP architecture** — Clean separation, no spaghetti

### The Rules

**Firebase** = Humans interact here ONLY
**Agents** = Think and decide
**MCPs** = Do without thinking
**Data** = Lives in Firestore/BigQuery

Simple. Powerful. Ships.

---

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete system overview
- **[AGENTS-DEPLOYMENT.md](AGENTS-DEPLOYMENT.md)** - Agent architecture details
- **[000-docs/](000-docs/)** - All technical documentation
- **[Google ADK Docs](https://github.com/google/adk-python)** - Official ADK documentation
- **[Vertex AI Agents](https://cloud.google.com/vertex-ai/docs/agents)** - Agent Engine documentation

---

## 🤝 Contributing

PRs welcome if they:
- ✅ Make it faster
- ✅ Make it smarter
- ✅ Make it cleaner
- ❌ Don't break production

### Development Setup

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test: `make test`
4. Commit: `git commit -m "feat: add amazing feature"`
5. Push: `git push origin feature/amazing-feature`
6. Open PR with clear description

---

## 📊 Status

**Current:** Phase 1 - Public Showcase

- ✅ Infrastructure deployed
- ✅ WIF auth configured
- ✅ 8 agents implemented
- ✅ Agent orchestration via A2A
- ✅ Dashboard scaffolded
- 🔄 MCPs in development (1-2 days)
- 🔄 Final integration testing

**Next:** Launch, then Phase 2 (SaaS)

---

## 🏆 Credits

Built on:
- [Google ADK](https://github.com/google/adk-python) - Agent Development Kit
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agents) - Agent orchestration
- [Firebase](https://firebase.google.com) - Hosting & real-time database
- [JVP Base](https://github.com/jeremylongshore/intent-agent-model-jvp-base) - Flexible development framework
- [Bob's Brain](https://github.com/jeremylongshore/bobs-brain) - Production enforcement

---

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Perception — Because manually checking news is for interns.**

[Get Started](#-quick-start) • [Documentation](CLAUDE.md) • [Report Bug](https://github.com/[your-username]/perception/issues)

Made with ☕ and AI by [Jeremy Longshore](https://jeremylongshore.com)

</div>
