# Workload Identity Federation (WIF) Setup Guide

This guide explains how to set up keyless authentication from GitHub Actions to Google Cloud using Workload Identity Federation.

## Why WIF?

Workload Identity Federation eliminates the need for service account keys (JSON files) by using OIDC tokens from GitHub. This is:
- ✅ More secure (no long-lived credentials)
- ✅ Easier to manage (no key rotation)
- ✅ Required for production (Bob's Brain enforcement)

## Prerequisites

- GCP project: `perception-with-intent`
- GitHub repository with Actions enabled
- `gcloud` CLI installed and authenticated

## Step 1: Enable Required APIs

```bash
gcloud services enable \
  iamcredentials.googleapis.com \
  cloudresourcemanager.googleapis.com \
  sts.googleapis.com \
  --project=perception-with-intent
```

## Step 2: Create Workload Identity Pool

```bash
# Create the pool
gcloud iam workload-identity-pools create github-pool \
  --project=perception-with-intent \
  --location=global \
  --display-name="GitHub Actions Pool"

# Verify creation
gcloud iam workload-identity-pools describe github-pool \
  --project=perception-with-intent \
  --location=global
```

## Step 3: Create Workload Identity Provider

```bash
# Get your project number
PROJECT_NUMBER=$(gcloud projects describe perception-with-intent --format="value(projectNumber)")

# Create the provider
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --project=perception-with-intent \
  --location=global \
  --workload-identity-pool=github-pool \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# Get the provider name (you'll need this for GitHub Actions)
echo "projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/providers/github-provider"
```

## Step 4: Create Service Account

```bash
# Create service account for deployments
gcloud iam service-accounts create perception-deployer \
  --project=perception-with-intent \
  --display-name="Perception Deployer"

# Grant necessary roles
gcloud projects add-iam-policy-binding perception-with-intent \
  --member="serviceAccount:perception-deployer@perception-with-intent.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding perception-with-intent \
  --member="serviceAccount:perception-deployer@perception-with-intent.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding perception-with-intent \
  --member="serviceAccount:perception-deployer@perception-with-intent.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding perception-with-intent \
  --member="serviceAccount:perception-deployer@perception-with-intent.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding perception-with-intent \
  --member="serviceAccount:perception-deployer@perception-with-intent.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

## Step 5: Bind Service Account to GitHub

Replace `[your-github-username]` with your actual GitHub username:

```bash
# Allow GitHub Actions from your repo to impersonate the service account
gcloud iam service-accounts add-iam-policy-binding \
  perception-deployer@perception-with-intent.iam.gserviceaccount.com \
  --project=perception-with-intent \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/[your-github-username]/perception"
```

## Step 6: Update GitHub Actions

Update `.github/workflows/deploy.yml` with your values:

```yaml
env:
  PROJECT_ID: perception-with-intent
  WORKLOAD_IDENTITY_PROVIDER: projects/[PROJECT_NUMBER]/locations/global/workloadIdentityPools/github-pool/providers/github-provider
  SERVICE_ACCOUNT: perception-deployer@perception-with-intent.iam.gserviceaccount.com
```

## Step 7: Test the Setup

Push to main branch and check GitHub Actions:

```bash
git add .
git commit -m "test: verify WIF authentication"
git push origin main
```

Check the Actions tab in GitHub. The workflow should authenticate without any service account keys.

## Troubleshooting

### "Permission denied" errors

Check service account roles:
```bash
gcloud projects get-iam-policy perception-with-intent \
  --flatten="bindings[].members" \
  --filter="bindings.members:perception-deployer@perception-with-intent.iam.gserviceaccount.com"
```

### "Workload identity pool not found"

Verify the pool exists:
```bash
gcloud iam workload-identity-pools list --location=global --project=perception-with-intent
```

### "Failed to impersonate service account"

Check the binding:
```bash
gcloud iam service-accounts get-iam-policy \
  perception-deployer@perception-with-intent.iam.gserviceaccount.com \
  --project=perception-with-intent
```

## Security Best Practices

1. **Limit repository access**: Only bind WIF to specific repositories
2. **Principle of least privilege**: Grant only required IAM roles
3. **Regular audits**: Review WIF bindings quarterly
4. **Monitor usage**: Enable Cloud Audit Logs for service account impersonation

## References

- [Google Cloud WIF Documentation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Bob's Brain WIF Setup](https://github.com/jeremylongshore/bobs-brain/blob/main/docs/wif-setup.md)

---

**Status:** ✅ WIF setup complete
**Last Updated:** 2025-11-14
