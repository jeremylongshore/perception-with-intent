# Perception With Intent - Context Handoff Document

**Document ID:** 6767-PM-REPO-context-handoff
**Version:** 1.0
**Date:** 2025-11-15
**Category:** Project Management
**Type:** Repository Context Handoff

---

## Executive Summary

This document provides comprehensive context for continuing work on the Perception With Intent platform. It captures the current state of the project at v0.3.0, recent architectural decisions, key technical patterns, and next steps for development.

**Current State:**
- MCP service deployed to Cloud Run
- 8-agent system complete and ready for deployment
- E2E ingestion pipeline built and documented
- Cloud-only deployment philosophy established

**Immediate Next Steps:**
1. Deploy Agent Engine to Vertex AI (scripts ready)
2. Run E2E ingestion test
3. Wire dashboard to Firestore data
4. Begin v0.4.0 (Dashboard Integration)

---

## Project Overview

### What Is Perception?

Perception is a production-grade AI news intelligence platform built on Google Cloud Platform. It demonstrates enterprise-level multi-agent system architecture using:

- **8 specialized AI agents** coordinated via A2A Protocol
- **Cloud Run MCP service** for agent tool execution
- **Vertex AI Agent Engine** for managed orchestration
- **Firebase + Firestore** for dashboard and data storage

**GCP Project:** `perception-with-intent`
**Current Version:** v0.3.0 (2025-11-15)
**Dashboard:** https://perception-with-intent.web.app
**MCP Service:** https://perception-mcp-348724539390.us-central1.run.app

---

## Recent Major Changes (v0.3.0)

### 1. Cloud-Only MCP Deployment

**Critical Architectural Decision:** All MCP testing and deployment happens in the cloud. NO localhost MCP servers.

**Rationale:**
- Local MCP servers create confusion and architectural drift
- Testing in cloud ensures production parity
- Simplifies development workflow

**Deployment Flow:**
```
Push to GitHub → CI/CD → Deploy to STAGING Cloud Run → Test in Cloud → Promote to PRODUCTION
```

**Key Files:**
- `app/mcp_service/Dockerfile` - Container definition for Cloud Run
- `app/mcp_service/main.py` - FastAPI MCP service
- `scripts/deploy_agent_engine.sh` - Agent Engine deployment (updated)

### 2. MCP Service Successfully Deployed

**Service URL:** `https://perception-mcp-348724539390.us-central1.run.app`

**Validated:**
- ✅ Health endpoint returns JSON: `{"status": "healthy", "service": "mcp-service"}`
- ✅ fetch_rss_feed returns 5+ real articles from Hacker News (270ms latency)
- ✅ Cloud Logging shows structured JSON logs with request details
- ✅ Zero ERROR-level logs

**Tools Status:**
- `fetch_rss_feed` - Real implementation (production-ready)
- `fetch_api_feed`, `fetch_webpage`, `store_articles`, `generate_brief`, `log_ingestion_run`, `send_notification` - Stubs

**IAM Permissions Fixed:**
Cloud Build service account granted:
- `roles/storage.objectViewer`
- `roles/logging.logWriter`
- `roles/artifactregistry.writer`

### 3. Agent Engine Deployment Infrastructure

**Entrypoint:** `agent_engine_app.py` (project root)

**Key Changes:**
- Fixed deployment script to use correct entrypoint (was pointing to old JVP agent config)
- Removed `VERTEX_AGENT_ENGINE_ID` requirement (ADK creates it automatically)
- Added telemetry flags (`--trace_to_cloud`)
- Created comprehensive deployment guide

**Agents Deployed as Single Unit:**
- Agent 0: Root Orchestrator
- Agent 1: Source Harvester
- Agent 2: Topic Manager
- Agent 3: Relevance & Ranking
- Agent 4: Brief Writer
- Agent 5: Alert & Anomaly Detector (stub)
- Agent 6: Validator
- Agent 7: Storage Manager
- Agent 8: Technology Desk Editor

**Communication:** A2A Protocol (not direct Python calls)

