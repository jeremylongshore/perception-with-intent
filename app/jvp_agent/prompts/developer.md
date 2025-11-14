Implementation guide for extending JVP (IAMJVP):

- Annotate gaps with `// TODO(ask): <question>` and log the item in `STATUS.md`.
- When adding new tools, document them in `app/jvp_agent/tools/README.md` (create if needed) and update the AgentCard skills.
- Keep prompts concise; move lengthy guidance into `000-docs/`.
- Prefer Google ADK primitives (Agent, Runner, Tool classes) over third-party abstractions.
- Local strategy orchestration uses simple heuristics—extend `strategic_orchestrator.py` with lightweight analyzers before reaching for remote services.
- Use `scripts/deploy_agent_engine.sh` (or the GitHub Action) to ship updates to Vertex AI Agent Engine; confirm CLI flags with manuals.
- `memory.py` auto-detects advanced session features; revisit the defaults once the ADK release finalizes the context cache + compaction APIs.
- Build artifacts with `python scripts/package_agent.py` prior to Terraform or manual uploads so Vertex AI Agent Engine receives pickle/tarball/requirements bundles.
