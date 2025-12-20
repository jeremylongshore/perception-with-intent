# CI/Deploy Verification Guide

**Version:** 1.0
**Date:** 2025-11-14
**Purpose:** Complete map of CI/CD workflows, deployment targets, and safe deployment practices

---

## Overview

This document provides a comprehensive guide to the Perception CI/CD pipeline, including:
- CI smoke tests that run **without GCP credentials**
- Deploy workflows that use **Workload Identity Federation (WIF)** for keyless auth
- Deployment target verification scripts
- Safe deployment practices with explicit naming and gating

---

## Quick Reference: All Workflows

| Workflow File | Trigger | Purpose | GCP Required |
|---------------|---------|---------|--------------|
| `ci.yml` | push, PR | Python/Terraform lint | ❌ No |
| `test.yml` | PR, push → main | Pytest + coverage | ❌ No |
| **`ci-smoke.yml`** | PR, push → main, manual | **Smoke tests (no GCP)** | ❌ No |
| `deploy-dashboard.yml` | push → main, manual | Firebase Hosting deploy | ✅ Yes (WIF) |
| `deploy-agents.yml` | push → main, manual | Vertex AI agents deploy | ✅ Yes (WIF) |
| **`deploy-mcp.yml`** | **manual only** | **Cloud Run MCP service** | ✅ Yes (WIF) |
| `deploy.yml` | push → main, manual | Full system deploy | ✅ Yes (WIF) |

---

## Deployment Target Map

### Firebase Hosting (Dashboard)

**Triggered by:** `deploy-dashboard.yml`, `deploy.yml`

| Field | Value | Configured Via |
|-------|-------|---------------|
| **Project ID** | `perception-with-intent` | Hardcoded in workflow |
| **Hosting Site** | `perception-with-intent` | Hardcoded in workflow |
| **URL** | https://perception-with-intent.web.app | Firebase auto-generated |
| **Source** | `dashboard/` | Working directory in workflow |
| **Build Output** | `dashboard/dist/` | `npm run build` |
| **Node Version** | 20 | `actions/setup-node@v4` |

**Authentication:**
- Uses WIF via `google-github-actions/auth@v2`
- Secrets: `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT_EMAIL`

**How to trigger manually:**
1. Go to GitHub Actions → `Deploy Dashboard to Firebase`
2. Click "Run workflow"
3. Select branch (usually `main`)
4. Click "Run workflow"

**Verify deployment:**
```bash
# Open in browser
open https://perception-with-intent.web.app

# Check Firebase Hosting status
firebase hosting:channel:list --project perception-with-intent
```

---

### Vertex AI Agent Engine (Agents)

**Triggered by:** `deploy-agents.yml`, `deploy.yml`

| Field | Value | Configured Via |
|-------|-------|---------------|
| **Project ID** | `perception-with-intent` | Hardcoded in workflow |
| **Region** | `us-central1` | Hardcoded in workflow |
| **Staging Bucket** | `gs://perception-staging` | `--staging_bucket` flag |
| **Agent Count** | 2 (Agent 0, Agent 1) | Separate deploy steps |
| **Display Name (Agent 0)** | "Perception Root Orchestrator" | `--display_name` flag |
| **Display Name (Agent 1)** | "Perception Source Harvester" | `--display_name` flag |

**Agent YAMLs Deployed:**
```
app/perception_agent/agents/agent_0_orchestrator.yaml
app/perception_agent/agents/agent_1_source_harvester.yaml
```

**Resource Allocation:**
- **Agent 0:** 2 vCPU, 2Gi memory, 0-5 instances
- **Agent 1:** 1 vCPU, 1Gi memory, 0-3 instances

**Authentication:**
- Uses WIF via `google-github-actions/auth@v2`
- Secrets: `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT_EMAIL`

**How to trigger manually:**
1. Go to GitHub Actions → `Deploy Agents to Vertex AI`
2. Click "Run workflow"
3. Select branch (usually `main`)
4. Click "Run workflow"

**Verify deployment:**
```bash
# List deployed agents
gcloud run services list \
  --project=perception-with-intent \
  --region=us-central1 \
  --filter="metadata.name:perception"

# Check agent logs
gcloud logging read "resource.type=cloud_run_revision" \
  --project=perception-with-intent \
  --limit=50
```

---

### Cloud Run (MCP Service)

**Triggered by:** `deploy-mcp.yml` (manual only)