### 4. Observability Stack

**Cloud Logging:**
- MCP service logs structured JSON with timestamp, severity, operation, metrics
- Agent Engine logs show agent-to-agent communication traces
- Zero ERROR-level logs indicate clean service

**Monitoring:**
- Cloud Run metrics: request count, latency (50th, 95th, 99th percentile), CPU/memory utilization
- Firestore batch write performance tracking
- E2E ingestion run success rate (pending first run)

**Documentation:** `6767-AT-ARCH-observability-and-monitoring.md`

### 5. Documentation Structure Established

**6767- Prefix (Foundational/Evergreen):**
- `6767-AT-ARCH-*` = Architecture documents
- `6767-OD-GUID-*` = Operational guides
- `6767-PP-PLAN-*` = Planning documents
- `6767-PM-REPO-*` = Project management/reports

**Numeric Prefix (AARs/Phase Reports):**
- `041-AA-REPT-phase-E2E-agent-engine-deployment.md` - First AAR
- Future: `042-AA-REPT-*`, `043-AA-REPT-*`, etc.

**All documentation in `000-docs/`** following strict naming conventions.

---

## Current Architecture

### System Components

```
┌────────────────────────────────────────────────────────────────┐
│                    FIREBASE (Human Interface)                   │
│  • Dashboard (React SPA) - executives view intelligence         │
│  • API Gateway (Cloud Functions) - ad-hoc queries              │
│  • Authentication (Firebase Auth) - email/password enabled     │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ↓ (Humans ask questions)
┌────────────────────────────────────────────────────────────────┐
│           VERTEX AI AGENT ENGINE (The Brains)                  │
│                                                                  │
│  Agent 0: Root Orchestrator (Editor-in-Chief)                  │
│    ├─→ Agent 1: Source Harvester → MCP                         │
│    ├─→ Agent 2: Topic Manager → Firestore                      │
│    ├─→ Agent 3: Relevance & Ranking → MCP                      │
│    ├─→ Agent 4: Brief Writer → MCP + Gemini                    │
│    ├─→ Agent 5: Alert & Anomaly Detector → MCP (stub)          │
│    ├─→ Agent 6: Validator → MCP                                │
│    ├─→ Agent 7: Storage Manager → Firestore                    │
│    └─→ Agent 8: Technology Desk Editor → MCP                   │
│                                                                  │
│  Communication: A2A Protocol (managed by Agent Engine)         │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ↓ (Agents use tools)
┌────────────────────────────────────────────────────────────────┐
│         CLOUD RUN MCP SERVICE (The Toolbox)                    │
│                                                                  │
│  URL: https://perception-mcp-348724539390.us-central1.run.app  │
│                                                                  │
│  Tools (FastAPI endpoints):                                    │
│  • /mcp/tools/fetch_rss_feed ✅ (real implementation)          │
│  • /mcp/tools/fetch_api_feed (stub)                            │
│  • /mcp/tools/fetch_webpage (stub)                             │
│  • /mcp/tools/store_articles (stub)                            │
│  • /mcp/tools/generate_brief (stub)                            │
│  • /mcp/tools/log_ingestion_run (stub)                         │
│  • /mcp/tools/send_notification (stub)                         │
│                                                                  │
│  MCPs are dumb tools. Agents are smart.                       │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ↓
┌────────────────────────────────────────────────────────────────┐
│              FIRESTORE + BIGQUERY (The Memory)                 │
│                                                                  │
│  Firestore Collections:                                        │
│  • topics_to_monitor - What we track                           │
│  • articles - Analyzed intelligence                            │
│  • daily_summaries - Executive briefs                          │
│  • ingestion_runs - Pipeline run records                       │
│                                                                  │
│  BigQuery (Future):                                            │
│  • Analytics datasets                                          │
│  • Historical trend analysis                                   │
└────────────────────────────────────────────────────────────────┘
```

### Data Flow (E2E Ingestion)

**Trigger:** Cloud Scheduler (daily at 7:30 AM CST) → Pub/Sub → Agent 0

