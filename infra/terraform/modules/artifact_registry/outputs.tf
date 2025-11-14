output "repository_id" {
  description = "Full resource name of the Artifact Registry repository."
  value       = length(google_artifact_registry_repository.agent) > 0 ? google_artifact_registry_repository.agent[0].id : null
}

output "repository_url" {
  description = "Canonical repository URL."
  value = length(google_artifact_registry_repository.agent) > 0 ? format(
    "%s-docker.pkg.dev/%s/%s",
    var.region,
    var.project_id,
    var.repo_name,
  ) : null
}
