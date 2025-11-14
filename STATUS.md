# Status

## Current State

- Repository repurposed for IAM JVP Base with ADK commander implementation (`app/jvp_agent/agent.py`, `a2a.py`, prompts, tools).
- Terraform baseline established under `infra/terraform/` with modular structure and `envs/dev/` wiring.
- Legacy GitHub workflows archived into `_archive/github-workflows/` with NOTE.
- CI pipeline (`.github/workflows/ci.yml`) performs Python formatting checks, Terraform init/fmt/validate, and placeholder ADK validation.
- Scripts added for repo sanity (`scripts/repo_repurpose_check.sh`), ADK dev runner stub, and lint/format execution.
- Documentation refreshed: new `README.md`, GitHub Pages snapshot in `docs/index.md`, `000-docs/README.md`, `000-docs/USER-MANUALS.md`, and updated `AGENTS.md`.
- Strategy orchestration helper `app/jvp_agent/tools/strategic_orchestrator.py` blends local risk/opportunity heuristics to keep planning deterministic.
- Memory helper `app/jvp_agent/memory.py` auto-enables context caching + compaction when the ADK release exposes those controls.
- Packaging + deploy tooling staged: `scripts/package_agent.py`, `scripts/deploy_agent_engine.sh`, and `.github/workflows/deploy-agent-engine.yml`.
- Deployment path added: `scripts/deploy_agent_engine.sh` and `.github/workflows/deploy-agent-engine.yml` wrap the ADK CLI for pushing to Vertex AI Agent Engine.

## Outstanding TODO(ask)

- Confirm Gemini model selection and safety policy for `app/jvp_agent/agent.yaml`.
- Determine official ADK CLI command for `scripts/dev_run_adk.sh` (replace uvicorn stub).
- Decide whether to provision Artifact Registry / Secret Manager / IAM resources by default (toggle variables exist).
- Define runtime target (Cloud Run, etc.) for `modules/agent_runtime`.
- Address `.venv` directory lingering at repo root (consider deleting or documenting).
- Replace placeholder ADK YAML validation step in CI with official tooling.
- Flesh out AgentCard skills once additional tools or sub-agents are defined.
- Document required Vertex AI Search datastore setup (current tool warns if unconfigured).
- Calibrate heuristic keywords/weights in `strategic_orchestrator.py` against upcoming manuals.
- Confirm ADK CLI package/command used by `scripts/deploy_agent_engine.sh` and GitHub workflow (`google-adk-cli` placeholder).
- Verify ADK version exposes `ContextCacheConfig` / `EventsCompactionConfig`; update defaults or fallbacks once manuals publish concrete guidance.
- Flesh out Terraform flow to upload `build/` artifacts (currently placeholder in docs) once packaging process is validated end-to-end.

## Next Steps

1. Review manuals in `000-docs/USER-MANUALS.md` and align TODO(ask) items.
2. Populate tests directory once additional functionality lands.
3. Stand up remote Terraform backend configuration (`backend.tf`).