**Workflow:**
1. **Agent 0** (Root Orchestrator) receives trigger
2. **Agent 2** (Topic Manager) fetches topics from Firestore
3. **Agent 1** (Source Harvester) calls MCP to fetch RSS feeds (parallel)
4. **Agent 3** (Relevance & Ranking) scores articles (keyword matching)
5. **Agent 4** (Brief Writer) generates executive brief with Gemini
6. **Agent 6** (Validator) validates article and brief schemas
7. **Agent 7** (Storage Manager) writes to Firestore in batches (500 docs)
8. **Agent 8** (Technology Desk Editor) curates Tech section (if applicable)

**Output:**
- `articles` collection populated with scored, analyzed articles
- `daily_summaries` collection updated with executive brief
- `ingestion_runs` collection tracks run success/failure

---

## Key Technical Patterns

### 1. Lazy Initialization

**Pattern:** Firestore client initialized on first use, not at import time.

**Rationale:** Prevents import-time failures in environments without GCP credentials.

**Example:**
```python
_firestore_client = None

def get_firestore_client():
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = firestore.Client()
    return _firestore_client
```

### 2. Batch Operations

**Pattern:** Firestore writes in 500-document batches for efficiency.

**Rationale:** Reduces API calls and improves write performance.

**Example:**
```python
batch = db.batch()
for i, article in enumerate(articles):
    if i > 0 and i % 500 == 0:
        batch.commit()
        batch = db.batch()
    batch.set(doc_ref, article)
batch.commit()
```

### 3. URL-Based Deduplication

**Pattern:** Hash article URLs to prevent duplicate storage.

**Rationale:** Same article may appear in multiple feeds.

**Example:**
```python
article_id = f"art-{hashlib.md5(url.encode()).hexdigest()[:12]}"
```

### 4. Structured JSON Logging

**Pattern:** All logs use structured JSON with timestamp, severity, operation, metrics.

**Rationale:** Enables Cloud Logging queries and observability.

**Example:**
```python
logger.info({
    "timestamp": datetime.utcnow().isoformat(),
    "severity": "INFO",
    "operation": "fetch_rss_feed",
    "metrics": {"latency_ms": 270, "article_count": 5}
})
```

### 5. Shared Working Memory

**Pattern:** Agents pass accumulated state through pipeline via A2A Protocol.

**Rationale:** Avoids repeated database queries and enables stateful workflows.

**Example:**
```json
{
  "topics": [...],
  "articles": [...],
  "scored_articles": [...],
  "brief": {...}
}
```

---

## Critical User Feedback (Session Context)

### Feedback 1: NO Localhost MCP Servers

**User Message:** "we dont need any dev local mcps do we have an dev local aj agents? all the testing should be conducted live in the cloud"

**Impact:** Completely changed deployment philosophy - NO localhost MCP support.

**Actions Taken:**
- Created cloud-only documentation
- Removed localhost defaults from all docs
- Emphasized Cloud Run as ONLY valid MCP runtime

### Feedback 2: Run Commands Myself

**User Message:** "why would i do that u van run gcloud commands... rene it chochop"

**Impact:** Stop asking user to run commands I can execute myself.

**Actions Taken:**
- Execute gcloud commands directly
- Provide proof in responses (logs, output, verification)

### Feedback 3: Port Confusion

**User Feedback:** Multiple questions about port 8080 vs 8081

**Impact:** Standardize MCP port to 8080 across all docs.

**Actions Taken:**
- Global sed replacements in 5+ documentation files
- Fixed background MCP process running on wrong port
- Documented that port 8080 is for local agent development, NOT MCP

---

## Known Issues & Blockers

### 1. Agent Engine Not Yet Deployed

**Issue:** Deployment script updated but not executed.

**Impact:** Cannot run E2E ingestion until Agent Engine is deployed.

**Workaround:** None - manual deployment required.

**Resolution:**
```bash
export VERTEX_PROJECT_ID=perception-with-intent
export VERTEX_LOCATION=us-central1
./scripts/deploy_agent_engine.sh
```

