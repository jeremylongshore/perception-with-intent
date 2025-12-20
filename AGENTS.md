# Repository Guidelines

## Project Structure & Module Organization
- `app/jvp_agent/` houses the production agent: `agent.py` wires the ADK agent, `a2a.py` exposes the `CommandAgentExecutor` and AgentCard, `agent.yaml` sets runtime defaults, `prompts/` carries instruction templates, and `tools/` implements the echo and Vertex AI Search integrations.
- `app/jvp_agent/tools/strategic_orchestrator.py` adds a local risk/opportunity synthesiser using lightweight heuristics—extend it before reaching for remote services.
- `app/jvp_agent/memory.py` toggles context cache + compaction features when supported by the installed ADK.
- `scripts/package_agent.py` produces the pickle/tarball/requirements artifacts consumed by Terraform or manual Vertex AI Agent Engine deployments.
- `scripts/` provides local automation (formatting, dev server, helpers) referenced throughout the manuals.
- `infra/terraform/` contains reusable modules plus `envs/dev/` as the reference deployment wiring; run Terraform from that directory.
- `000-docs/` captures operator manuals (entry point `000-docs/USER-MANUALS.md`), while `docs/` holds the public GitHub Pages snapshot. `_archive/` stores legacy artifacts and migration notes.

## Build, Test, and Development Commands
- `./scripts/fmt_vet_lint.sh` installs pinned `black`/`ruff` versions and runs formatting + lint checks.
- `./scripts/dev_run_adk.sh` starts the ADK/A2A dev server (`python -m app.main`) for local agent runs.
- `terraform init -backend=false` and `terraform plan -var-file=terraform.tfvars.example` (run from `infra/terraform/envs/dev/`) validate IaC changes without touching remote state.
- Export `VERTEX_PROJECT_ID`, `VERTEX_LOCATION`, `VERTEX_AGENT_ENGINE_ID`, and `VERTEX_SEARCH_DATA_STORE_ID` to enable Vertex-managed sessions and RAG search; without them the agent falls back to in-memory services.
- The strategy orchestrator relies solely on in-repo heuristics—no additional credentials or services required.
- Use `./scripts/deploy_agent_engine.sh` for manual deployments; trigger `.github/workflows/deploy-agent-engine.yml` once Workload Identity Federation is configured.
- Run `python scripts/package_agent.py` before Terraform/GCS uploads so the build artifacts exist.

## Coding Style & Naming Conventions
- Use 4-space indentation, snake_case for functions/modules, PascalCase for classes, and stay ASCII unless a manual dictates otherwise.
- Keep prompts terse; longer guidance lives in `000-docs/`. Flag ambiguities with `// TODO(ask)` plus a manual reference.

## Testing Guidelines
- Pytest scaffolding is not yet shipped. Exercise new behavior through the ADK CLI or integration harness documented in the manuals.
- When adding tests, mirror the `app/` layout under `tests/`, keep CI free of external credentials, and name test files `test_<feature>.py`.

## Commit & Pull Request Guidelines
- Commits follow `type: short imperative` (e.g., `feat: add vertex rag tool`). Batch related changes and avoid mixing Terraform, docs, and runtime tweaks without explanation.
- Pull requests must state the motivation, call out operator actions, and reference relevant manuals or `STATUS.md` updates. Run `./scripts/fmt_vet_lint.sh` before submitting.

## Security & Configuration Tips
- Never commit credentials or service account keys; prefer Workload Identity Federation for GitHub Actions when redeploying pipelines.
- Document noteworthy config shifts in `STATUS.md` and the relevant manual section so operators can track environment expectations.

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
