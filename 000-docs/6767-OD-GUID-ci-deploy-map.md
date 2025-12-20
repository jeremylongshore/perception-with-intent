# CI/Deploy Workflow Mapping

**Version:** 1.0
**Date:** 2025-11-14
**Purpose:** Complete inventory of all GitHub Actions workflows, deployment targets, and authentication flow

---

## Workflow Inventory

### 1. ci.yml - Python & Terraform Validation

**File:** `.github/workflows/ci.yml`

**Triggers:**
- `push` to any branch
- `pull_request` to any branch

**Purpose:** Lint and validate Python + Terraform code

**Jobs:**
| Job | Actions | Tools |
|-----|---------|-------|
| validate | Python lint (black, ruff) | Python 3.11, pip |
|  | Terraform fmt check | Terraform 1.9.5 |
|  | Terraform validate | terraform init/fmt/validate |
|  | ADK YAML sanity (TODO) | - |

**GCP Dependencies:** ❌ None (no GCP authentication needed)

**Status:** ✅ Works without GCP credentials

---

### 2. test.yml - Test & Lint

**File:** `.github/workflows/test.yml`

**Triggers:**
- `pull_request` → main
- `push` → main

**Purpose:** Run pytest unit tests + linting (flake8, black, mypy)

**Jobs:**
| Job | Actions | Coverage |
|-----|---------|----------|
| test | Run pytest | ✅ Upload to codecov |
| lint | flake8, black, mypy | - |

**GCP Dependencies:** ❌ None

**Status:** ✅ Works without GCP credentials

---

### 3. deploy-dashboard.yml - Deploy Dashboard to Firebase (WIF)

**File:** `.github/workflows/deploy-dashboard.yml`

**Triggers:**
- `push` → main (only if `dashboard/**` changed)
- `workflow_dispatch` (manual)

**Purpose:** Build and deploy React dashboard to Firebase Hosting

**Deployment Targets:**

| Target | Value | Source |
|--------|-------|--------|
| **Project ID** | `perception-with-intent` | Hardcoded |
| **Hosting Site** | `perception-with-intent` | Hardcoded |
| **URL** | https://perception-with-intent.web.app | Firebase auto-generated |
| **Region** | N/A (Firebase Hosting is global CDN) | - |

**Authentication:**
- **WIF Provider:** `${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}`
- **Service Account:** `${{ secrets.GCP_SERVICE_ACCOUNT }}`

**Build:**
- Node.js 20
- `npm ci` → `npm run build` in `dashboard/`
- Output: `dashboard/dist/`

**Deploy:**
```bash
firebase deploy --only hosting --project perception-with-intent --non-interactive
```

**Status:** ⚠️ Ready but requires WIF secrets configured

---

### 4. deploy-firebase-dashboard.yml - Duplicate Dashboard Deploy

**File:** `.github/workflows/deploy-firebase-dashboard.yml`

**Triggers:**
- `push` → main (only if `dashboard/**` changed)
- `workflow_dispatch`

**Purpose:** DUPLICATE of deploy-dashboard.yml (same functionality)

**Status:** ⚠️ REDUNDANT - Consider removing

---

### 5. deploy-agent-engine.yml - Manual Agent Engine Deploy

**File:** `.github/workflows/deploy-agent-engine.yml`

**Triggers:**
- `workflow_dispatch` (manual only) with inputs:
  - `project_id` (required)
  - `location` (required, e.g., us-central1)
  - `agent_engine_id` (required)

**Purpose:** Deploy agent(s) to Vertex AI Agent Engine via manual inputs

**Deployment Targets:**

| Target | Value | Source |
|--------|-------|--------|
| **Project ID** | User input | `${{ github.event.inputs.project_id }}` |
| **Region** | User input | `${{ github.event.inputs.location }}` |
| **Agent Engine ID** | User input | `${{ github.event.inputs.agent_engine_id }}` |

**Authentication:**
- **WIF Provider:** `${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}`
- **Service Account:** `${{ secrets.GCP_SERVICE_ACCOUNT_EMAIL }}`

**Deploy Script:** `scripts/deploy_agent_engine.sh`

**Status:** ⚠️ Requires ADK CLI (`google-adk-cli`) - TODO: verify package name

---

### 6. deploy-agents.yml - Vertex AI Agents Deploy

**File:** `.github/workflows/deploy-agents.yml`

**Triggers:**
- `push` → main (only if `app/**` or `infra/**` changed)
- `workflow_dispatch`

**Purpose:** Deploy agents to Vertex AI using ADK

**Deployment Targets:**

| Target | Value | Source |
|--------|-------|--------|
| **Project ID** | `perception-with-intent` | Hardcoded |
| **Region** | `us-central1` | Hardcoded |
| **Staging Bucket** | `gs://perception-staging` | Hardcoded |
| **Display Name (Agent 0)** | "Perception Root Orchestrator" | Hardcoded |
| **Display Name (Agent 1)** | "Perception Topic Manager" | Hardcoded |

