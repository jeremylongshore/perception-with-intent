variable "project_id" {
  description = "Target Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Region for the Artifact Registry repository."
  type        = string
  default     = "us-central1"
}

variable "repo_name" {
  description = "Repository name for container images."
  type        = string
  default     = "iamjvp-agent"
}

variable "format" {
  description = "Artifact Registry format to use."
  type        = string
  default     = "DOCKER"
}

variable "create_repository" {
  description = "Set false to skip repository creation (e.g., if managed elsewhere)."
  type        = bool
  default     = true
}
