"""A2A integration helpers for the JVP (IAMJVP) commander agent."""

from __future__ import annotations

from typing import Any, Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import AgentSkill, Role, TaskState, TextPart
from a2a.utils import new_agent_text_message
from a2a.utils.errors import ServerError
from google.adk import Runner
from google.adk.agents import Agent as AdkAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import VertexAiMemoryBankService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from google.genai import types as genai_types
from vertexai.preview.reasoning_engines import A2aAgent
from vertexai.preview.reasoning_engines.templates.a2a import create_agent_card

from jvp_agent.agent import JVP_AGENT
from jvp_agent.config import settings
from jvp_agent.memory import runner_memory_kwargs


def build_agent_card() -> Any:
    """Create the AgentCard describing JVP's capabilities."""
    commander_skill = AgentSkill(
        id="command_router",
        name="Command Routing",
        description=(
            "Coordinate strategic tasks, surface follow-ups, and route commands to "
            "specialist tools or downstream agents."
        ),
        tags=["command", "coordination", "vertex-ai"],
        examples=[
            "Create a briefing for the latest Vertex AI Agent Engine update.",
            "Summarize outstanding TODO(ask) markers across the repo.",
            "Draft a rollout plan for enabling a Cloud Run runtime module.",
            "List the Terraform variables required for dev promotion.",
            "Produce a balanced strategic read-out using the local heuristics tool.",
        ],
        input_modes=["text/plain"],
        output_modes=["text/plain"],
    )
    return create_agent_card(
        agent_name="IAMJVP Commander",
        description="Baseline commander agent aligned with the latest Google ADK + A2A protocols.",
        skills=[commander_skill],
    )


class CommandAgentExecutor(AgentExecutor):
    """Bridge between the A2A protocol surface and the ADK agent runner."""

    def __init__(self, agent: AdkAgent | None = None) -> None:
        self._agent = agent or JVP_AGENT
        self._runner: Optional[Runner] = None

    def _ensure_runner(self) -> None:
        if self._runner is None:
            session_service = (
                VertexAiSessionService(
                    project=settings.project_id,
                    location=settings.location,
                    agent_engine_id=settings.agent_engine_id,
                )
                if settings.has_remote_agent_services
                else InMemorySessionService()
            )
            memory_service = (
                VertexAiMemoryBankService(
                    project=settings.project_id,
                    location=settings.location,
                    agent_engine_id=settings.agent_engine_id,
                )
                if settings.has_remote_agent_services
                else InMemoryMemoryService()
            )
            runner_kwargs = {
                "app_name": self._agent.name,
                "agent": self._agent,
                "artifact_service": InMemoryArtifactService(),
                "session_service": session_service,
                "memory_service": memory_service,
            }
            runner_kwargs.update(runner_memory_kwargs(Runner))
            self._runner = Runner(**runner_kwargs)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        self._ensure_runner()
        assert self._runner is not None

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        if not context.current_task:
            await updater.submit()

        await updater.start_work()

        try:
            session = await self._get_or_create_session(context.context_id)
            content = genai_types.Content(
                role=Role.user,
                parts=[genai_types.Part(text=context.get_user_input())],
            )

            async for event in self._runner.run_async(
                session_id=session.id,
                user_id=context.context_id or "user",
                new_message=content,
            ):
                if event.is_final_response():
                    answer = self._collect_text(event)
                    await updater.add_artifact(
                        [TextPart(text=answer)],
                        name="command_response",
                    )
                    await updater.complete()
                    break
        except Exception as exc:  # noqa: BLE001
            await updater.update_status(
                TaskState.failed,
                message=new_agent_text_message(f"Command execution failed: {exc!s}"),
            )
            raise

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise ServerError(new_agent_text_message("Cancellation not supported yet."))

    async def _get_or_create_session(self, session_id: str | None):
        assert self._runner is not None
        resolved_session_id = session_id or "default-session"
        session = await self._runner.session_service.get_session(
            app_name=self._runner.app_name,
            user_id=resolved_session_id,
            session_id=resolved_session_id,
        )
        if not session:
            session = await self._runner.session_service.create_session(
                app_name=self._runner.app_name,
                user_id=resolved_session_id,
                session_id=resolved_session_id,
            )
        return session

    @staticmethod
    def _collect_text(event: Any) -> str:
        parts = [
            part.text for part in event.content.parts if getattr(part, "text", None)
        ]
        return " ".join(parts) if parts else "No response generated."


def build_a2a_agent() -> A2aAgent:
    """Construct and set up the A2A agent wrapper."""
    card = build_agent_card()
    agent = A2aAgent(agent_card=card, agent_executor_builder=CommandAgentExecutor)
    agent.set_up()
    return agent
