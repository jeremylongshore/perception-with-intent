resource "google_service_account" "agent_runner" {
  count        = var.create_service_account ? 1 : 0
  project      = var.project_id
  account_id   = var.service_account_id
  display_name = var.service_account_display_name
  description  = "Service account for IAMJVP agent runtime."
}

# TODO(ask): Define IAM bindings once minimum runtime roles are approved.