**Priority:** High

### 2. VERTEX_AGENT_ID Unknown

**Issue:** E2E trigger script requires VERTEX_AGENT_ID but we don't have it yet.

**Impact:** Cannot run trigger script until after first deployment.

**Workaround:**
```bash
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1
```

**Resolution:** Document Agent ID retrieval in deployment guide (already done).

**Priority:** Medium (already documented)

### 3. MCP_BASE_URL Not Set in Agent Runtime

**Issue:** Agent tools reference MCP_BASE_URL env var but it's not configured in Agent Engine deployment.

**Impact:** Agents won't be able to call MCP service.

**Workaround:** Need to add env var to Agent Engine deployment.

**Resolution:** Research how to pass env vars to Agent Engine app.

**Priority:** High

**Action Item:** Investigate ADK documentation for environment variable configuration.

---

## Immediate Next Steps

### 1. Deploy Agent Engine to Staging

**Command:**
```bash
export VERTEX_PROJECT_ID=perception-with-intent
export VERTEX_LOCATION=us-central1
./scripts/deploy_agent_engine.sh
```

**Expected Outcome:**
- ADK deploys `agent_engine_app.py` to Vertex AI
- Agent Engine appears in `gcloud alpha aiplatform agents list`
- Cloud Logging shows "Perception Agent Engine starting..."

### 2. Get Agent ID

**Command:**
```bash
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1
```

**Copy AGENT_ID for next step.**

### 3. Configure MCP_BASE_URL

**Research Needed:** How to pass env vars to Agent Engine app.

**Target Value:** `MCP_BASE_URL=https://perception-mcp-348724539390.us-central1.run.app`

### 4. Run E2E Ingestion

**Command:**
```bash
export VERTEX_AGENT_ID=<from-step-2>
./scripts/run_ingestion_via_agent_engine.sh
```

**Expected Outcome:**
- Firestore `/ingestion_runs` collection updated
- Firestore `/articles` collection populated
- Firestore `/briefs` collection updated
- Cloud Logging shows full trace

### 5. Verify Data Landed

**Commands:**
```bash
# Check ingestion runs
gcloud firestore documents list \
  --collection=ingestion_runs \
  --limit=1 \
  --project=perception-with-intent

# Check articles
gcloud firestore documents list \
  --collection=articles \
  --limit=10 \
  --project=perception-with-intent

# Check briefs
gcloud firestore documents list \
  --collection=briefs \
  --limit=1 \
  --project=perception-with-intent

# View Cloud Logging for full trace
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/Agent"' \
  --project=perception-with-intent \
  --limit=50
```

---

## Future Phases

### v0.4.0 - Dashboard Integration

**Objectives:**
- Wire dashboard to read from Firestore collections
- Display briefs on homepage
- Show article lists per section
- Live ingestion status tracking

**Timeline:** 1-2 weeks after v0.3.0 complete

### v0.5.0 - Section Editors Rollout

**Objectives:**
- Agent 9: Business Desk Editor
- Agent 10: Politics Desk Editor
- Agent 11: Sports Desk Editor
- Section-specific curation logic

**Timeline:** 2-3 weeks after v0.4.0

### v1.0.0 - Production Launch

**Objectives:**
- Multi-tenant support (Firebase Auth)
- Per-user topic customization
- Production ingress controls (`internal-and-cloud-load-balancing`)
- Performance optimization
- Cost monitoring and alerts
- Public beta release

**Timeline:** 6-8 weeks after v0.5.0

---

## Key Files & Locations

### Entry Points
- `agent_engine_app.py` - Production entry point (Vertex AI Agent Engine)
- `app/main.py` - Local development entry point (uvicorn)

