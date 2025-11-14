variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "billing_id" {
  description = "Billing account ID. // TODO(ask): Validate requirement per org policy."
  type        = string
}

variable "region" {
  description = "Primary region for IAMJVP infrastructure."
  type        = string
  default     = "us-central1"
}

variable "repo_name" {
  description = "Artifact Registry repository name."
  type        = string
  default     = "iamjvp-agent"
}

variable "repo_format" {
  description = "Repository format (DOCKER, PYPI, etc.)."
  type        = string
  default     = "DOCKER"
}

variable "create_artifact_repo" {
  description = "Set false to skip Artifact Registry provisioning."
  type        = bool
  default     = true
}

variable "enable_service_account" {
  description = "Provision a dedicated agent service account."
  type        = bool
  default     = false
}

variable "service_account_id" {
  description = "Service account ID when enable_service_account is true."
  type        = string
  default     = "iamjvp-agent"
}

variable "service_account_display_name" {
  description = "Display name for the agent service account."
  type        = string
  default     = "IAMJVP Agent Runner"
}

variable "create_secret" {
  description = "Set true to create a baseline secret."
  type        = bool
  default     = false
}

variable "secret_id" {
  description = "Secret Manager identifier."
  type        = string
  default     = "iamjvp-agent-config"
}

variable "secret_labels" {
  description = "Labels applied to any created secrets."
  type        = map(string)
  default     = {}
}

variable "secret_replica_locations" {
  description = "Secret Manager replica regions."
  type        = list(string)
  default     = ["us-central1"]
}

variable "runtime_service_name" {
  description = "Display name for the runtime service placeholder."
  type        = string
  default     = "iamjvp-runtime"
}
