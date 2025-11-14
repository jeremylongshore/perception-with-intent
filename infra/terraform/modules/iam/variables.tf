variable "project_id" {
  description = "Target Google Cloud project ID."
  type        = string
}

variable "create_service_account" {
  description = "Set true to provision the IAMJVP runtime service account."
  type        = bool
  default     = false
}

variable "service_account_id" {
  description = "Service account ID (without domain)."
  type        = string
  default     = "iamjvp-agent"
}

variable "service_account_display_name" {
  description = "Friendly display name for the service account."
  type        = string
  default     = "IAMJVP Agent Runner"
}
