variable "project_id" {
  description = "Target Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Primary region for the runtime."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name of the runtime service."
  type        = string
  default     = "iamjvp-runtime"
}
