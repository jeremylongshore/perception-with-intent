terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "project" {
  source     = "../../modules/project"
  project_id = var.project_id
  billing_id = var.billing_id
}

module "artifact_registry" {
  source            = "../../modules/artifact_registry"
  project_id        = var.project_id
  region            = var.region
  repo_name         = var.repo_name
  create_repository = var.create_artifact_repo
  format            = var.repo_format
}

module "iam" {
  source                       = "../../modules/iam"
  project_id                   = var.project_id
  create_service_account       = var.enable_service_account
  service_account_id           = var.service_account_id
  service_account_display_name = var.service_account_display_name
}

# module "secrets" {
#   source            = "../../modules/secrets"
#   project_id        = var.project_id
#   secret_id         = var.secret_id
#   create_secret     = var.create_secret
#   labels            = var.secret_labels
#   replica_locations = var.secret_replica_locations
# }

module "agent_runtime" {
  source       = "../../modules/agent_runtime"
  project_id   = var.project_id
  region       = var.region
  service_name = var.runtime_service_name
}

output "project_number" {
  description = "Project number resolved by the project module."
  value       = module.project.project_number
}

output "artifact_registry_repo" {
  description = "Artifact Registry repository identifier."
  value       = module.artifact_registry.repository_id
}