**Authentication:**
- **WIF Provider:** `${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}`
- **Service Account:** `${{ secrets.GCP_SERVICE_ACCOUNT_EMAIL }}`

**Deploy Commands:**
```bash
# Agent 0
adk deploy agent_engine \
  --project=perception-with-intent \
  --region=us-central1 \
  --staging_bucket=gs://perception-staging \
  --display_name="Perception Root Orchestrator" \
  app/perception_agent/agents/agent_0_orchestrator.yaml \
  --trace_to_cloud \
  --cpu=2 --memory=2Gi \
  --min_instances=0 --max_instances=5

# Agent 1
adk deploy agent_engine \
  --project=perception-with-intent \
  --region=us-central1 \
  --staging_bucket=gs://perception-staging \
  --display_name="Perception Topic Manager" \
  app/perception_agent/agents/agent_1_topic_manager.yaml \
  --trace_to_cloud \
  --cpu=1 --memory=1Gi \
  --min_instances=0 --max_instances=3
```

**Issues:**
- ❌ References `agent_1_topic_manager.yaml` (should be `agent_1_source_harvester.yaml`)
- ❌ Only deploys 2 of 8 agents

**Status:** ⚠️ OUT OF DATE - needs agent filename corrections

---

### 7. deploy.yml - Full Deployment (Agents + Dashboard)

**File:** `.github/workflows/deploy.yml`

**Triggers:**
- `push` → main
- `workflow_dispatch`

**Purpose:** Deploy entire system (agents + dashboard) in sequence

**Deployment Targets:**

| Component | Target | Value |
|-----------|--------|-------|
| **Agents** | Project | `perception-with-intent` |
|  | Region | `us-central1` |
|  | Display Name | "Perception Intelligence System" |
|  | YAML | `app/perception_agent/agents/agent_0_root_orchestrator.yaml` ❌ |
|  | Staging Bucket | `gs://perception-staging` |
| **Dashboard** | Project | `perception-with-intent` |
|  | Hosting Site | Firebase Hosting |
|  | URL | https://perception-with-intent.web.app |

**Authentication:**
- **WIF Provider:** `${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}`
- **Service Account:** `${{ secrets.GCP_SERVICE_ACCOUNT_EMAIL }}`

**Jobs:**
1. `deploy-agents` - Deploy to Vertex AI
2. `deploy-dashboard` - Deploy to Firebase (after agents succeed)
3. `notify` - Report status

**Issues:**
- ❌ References `agent_0_root_orchestrator.yaml` (should be `agent_0_orchestrator.yaml`)
- ✅ Uses Docker build (pushes to Artifact Registry)

**Status:** ⚠️ OUT OF DATE - needs agent filename correction

---

## Missing Workflows

### 1. MCP Service Deployment

**Status:** ❌ NOT YET CREATED

**Required:**
- Deploy `app/mcp_service/` to Cloud Run
- Service name: `perception-mcp` or similar
- Region: `us-central1`
- Dockerfile needed

### 2. CI Smoke Tests

**Status:** ❌ NOT YET CREATED

**Required:**
- Workflow that runs WITHOUT GCP credentials
- Validates agent YAML files
- Validates MCP service can start
- Runs unit tests
- Does NOT deploy anything

---

## Authentication Flow (WIF)

**Workload Identity Federation (WIF)** is used for keyless authentication:

```
GitHub Actions
    ↓ (OIDC token)
Google Cloud Workload Identity Pool
    ↓ (impersonate)
Service Account
    ↓ (permissions)
GCP Resources (Cloud Run, Vertex AI, Firebase)
```

**Required Secrets:**

| Secret Name | Purpose | Example Value |
|-------------|---------|---------------|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | WIF provider resource name | `projects/123/locations/global/workloadIdentityPools/github/providers/github-provider` |
| `GCP_SERVICE_ACCOUNT_EMAIL` | Service account to impersonate | `github-actions@perception-with-intent.iam.gserviceaccount.com` |
| `GCP_SERVICE_ACCOUNT` | Alias for service account email | Same as above |
| `FIREBASE_API_KEY` | Firebase API key (if needed) | `AIzaSyB...` |
| `GITHUB_TOKEN` | Auto-provided by GitHub | Auto-generated |

**Note:** Some workflows use `GCP_SERVICE_ACCOUNT_EMAIL`, others use `GCP_SERVICE_ACCOUNT`. These should be unified.

---

## Deployment Target Summary

### Google Cloud Project

| Field | Value | Status |
|-------|-------|--------|
| **Project ID** | `perception-with-intent` | ✅ Configured |
| **Project Number** | `348724539390` | ✅ Verified |
| **Default Region** | `us-central1` | ✅ Used in workflows |

### Firebase Hosting