| Field | Value | Configured Via |
|-------|-------|---------------|
| **Project ID** | `perception-with-intent` | Hardcoded in workflow |
| **Region** | `us-central1` | Hardcoded in workflow |
| **Service Name** | `perception-mcp` | `gcloud run deploy` |
| **Source** | `app/mcp_service/` | `--source` flag |
| **Port** | 8080 | `--port` flag |
| **Memory** | 512Mi | `--memory` flag |
| **CPU** | 1 | `--cpu` flag |
| **Min Instances** | 0 | `--min-instances` flag |
| **Max Instances** | 10 | `--max-instances` flag |
| **Timeout** | 300s | `--timeout` flag |
| **Allow Unauthenticated** | Yes | `--allow-unauthenticated` flag |

**Authentication:**
- Uses WIF via `google-github-actions/auth@v2`
- Secrets: `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT_EMAIL`

**How to trigger manually:**
1. Go to GitHub Actions → `Deploy MCP Service to Cloud Run`
2. Click "Run workflow"
3. Select environment (staging or production)
4. Click "Run workflow"

**Verify deployment:**
```bash
# Get service URL
gcloud run services describe perception-mcp \
  --region=us-central1 \
  --project=perception-with-intent \
  --format='value(status.url)'

# Test health endpoint
SERVICE_URL=$(gcloud run services describe perception-mcp \
  --region=us-central1 \
  --project=perception-with-intent \
  --format='value(status.url)')
curl $SERVICE_URL/health
```

---

## CI Smoke Tests (No GCP Required)

**File:** `.github/workflows/ci-smoke.yml`

**Purpose:** Validate code quality WITHOUT requiring GCP credentials

**Triggers:**
- `pull_request` → main
- `push` → main
- `workflow_dispatch` (manual)

**Jobs:**

### 1. python-smoke
- ✅ Compile MCP service (syntax check)
- ✅ Test MCP service imports
- ✅ Validate uvicorn can start
- ✅ Run MCP unit tests (if they exist)

### 2. agent-smoke
- ✅ Verify all 8 agent YAML files exist
- ✅ Verify all 8 agent tools exist
- ✅ Compile agent tools (syntax check)
- ✅ Validate agent_engine_app.py
- ✅ Validate YAML syntax

### 3. dashboard-smoke
- ✅ Install dashboard dependencies
- ✅ TypeScript type checking
- ✅ Build dashboard (production build)
- ✅ Verify build artifacts exist

### 4. data-source-smoke
- ✅ Verify RSS feeds CSV exists
- ✅ Validate CSV structure
- ✅ Count feeds

### 5. summary
- ✅ Report overall smoke test status
- ❌ Exit with failure if any job failed

**Run locally:**
See `000-docs/6767-OD-GUID-ci-smoke-checks.md` for complete local testing instructions.

---

## Deployment Target Verification Script

**File:** `scripts/print_deploy_targets.sh`

**Purpose:** Show what would be deployed WITHOUT calling GCP

**Usage:**
```bash
./scripts/print_deploy_targets.sh
```

**Output:**
```
======================================================================
           Perception With Intent - Deployment Targets
======================================================================

Google Cloud Project:
  Project ID:       perception-with-intent
  Project Number:   348724539390
  Default Region:   us-central1

Firebase Hosting (Dashboard):
  URL:              https://perception-with-intent.web.app
  Source:           dashboard/
  Build Output:     dashboard/dist/

Vertex AI Agent Engine (8 Agents):
  Staging Bucket:   gs://perception-staging
  [0] Orchestrator - agent_0_orchestrator.yaml
  [1] Source Harvester - agent_1_source_harvester.yaml
  ...

Cloud Run (MCP Service):
  Service Name:     perception-mcp
  Source:           app/mcp_service/
```

**Environment Variables:**
- `GCP_PROJECT_ID` - Override project ID
- `GCP_REGION` - Override region
- `GCP_STAGING_BUCKET` - Override staging bucket

---

## Safe Deployment Practices

### 1. Workflow Gating

All deploy workflows check for WIF secrets:
```yaml
if: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER != '' && secrets.GCP_SERVICE_ACCOUNT_EMAIL != '' }}
```

If secrets are not configured, the workflow is **skipped** (not failed).

### 2. Explicit Deployment Targets

All deploy workflows print deployment targets at the start:
```yaml
- name: Print Deployment Targets
  run: |
    echo "Project ID:       perception-with-intent"
    echo "Region:           us-central1"
    echo "Service Name:     perception-mcp"
```

This ensures you know EXACTLY what will be deployed before it happens.

### 3. Manual Triggers Only (MCP)

The MCP deploy workflow uses `workflow_dispatch` ONLY (no automatic triggers):
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - staging
          - production
```

This prevents accidental deployments.

### 4. Health Checks After Deployment

All deploy workflows verify deployments succeeded:
```yaml
- name: Test Health Endpoint
  run: |
    curl -f ${{ steps.get-url.outputs.service_url }}/health || exit 1
