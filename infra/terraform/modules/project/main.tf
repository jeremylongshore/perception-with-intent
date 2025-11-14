data "google_project" "current" {
  project_id = var.project_id
}

# TODO(ask): Confirm whether this module should manage billing linkage or APIs.
