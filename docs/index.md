# 🤖 IAM JVP Base — Vertex AI Agent Engine Commander

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4.svg)](https://cloud.google.com/vertex-ai/agents/docs/adk/overview)
[![Vertex AI Agent Engine](https://img.shields.io/badge/Vertex%20AI-Agent%20Engine-4285F4.svg)](https://cloud.google.com/vertex-ai/generative-ai/docs/agents)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-844FBA.svg)](https://registry.terraform.io/providers/hashicorp/google/latest)

**JVP (IAMJVP) is a freshly built strategic commander agent template aligned with Google’s ADK + A2A update from six days ago.**

---

## Snapshot

- ADK agent (`app/jvp_agent/agent.py`) + prompts + Vertex AI memory callback.
- A2A bridge (`app/jvp_agent/a2a.py`) exposing the commander skill via `A2aAgent` (uses Vertex AI Sessions + Memory Bank if configured).
- Vertex AI Search tool (`app/jvp_agent/tools/rag_search.py`) for knowledge-grounded results.
- Strategy orchestrator (`app/jvp_agent/tools/strategic_orchestrator.py`) that balances simple risk/opportunity heuristics for quick planning.
- Terraform baseline (`infra/terraform/`) covering project, IAM, Artifact Registry, secrets, and runtime placeholder modules.
- Tooling scripts + CI for formatting, linting, and Terraform validation.
- Deployment helpers (`scripts/deploy_agent_engine.sh`, `.github/workflows/deploy-agent-engine.yml`) to push the agent to Vertex AI Agent Engine via CLI or GitHub Actions.
- Memory helpers (`app/jvp_agent/memory.py`) dynamically enable context caching + compaction when the ADK release supports the new Vertex AI features.
- Packaging script (`scripts/package_agent.py`) builds the pickle/tarball/requirements triple required by Vertex AI Agent Engine deployments.
- Documentation hub (`000-docs/`) and STATUS tracker for outstanding TODO(ask) items.

---

## Architecture Diagram

```mermaid
graph TD
  subgraph App
    Agent[agent.py]
    Prompts(prompts/)
    Echo(tools/echo_tool.py)
  end

  subgraph Terraform
    Dev(envs/dev/main.tf)
    ProjectMod(modules/project)
    IAMMod(modules/iam)
    SecretsMod(modules/secrets)
    ArtifactMod(modules/artifact_registry)
    RuntimeMod(modules/agent_runtime)
  end

  subgraph Ops
    Scripts(scripts/*.sh)
    CI(.github/workflows/ci.yml)
    Manuals(000-docs/USER-MANUALS.md)
  end

  Agent --> Prompts
  Agent --> Echo
  Dev --> ProjectMod
  Dev --> IAMMod
  Dev --> SecretsMod
  Dev --> ArtifactMod
  Dev --> RuntimeMod
  Scripts --> Agent
  Scripts --> Dev
  CI --> Agent
  CI --> Dev
  Manuals --> Agent
```

---

## Quick Links

- [Repository README](../README.md)
- [User Manuals Index](../000-docs/USER-MANUALS.md)
- [Launch Notes](../000-docs/008-AT-RELE-iamjvp-launch.md)
- [Status & TODO(ask)](../STATUS.md)

Fork it, replace the TODO markers as you verify manual updates, and extend the commander into a full Vertex AI deployment.
