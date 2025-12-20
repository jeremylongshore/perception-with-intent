# Changelog

All notable changes to the Perception With Intent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Context handoff document for session continuity
- Comprehensive observability stack documentation
- Agent Engine deployment guide
- E2E ingestion trigger script

## [0.3.0] - 2025-11-15

### Added
- **MCP Service deployed to Cloud Run** (`perception-mcp`)
  - Service URL: `https://perception-mcp-348724539390.us-central1.run.app`
  - Dockerfile for containerization
  - Health endpoint returning JSON status
  - Real RSS feed fetching validated (5+ articles, 270ms latency)
- **Cloud Logging integration**
  - Structured JSON logs for all MCP requests
  - Request path, method, status, latency tracking
  - No ERROR-level logs (clean service)
- **Observability documentation** (`6767-AT-ARCH-observability-and-monitoring.md`)
  - Cloud Logging queries and filters
  - Cloud Run metrics dashboard setup
  - Verification procedures for MCP health
  - Troubleshooting guide
- **Agent Engine deployment infrastructure**
  - Updated `scripts/deploy_agent_engine.sh` to use `agent_engine_app.py`
  - Deployment guide (`6767-OD-GUID-agent-engine-deploy.md`)
  - E2E ingestion trigger script (`scripts/run_ingestion_via_agent_engine.sh`)
- **Release log** (`6767-PP-PLAN-release-log.md`)
  - Version tracking across all releases
  - Links to AARs for detailed analysis
- **First AAR** (`041-AA-REPT-phase-E2E-agent-engine-deployment.md`)
  - Documents Agent Engine deployment phase
  - Known issues and next steps
  - Lessons learned

### Changed
- **MCP deployment script** (`scripts/deploy_agent_engine.sh`)
  - Removed old JVP agent references
  - Now uses `agent_engine_app.py` (correct entrypoint)
  - Added telemetry flags (`--trace_to_cloud`)
  - Removed `VERTEX_AGENT_ENGINE_ID` requirement (ADK creates it)

### Fixed
- Cloud Build IAM permissions for MCP deployment
  - Granted `storage.objectViewer` to default service account
  - Granted `logging.logWriter` for Cloud Logging
  - Granted `artifactregistry.writer` for container registry

### Infrastructure
- **Cloud Run MCP Service:**
  - Memory: 512Mi
  - CPU: 1
  - Min Instances: 0
  - Max Instances: 10
  - Port: 8080
  - Ingress: `all` (testing), will be `internal-and-cloud-load-balancing` (production)
- **IAM Permissions:**
  - MCP service account permissions configured
  - Cloud Build service account permissions configured

## [0.2.0] - 2025-11-14

### Added
- **Complete 8-agent system**
  - Agent 0: Root Orchestrator (`run_daily_ingestion()`)
  - Agent 1: Source Harvester (MCP integration)
  - Agent 2: Topic Manager (Firestore topics)
  - Agent 3: Relevance & Ranking (keyword scoring)
  - Agent 4: Brief Writer (section-based briefs)
  - Agent 5: Alert & Anomaly Detector (stub)
  - Agent 6: Validator (schema validation)
  - Agent 7: Storage Manager (Firestore batch operations)
  - Agent 8: Technology Desk Editor (tech section curation)
- **E2E Ingestion Pipeline**
  - Complete workflow from RSS fetch to Firestore storage
  - Production keyword-based scoring (title 3x, content 1x)
  - Section inference (Tech, Business, Politics, Sports, General)
  - Validation layer for articles and briefs
  - Firestore batch writes with URL-based deduplication
- **MCP Service Scaffolding**
  - All 7 MCP tools stubbed
  - Real implementation: `fetch_rss_feed`
  - FastAPI framework with CORS middleware
  - Health check endpoint
- **Documentation**
  - E2E architecture guide (`6767-AT-ARCH-e2e-ingestion-and-tech-editor.md`)
  - Developer ingestion run guide (`6767-OD-GUID-dev-ingestion-run.md`)
  - Updated agents overview (`012-AT-ARCH-agents-overview.md`)
- **Development Scripts**
  - `scripts/run_ingestion_once.py` for local testing

### Changed
- Agent tool implementations from stubs to production code
- Firestore client to lazy initialization pattern
- Agent 0 orchestrator to support full E2E workflow

## [0.1.0] - 2025-11-13

### Added
- **Initial Project Setup**
  - GCP project created (`perception-with-intent`)
  - Firestore schema defined
  - Firebase dashboard scaffolding (React + TypeScript + Vite)
  - GitHub workflows for CI/CD
  - Workload Identity Federation (WIF) configured
- **Agent Configurations**
  - YAML configs for 8 agents
  - Agent tools structure established
  - A2A Protocol integration
- **Infrastructure as Code**
  - Terraform modules (placeholder)
  - Cloud Run service definitions
  - Firestore schema documentation
- **Documentation Foundation**
  - Architecture overview (`010-AT-ARCH-perception-build-plan.md`)
  - Firestore schema (`001-AT-ARCH-firestore-schema.md`)
  - Build phases plan (`011-PP-PLAN-build-phases-architecture.md`)
  - Product roadmap (`008-PP-PLAN-product-roadmap.md`)

### Infrastructure
- **GCP Project:** perception-with-intent
- **Region:** us-central1
- **Firestore:** Native mode
- **Firebase Hosting:** Configured
- **GitHub Repository:** jeremylongshore/perception-with-intent

---

## Release Links

- [0.3.0 AAR](000-docs/041-AA-REPT-phase-E2E-agent-engine-deployment.md)
- [Release Log](000-docs/6767-PP-PLAN-release-log.md)
- [Observability Guide](000-docs/6767-AT-ARCH-observability-and-monitoring.md)
- [Agent Engine Deployment](000-docs/6767-OD-GUID-agent-engine-deploy.md)

---

**Note:** For detailed technical analysis of each release, see the corresponding After Action Report (AAR) in `000-docs/`.
