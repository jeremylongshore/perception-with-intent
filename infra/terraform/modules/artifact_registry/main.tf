resource "google_artifact_registry_repository" "agent" {
  count         = var.create_repository ? 1 : 0
  project       = var.project_id
  location      = var.region
  repository_id = var.repo_name
  format        = var.format
  description   = "Artifact Registry repository for IAMJVP agent images."

  docker_config {
    immutable_tags = true
  }
}

# TODO(ask): Confirm additional lifecycle policies (retention, cleanup) once requirements solidify.
