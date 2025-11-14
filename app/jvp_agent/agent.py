"""Core ADK agent definition for JVP (IAMJVP)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from jvp_agent.tools.echo_tool import echo_command
from jvp_agent.tools.rag_search import vertex_ai_rag_search
from jvp_agent.tools.strategic_orchestrator import orchestrate_strategy

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def _load_prompt(filename: str) -> str:
    """Load prompt text from the prompts directory."""
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8").strip()


async def add_session_to_memory(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Persist completed sessions using the configured memory service."""
    invocation_context = getattr(callback_context, "_invocation_context", None)
    if invocation_context and invocation_context.memory_service:
        await invocation_context.memory_service.add_session_to_memory(
            invocation_context.session
        )
    return None


JVP_AGENT = Agent(
    name="iamjvp-commander",
    model="gemini-1.5-pro",  # TODO(ask): confirm canonical model from manuals
    description="Baseline strategic command agent aligned with the latest ADK + A2A rollout.",
    instruction="\n\n".join(
        [
            _load_prompt("system.md"),
            "Developer context:",
            _load_prompt("developer.md"),
        ]
    ),
    tools=[
        echo_command,
        orchestrate_strategy,
        vertex_ai_rag_search,
        PreloadMemoryTool(),  # Aligns with memory guidance in user manuals
    ],
    after_agent_callback=add_session_to_memory,
)