### Agent Configurations
- `app/perception_agent/agents/agent_0_root_orchestrator.yaml` - Root orchestrator
- `app/perception_agent/agents/agent_1_source_harvester.yaml` - Source harvester
- `app/perception_agent/agents/agent_2_topic_manager.yaml` - Topic manager
- `app/perception_agent/agents/agent_3_relevance_ranking.yaml` - Relevance scorer
- `app/perception_agent/agents/agent_4_brief_writer.yaml` - Brief writer
- `app/perception_agent/agents/agent_5_alert_anomaly.yaml` - Alert detector
- `app/perception_agent/agents/agent_6_validator.yaml` - Validator
- `app/perception_agent/agents/agent_7_storage_manager.yaml` - Storage manager
- `app/perception_agent/agents/agent_8_tech_editor.yaml` - Technology editor

### Agent Tools
- `app/perception_agent/tools/agent_0_tools.py` - Orchestration tools
- `app/perception_agent/tools/agent_1_tools.py` - Source harvesting tools
- `app/perception_agent/tools/agent_2_tools.py` - Topic management tools
- `app/perception_agent/tools/agent_3_tools.py` - Relevance scoring tools
- `app/perception_agent/tools/agent_4_tools.py` - Brief writing tools
- `app/perception_agent/tools/agent_5_tools.py` - Alert detection tools (stub)
- `app/perception_agent/tools/agent_6_tools.py` - Validation tools
- `app/perception_agent/tools/agent_7_tools.py` - Storage tools
- `app/perception_agent/tools/agent_8_tools.py` - Technology editor tools

### MCP Service
- `app/mcp_service/main.py` - FastAPI MCP service
- `app/mcp_service/Dockerfile` - Container definition
- `app/mcp_service/requirements.txt` - Python dependencies

### Deployment Scripts
- `scripts/deploy_agent_engine.sh` - Deploy to Vertex AI Agent Engine
- `scripts/run_ingestion_via_agent_engine.sh` - Trigger E2E ingestion

### Documentation
- `CLAUDE.md` - Complete system overview & current architecture
- `CHANGELOG.md` - Version history (v0.3.0, v0.2.0, v0.1.0)
- `README.md` - Project README with deployment info
- `000-docs/6767-AT-ARCH-observability-and-monitoring.md` - Monitoring stack
- `000-docs/6767-OD-GUID-agent-engine-deploy.md` - Agent Engine deployment
- `000-docs/6767-PP-PLAN-release-log.md` - Release tracking
- `000-docs/041-AA-REPT-phase-E2E-agent-engine-deployment.md` - Latest AAR
- `000-docs/6767-PM-REPO-context-handoff.md` - This document

### Dashboard
- `dashboard/src/App.tsx` - Main React app
- `dashboard/src/pages/Login.tsx` - Firebase Auth login/signup
- `dashboard/firebase.json` - Firebase configuration

### Infrastructure
- `infra/terraform/envs/dev/` - Development Terraform environment
- `.github/workflows/deploy-agent-engine.yml` - Agent Engine deployment workflow
- `.github/workflows/ci.yml` - Continuous integration workflow

---

## Environment Variables

### Required for Agent Engine Deployment
```bash
VERTEX_PROJECT_ID=perception-with-intent
VERTEX_LOCATION=us-central1
```

### Required for E2E Ingestion
```bash
VERTEX_AGENT_ID=<from-gcloud-agents-list>
USER_ID=smoke-test-user (optional, defaults to smoke-test-user)
TRIGGER=manual_e2e_test (optional, defaults to manual_e2e_test)
```

### Optional (for distributed deployments)
```bash
AGENT_SPIFFE_ID=spiffe://perception/agent/[name]
FIRESTORE_DATABASE=(default)
```

### NOT Required (ADK creates automatically)
```bash
VERTEX_AGENT_ENGINE_ID  # Removed from deployment script
```

---

## Verification Commands

### MCP Service Health
```bash
curl https://perception-mcp-348724539390.us-central1.run.app/health
# Expected: {"status": "healthy", "service": "mcp-service", ...}
```

### MCP RSS Fetching
```bash
curl -X POST https://perception-mcp-348724539390.us-central1.run.app/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{"feed_id": "hackernews"}'
# Expected: {"articles": [...], "count": 5}
```

