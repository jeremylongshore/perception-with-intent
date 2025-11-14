output "service_account_email" {
  description = "Email of the created service account, if provisioned."
  value       = length(google_service_account.agent_runner) > 0 ? google_service_account.agent_runner[0].email : null
}

output "service_account_id" {
  description = "Resource ID of the service account."
  value       = length(google_service_account.agent_runner) > 0 ? google_service_account.agent_runner[0].name : null
}
