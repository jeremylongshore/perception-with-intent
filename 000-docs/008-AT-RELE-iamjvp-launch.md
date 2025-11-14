# IAMJVP Commander Launch Notes

**ID:** 008-AT-RELE-iamjvp-launch  
**Date:** 2025-11-17  
**Status:** Released  

## Summary

Established the initial IAMJVP commander scaffold aligned with Google’s most recent ADK + A2A rollout (Nov 2025). The repository now contains:

- Python-based ADK agent (`app/jvp_agent/agent.py`) with memory callback support.
- A2A bridge (`app/jvp_agent/a2a.py`) exposing the agent via the Vertex AI `A2aAgent` wrapper.
- Modular Terraform baseline under `infra/terraform/` with optional resource toggles.
- GitHub Pages landing page (`docs/index.md`) mirroring the README for public visibility.
- Unified CI pipeline running lint/format + Terraform init/fmt/validate.

## Highlights

- **Agent Definition:** Uses `google.adk.agents.Agent` with prompts sourced from `app/jvp_agent/prompts/`.
- **Memory Integration:** `PreloadMemoryTool` and `add_session_to_memory` callback persist sessions; remote `VertexAiSessionService`/`VertexAiMemoryBankService` activate when environment variables are set.
- **Knowledge Retrieval:** Added `vertex_ai_rag_search` tool backed by Vertex AI Search (App Builder) to provide short + long-term retrieval.
- **A2A Skill:** Command routing capability advertised via `AgentSkill` and `create_agent_card`.
- **Dev Experience:** `scripts/dev_run_adk.sh` launches the UVicorn dev server (`python -m app.main`).
- **Docs:** README + GitHub Pages include badges, architecture diagram, quickstart, and roadmap. `STATUS.md` tracks outstanding TODO(ask) items.

### Environment Configuration

Set the following variables to enable managed services and Vertex AI Search:

- `VERTEX_PROJECT_ID`
- `VERTEX_LOCATION`
- `VERTEX_AGENT_ENGINE_ID`
- `VERTEX_SEARCH_DATA_STORE_ID`

Without these values, IAMJVP falls back to in-memory session/memory services and the RAG tool returns a configuration warning.

## Next Steps

1. Confirm final Gemini model + safety policy from manuals and update `agent.yaml` + code comments.
2. Replace UVicorn stub with official ADK CLI command when the toolkit exposes an A2A-aware runner.
3. Extend `modules/agent_runtime` once runtime target (Cloud Run, API Gateway) is finalized.
4. Implement real tools and update AgentCard skill set to reflect production capabilities.
5. Add automated tests mirroring ADK starter suites once non-trivial behavior is introduced.
