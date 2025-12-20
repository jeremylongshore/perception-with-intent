#!/usr/bin/env bash
#
# Print Deployment Targets
#
# This script displays the expected deployment targets for all Perception components.
# It does NOT call GCP - it just shows what would be deployed based on env vars and defaults.
#
# Usage:
#   ./scripts/print_deploy_targets.sh
#
# Environment variables (optional):
#   GCP_PROJECT_ID - Override default project ID
#   GCP_REGION - Override default region

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Defaults
DEFAULT_PROJECT_ID="perception-with-intent"
DEFAULT_REGION="us-central1"
DEFAULT_STAGING_BUCKET="gs://perception-staging"

# Read from env or use defaults
PROJECT_ID="${GCP_PROJECT_ID:-$DEFAULT_PROJECT_ID}"
REGION="${GCP_REGION:-$DEFAULT_REGION}"
STAGING_BUCKET="${GCP_STAGING_BUCKET:-$DEFAULT_STAGING_BUCKET}"

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}           Perception With Intent - Deployment Targets${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

echo -e "${GREEN}Google Cloud Project:${NC}"
echo "  Project ID:       $PROJECT_ID"
echo "  Project Number:   348724539390"
echo "  Default Region:   $REGION"
echo ""

echo -e "${GREEN}Firebase Hosting (Dashboard):${NC}"
echo "  Project:          $PROJECT_ID"
echo "  Site ID:          perception-with-intent"
echo "  URL:              https://perception-with-intent.web.app"
echo "  Source:           dashboard/"
echo "  Build Output:     dashboard/dist/"
echo ""

echo -e "${GREEN}Vertex AI Agent Engine (8 Agents):${NC}"
echo "  Project:          $PROJECT_ID"
echo "  Region:           $REGION"
echo "  Staging Bucket:   $STAGING_BUCKET"
echo ""
echo "  Agent Deployments:"
echo "    [0] Orchestrator"
echo "        Display Name: Perception Root Orchestrator"
echo "        YAML:         app/perception_agent/agents/agent_0_orchestrator.yaml"
echo "        CPU:          2 vCPU"
echo "        Memory:       2Gi"
echo "        Instances:    0-5"
echo ""
echo "    [1] Source Harvester"
echo "        Display Name: Perception Source Harvester"
echo "        YAML:         app/perception_agent/agents/agent_1_source_harvester.yaml"
echo "        CPU:          1 vCPU"
echo "        Memory:       1Gi"
echo "        Instances:    0-3"
echo ""
echo "    [2] Topic Manager"
echo "        Display Name: Perception Topic Manager"
echo "        YAML:         app/perception_agent/agents/agent_2_topic_manager.yaml"
echo "        CPU:          1 vCPU"
echo "        Memory:       1Gi"
echo "        Instances:    0-3"
echo ""
echo "    [3] Relevance & Ranking"
echo "        Display Name: Perception Relevance & Ranking"
echo "        YAML:         app/perception_agent/agents/agent_3_relevance_ranking.yaml"
echo "        CPU:          2 vCPU"
echo "        Memory:       2Gi"
echo "        Instances:    0-5"
echo ""
echo "    [4] Brief Writer"
echo "        Display Name: Perception Brief Writer"
echo "        YAML:         app/perception_agent/agents/agent_4_brief_writer.yaml"
echo "        CPU:          1 vCPU"
echo "        Memory:       1Gi"
echo "        Instances:    0-3"
echo ""
echo "    [5] Alert & Anomaly"
echo "        Display Name: Perception Alert & Anomaly"
echo "        YAML:         app/perception_agent/agents/agent_5_alert_anomaly.yaml"
echo "        CPU:          1 vCPU"
echo "        Memory:       1Gi"
echo "        Instances:    0-3"
echo ""
echo "    [6] Validator"
echo "        Display Name: Perception Validator"
echo "        YAML:         app/perception_agent/agents/agent_6_validator.yaml"
echo "        CPU:          1 vCPU"
echo "        Memory:       1Gi"
echo "        Instances:    0-3"
echo ""
echo "    [7] Storage Manager"
echo "        Display Name: Perception Storage Manager"
echo "        YAML:         app/perception_agent/agents/agent_7_storage_manager.yaml"
echo "        CPU:          1 vCPU"
echo "        Memory:       1Gi"
echo "        Instances:    0-3"
echo ""

echo -e "${GREEN}Cloud Run (MCP Service):${NC}"
echo "  Project:          $PROJECT_ID"
echo "  Region:           $REGION"
echo "  Service Name:     perception-mcp"
echo "  Source:           app/mcp_service/"
echo "  Dockerfile:       app/mcp_service/Dockerfile (TODO: create)"
echo "  Port:             8080 (Cloud Run standard)"
echo "  Min Instances:    0"
echo "  Max Instances:    10"
echo "  Concurrency:      80"
echo ""

echo -e "${GREEN}Artifact Registry:${NC}"
echo "  Project:          $PROJECT_ID"
echo "  Region:           $REGION"
echo "  Repository:       perception-agents"
echo "  Full Path:        $REGION-docker.pkg.dev/$PROJECT_ID/perception-agents"
echo ""

echo -e "${YELLOW}Service Accounts:${NC}"
echo "  GitHub Actions:   github-actions@$PROJECT_ID.iam.gserviceaccount.com"
echo "  MCP Service:      mcp-service@$PROJECT_ID.iam.gserviceaccount.com"
echo "  Agent Engine:     Default Compute Engine service account"
echo ""

echo -e "${YELLOW}Required Secrets (GitHub):${NC}"
echo "  GCP_WORKLOAD_IDENTITY_PROVIDER - WIF provider resource name"
echo "  GCP_SERVICE_ACCOUNT_EMAIL      - Service account to impersonate"
echo "  FIREBASE_API_KEY               - Firebase API key (optional)"
echo ""

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}                            Summary${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""
echo "  Total Components:  3 (Dashboard, Agents, MCP Service)"
echo "  Agent Count:       8"
echo "  Cloud Run Services: 2 (Agent Engine runtime + MCP Service)"
echo "  Firebase Sites:    1 (Dashboard)"
echo ""
echo -e "${YELLOW}Note: This script does not verify if these resources exist in GCP.${NC}"
echo -e "${YELLOW}      Use 'gcloud' commands to check actual deployment status.${NC}"
echo ""