### MCP Logs
```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp"' \
  --project=perception-with-intent \
  --limit=20
```

### Agent Engine Status
```bash
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1
```

### Agent Engine Logs
```bash
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/Agent"' \
  --project=perception-with-intent \
  --limit=20
```

### Firestore Data
```bash
# Ingestion runs
gcloud firestore documents list \
  --collection=ingestion_runs \
  --limit=5 \
  --project=perception-with-intent

# Articles
gcloud firestore documents list \
  --collection=articles \
  --limit=10 \
  --project=perception-with-intent

# Briefs
gcloud firestore documents list \
  --collection=briefs \
  --limit=1 \
  --project=perception-with-intent
```

---

## Cost Monitoring

**Monthly burn rate (estimated):**
- Cloud Run MCP: ~$15 (scale to zero)
- Vertex AI Agent Engine: ~$25
- Gemini 2.0 Flash: ~$20
- Firestore: ~$10
- Firebase Hosting: $0 (Spark plan)
- **Total: ~$70/month**

**Cost Optimization:**
- MCPs scale to zero when idle
- Gemini 2.0 Flash 60% cheaper than GPT-4
- Firebase Hosting free tier covers most traffic
- No Imagen/Lyria costs (text-only analysis)

---

## Lessons Learned (v0.3.0)

### What Went Well

1. **Clear Separation of Concerns**
   - Agent Engine app in one file (`agent_engine_app.py`)
   - Deployment script updated cleanly
   - Documentation follows 6767- prefix rules consistently

2. **Reusable Scripts**
   - Deployment script is environment-agnostic
   - E2E trigger script works for staging and production
   - Verification commands copy-pasteable

3. **Comprehensive Documentation**
   - Observability guide covers all scenarios
   - Deployment guide anticipates common issues
   - Examples provided for every command

### What Could Be Improved

1. **MCP_BASE_URL Configuration Gap**
   - Didn't discover env var passing mechanism during script creation
   - Should have researched ADK env var support upfront
   - **Action:** Research and document in next iteration

2. **No Dry-Run Capability**
   - Deployment script doesn't have `--dry-run` flag
   - Can't validate without actually deploying
   - **Action:** Add validation-only mode to deployment script

3. **Limited Error Handling**
   - Scripts assume happy path
   - No retry logic for transient failures
   - **Action:** Add error handling in future iteration

---

## Continuation Instructions

### For Next Claude Code Session

1. **Read This Document First** - Provides full context and current state
2. **Review Known Issues** - Understand blockers before starting work
3. **Check Immediate Next Steps** - Priorities for continuation
4. **Reference Key Files** - Locations of all critical code
5. **Use Verification Commands** - Validate state before making changes

### For Human Developer

1. **Deploy Agent Engine** - `./scripts/deploy_agent_engine.sh`
2. **Get Agent ID** - `gcloud alpha aiplatform agents list`
3. **Research MCP_BASE_URL** - How to pass env vars to Agent Engine
4. **Run E2E Ingestion** - `./scripts/run_ingestion_via_agent_engine.sh`
5. **Verify Data** - Check Firestore collections

### For Project Handoff

1. **Architecture:** See CLAUDE.md for complete system overview
2. **Deployment:** See 6767-OD-GUID-agent-engine-deploy.md for procedures
3. **Monitoring:** See 6767-AT-ARCH-observability-and-monitoring.md for observability
4. **Release History:** See 6767-PP-PLAN-release-log.md for versions
5. **This Document:** For current state and context

---

## External Resources

- **Google ADK:** https://github.com/google/adk-python
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/docs/agents
- **A2A Protocol:** https://cloud.google.com/vertex-ai/docs/agents/a2a
- **Firebase:** https://firebase.google.com/docs
- **Cloud Run:** https://cloud.google.com/run/docs
- **Firestore:** https://cloud.google.com/firestore/docs

---

**Last Updated:** 2025-11-15
**Version:** v0.3.0
**Status:** Ready for Agent Engine deployment
**Next AAR:** Will be created after successful E2E ingestion run
