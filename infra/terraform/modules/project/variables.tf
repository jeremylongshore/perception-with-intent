variable "project_id" {
  description = "ID of the existing Google Cloud project."
  type        = string
}

variable "billing_id" {
  description = "Billing account ID for auditing. // TODO(ask): Should this module enforce billing link?"
  type        = string
}
