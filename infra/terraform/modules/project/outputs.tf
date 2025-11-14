output "project_id" {
  description = "Project ID passed into the module."
  value       = var.project_id
}

output "project_number" {
  description = "Numeric project identifier."
  value       = data.google_project.current.number
}

output "project_name" {
  description = "Display name of the project."
  value       = data.google_project.current.name
}
