# IAMJVP Terraform Baseline

This directory contains the minimal Terraform stack for the IAM JVP Base agent.
Follow the User Manuals in `000-docs` for deeper guidance.

## Structure

- `modules/` — Reusable building blocks (project, IAM, Artifact Registry, secrets, runtime placeholder).
- `envs/dev/` — Example environment wiring the modules together.

## Prerequisites

- Terraform `>= 1.6.0`
- Google Cloud SDK (`gcloud`) configured with the target project
- Appropriate permissions to read project metadata and create resources (Artifact Registry, Secret Manager, IAM)

## Usage (Dev)

```bash
cd infra/terraform/envs/dev
terraform init -backend=false
terraform plan -var-file=terraform.tfvars.example
```

Set `-backend=false` until you configure remote state (`backend.tf.example`).

## Variables

See `variables.tf` for required inputs. Key items:

- `project_id` (string) — existing GCP project
- `billing_id` (string) — captured for auditing // TODO(ask): confirm enforcement
- `region` (string) — defaults to `us-central1`
- Feature flags: `create_artifact_repo`, `enable_service_account`, `create_secret`

Adjust `terraform.tfvars.example` and copy to `terraform.tfvars` before applying.

## Remote State

When ready, copy `backend.tf.example` to `backend.tf` and fill in your Terraform Cloud or GCS backend configuration.

## Next Steps

- Define runtime resources in `modules/agent_runtime` once the hosting platform (Cloud Run, GKE, etc.) is chosen.
- Extend IAM bindings in `modules/iam` per security review.
- Document any deviations from manuals using `// TODO(ask)` comments and update `STATUS.md`.
