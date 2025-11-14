# JVP Tooling Overview

| Tool | Module | Purpose | Configuration |
|------|--------|---------|---------------|
| `echo_command` | `echo_tool.py` | Baseline proof-of-life command that returns the structured payload. | None |
| `orchestrate_strategy` | `strategic_orchestrator.py` | Balances risk and opportunity insights using local heuristics. | None; deterministic in-repo logic. |
| `vertex_ai_rag_search` | `rag_search.py` | Queries Vertex AI Search for knowledge-grounded snippets. | Requires Vertex Search datastore (`VERTEX_PROJECT_ID`, `VERTEX_LOCATION`, `VERTEX_SEARCH_DATA_STORE_ID`). |

Add new tools here and keep entries synced with `agent.yaml` plus the AgentCard skill catalogue.
