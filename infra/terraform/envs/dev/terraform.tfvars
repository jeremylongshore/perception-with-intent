# Perception - AI News Intelligence Platform
# Terraform Variables for Development Environment

project_id  = "perception-with-intent"
billing_id  = "01B257-163362-FC016A"
region      = "us-central1"

# Artifact Registry
repo_name            = "perception-agents"
repo_format          = "DOCKER"
create_artifact_repo = true

# Service Account
enable_service_account       = true
service_account_id           = "perception-agent-runner"
service_account_display_name = "Perception Agent Runner"

# Secret Manager
create_secret             = true
secret_id                 = "perception-agent-config"
secret_replica_locations  = ["us-central1"]
secret_labels = {
  environment = "dev"
  project     = "perception"
  managed_by  = "terraform"
}

# Agent Runtime
runtime_service_name = "perception-runtime"