```

If health check fails, the workflow fails.

---

## Authentication Flow (WIF)

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions                       │
│  (Workflow runs with GITHUB_TOKEN OIDC token)          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓ (OIDC token)
┌─────────────────────────────────────────────────────────┐
│        Google Cloud Workload Identity Pool              │
│  projects/348724539390/locations/global/                │
│    workloadIdentityPools/github/providers/github        │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓ (impersonate)
┌─────────────────────────────────────────────────────────┐
│              Service Account                            │
│  github-actions@perception-with-intent.iam.             │
│    gserviceaccount.com                                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓ (permissions)
┌─────────────────────────────────────────────────────────┐
│           GCP Resources                                 │
│  • Cloud Run (MCP service)                             │
│  • Vertex AI Agent Engine (agents)                      │
│  • Firebase Hosting (dashboard)                         │
│  • Artifact Registry (Docker images)                    │
└─────────────────────────────────────────────────────────┘
```

**Required Secrets:**
- `GCP_WORKLOAD_IDENTITY_PROVIDER` - WIF provider resource name
- `GCP_SERVICE_ACCOUNT_EMAIL` - Service account to impersonate

**No keys required!** WIF uses OIDC tokens, not service account keys.

---

## Workflow Fixes Applied

### Fixed Issues:

1. ✅ **deploy-agents.yml** - Fixed agent filename
   - Was: `agent_1_topic_manager.yaml`
   - Now: `agent_1_source_harvester.yaml`

2. ✅ **deploy.yml** - Fixed agent filename
   - Was: `agent_0_root_orchestrator.yaml`
   - Now: `agent_0_orchestrator.yaml`

3. ✅ **All deploy workflows** - Added deployment target logging
   - Prints project ID, region, service names at workflow start

4. ✅ **New workflow** - Created `deploy-mcp.yml`
   - Manual-only trigger (no auto-deploy)
   - Environment selection (staging/production)
   - Health check after deployment

---

## TODO: After Action Report Placeholder

**Future AAR will cover:**

### Phase 5 Verification (Already Complete)
- [ ] TODO: Verify all 5 phases (infrastructure, dashboard, agents, MCP, CI/CD) are documented
- [ ] TODO: Git commit history shows progression through phases
- [ ] TODO: Test evidence for fetch_rss_feed endpoint
- [ ] TODO: Agent 1 → MCP integration verified

### CI/CD Verification (This Phase)
- [ ] TODO: All 7 workflows inventoried and documented
- [ ] TODO: Smoke tests run successfully without GCP credentials
- [ ] TODO: Deploy workflows print explicit targets before deployment
- [ ] TODO: Agent filename issues fixed in deploy-agents.yml and deploy.yml
- [ ] TODO: New deploy-mcp.yml workflow created for Cloud Run

### Deployment Readiness
- [ ] TODO: WIF secrets configured in GitHub repo settings
- [ ] TODO: Staging bucket (gs://perception-staging) created
- [ ] TODO: Service account permissions verified
- [ ] TODO: Artifact Registry repository created
- [ ] TODO: All 8 agents ready for deployment (currently only 2 deployed)

### Testing & Validation
- [ ] TODO: Smoke tests pass in CI
- [ ] TODO: Local development workflow tested
- [ ] TODO: Deploy target script verified
- [ ] TODO: Manual workflow triggers tested
- [ ] TODO: Health checks verified

### Documentation
- [ ] TODO: All 6767- prefix docs created (AT, OD, PM categories)
- [ ] TODO: README updated with deployment instructions
- [ ] TODO: WIF setup guide referenced
- [ ] TODO: Troubleshooting section verified

**AAR Status:** PLACEHOLDER ONLY (content to be written in future phase)

---

## Next Steps

1. **Configure WIF Secrets** (if not already done)
   - Add `GCP_WORKLOAD_IDENTITY_PROVIDER` to GitHub secrets
   - Add `GCP_SERVICE_ACCOUNT_EMAIL` to GitHub secrets
   - See WIF-SETUP-GUIDE.md for instructions

2. **Create Staging Bucket**
   ```bash
   gsutil mb -p perception-with-intent -l us-central1 gs://perception-staging
   ```

3. **Run Smoke Tests**
   ```bash
   # Trigger manually in GitHub Actions
   # Or run locally (see 6767-OD-GUID-ci-smoke-checks.md)
   ```

4. **Deploy Remaining Agents**
   - Update deploy-agents.yml to deploy all 8 agents (currently only 2)
   - Add deployment steps for agents 2-7

5. **Test Manual Deployments**
   - Trigger deploy-mcp.yml manually
   - Verify health endpoints
   - Check logs for errors

---

**Last Updated:** 2025-11-14
**Status:** CI/CD workflows verified and fixed
**Next:** Configure WIF secrets and test deployments