| Field | Value | Status |
|-------|-------|--------|
| **Site ID** | `perception-with-intent` | ✅ Configured |
| **URL** | https://perception-with-intent.web.app | ✅ Ready |
| **Deploy Source** | `dashboard/dist/` | ✅ Built locally |

### Vertex AI Agent Engine

| Field | Value | Status |
|-------|-------|--------|
| **Project** | `perception-with-intent` | ✅ |
| **Region** | `us-central1` | ✅ |
| **Staging Bucket** | `gs://perception-staging` | ⚠️ Must be created |
| **Display Name** | "Perception Intelligence System" (deploy.yml)<br>OR "Perception Root Orchestrator" (deploy-agents.yml) | ⚠️ Inconsistent |
| **Entrypoint** | `app/agent_engine_app.py` (implied) | ✅ |
| **Agent Configs** | 8 YAML files in `app/perception_agent/agents/` | ✅ |

**Agent YAML Filenames (CORRECT):**
1. `agent_0_orchestrator.yaml` ✅
2. `agent_1_source_harvester.yaml` ✅
3. `agent_2_topic_manager.yaml` ✅
4. `agent_3_relevance_ranking.yaml` ✅
5. `agent_4_brief_writer.yaml` ✅
6. `agent_5_alert_anomaly.yaml` ✅
7. `agent_6_validator.yaml` ✅
8. `agent_7_storage_manager.yaml` ✅

**Issues in Workflows:**
- ❌ `deploy-agents.yml` references `agent_1_topic_manager.yaml` (wrong)
- ❌ `deploy.yml` references `agent_0_root_orchestrator.yaml` (wrong)

### Cloud Run (Future - MCP Service)

| Field | Value | Status |
|-------|-------|--------|
| **Project** | `perception-with-intent` | ✅ |
| **Region** | `us-central1` | ✅ Planned |
| **Service Name** | `perception-mcp` | ⏸️ To be created |
| **Source** | `app/mcp_service/` | ✅ Ready |
| **Dockerfile** | - | ❌ Not created yet |

---

## Unknowns / TODOs

1. **ADK CLI Package Name**
   - Workflows reference `google-adk-cli` and `google-adk`
   - TODO: Verify correct package name for ADK deployment

2. **Staging Bucket Existence**
   - `gs://perception-staging` referenced but may not exist
   - TODO: Create bucket or verify it exists

3. **Service Account Permissions**
   - Unknown if `github-actions@perception-with-intent.iam.gserviceaccount.com` has:
     - `roles/run.admin` (Cloud Run deploy)
     - `roles/iam.serviceAccountUser` (impersonation)
     - `roles/aiplatform.user` (Vertex AI Agent Engine)
     - `roles/firebase.admin` (Firebase Hosting)

4. **Artifact Registry Repository**
   - `us-central1-docker.pkg.dev/perception-with-intent/perception-agents` referenced
   - TODO: Verify repository exists

5. **Secret Manager Values**
   - TODO: Verify all secrets are configured in GitHub repo settings

---

## Workflow Cleanup Recommendations

1. **Remove Duplicate:**
   - Delete `.github/workflows/deploy-firebase-dashboard.yml` (duplicate of deploy-dashboard.yml)

2. **Fix Agent Filenames:**
   - Update `deploy-agents.yml` line 69: `agent_1_topic_manager.yaml` → `agent_1_source_harvester.yaml`
   - Update `deploy.yml` line 69: `agent_0_root_orchestrator.yaml` → `agent_0_orchestrator.yaml`

3. **Unify Secret Names:**
   - Standardize on `GCP_SERVICE_ACCOUNT_EMAIL` everywhere
   - Remove references to `GCP_SERVICE_ACCOUNT` (use `GCP_SERVICE_ACCOUNT_EMAIL` instead)

4. **Add Missing Workflows:**
   - Create `ci-smoke.yml` - Smoke tests without GCP
   - Create `deploy-mcp.yml` - Deploy MCP service to Cloud Run

5. **Complete Agent Deployment:**
   - Update `deploy-agents.yml` to deploy all 8 agents (currently only 2)

---

## Verification Commands

### Check Workflow Syntax

```bash
# Install actionlint
brew install actionlint  # or use go install

# Lint all workflows
actionlint .github/workflows/*.yml
```

### Check GCP Configuration

```bash
# Verify project
gcloud config get-value project

# Check staging bucket
gsutil ls gs://perception-staging

# List Cloud Run services
gcloud run services list --region=us-central1

# Check Artifact Registry
gcloud artifacts repositories list --location=us-central1
```

### Check Service Account Permissions

```bash
# List service account IAM bindings
gcloud projects get-iam-policy perception-with-intent \
  --flatten="bindings[].members" \
  --filter="bindings.members:github-actions@perception-with-intent.iam.gserviceaccount.com"
```

---

**Last Updated:** 2025-11-14
**Status:** Inventory Complete - Issues Identified
**Next:** Create smoke test workflow + MCP deploy workflow + fix agent filenames
