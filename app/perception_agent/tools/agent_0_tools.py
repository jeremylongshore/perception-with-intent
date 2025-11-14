"""
Tools for Agent 0 (Perception Orchestrator).

These functions are invoked by the orchestration agent to:
- Start and update ingestion run records.
- Coordinate calls to sub-agents (via ADK / Agent Engine mechanisms).
- Aggregate results for logging and status reporting.

Implementation will be filled in subsequent phases.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

# NOTE: In later phases, this module will:
# - Use the Firestore client to write /ingestion_runs/{runId}.
# - Use ADK's mechanisms to call sub-agents.
# - Emit OpenTelemetry spans and metrics.


def start_ingestion_run(trigger: str) -> Dict[str, Any]:
    """
    Create an ingestion run descriptor.

    Args:
        trigger: A string describing what kicked off the run
                 (e.g., "scheduled", "manual_dashboard").

    Returns:
        A dict with at least:
        - run_id: string
        - started_at: ISO8601 timestamp
        - trigger: original trigger string
    """
    # TODO: replace with Firestore-backed ID generator.
    run_id = f"run_{int(datetime.now(tz=timezone.utc).timestamp())}"

    return {
        "run_id": run_id,
        "started_at": datetime.now(tz=timezone.utc).isoformat(),
        "trigger": trigger,
        "status": "running",
    }


def finalize_ingestion_run(
    run_id: str, success: bool, stats: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Produce a final ingestion run status payload.

    Args:
        run_id: ID of the ingestion run.
        success: Whether the run completed successfully.
        stats: Optional dictionary of counts/metrics
               (e.g., articles_ingested, articles_selected, alerts_triggered).

    Returns:
        A dict representing the final ingestion run state.
    """
    return {
        "run_id": run_id,
        "finished_at": datetime.now(tz=timezone.utc).isoformat(),
        "status": "success" if success else "failed",
        "stats": stats or {},
    }


def build_daily_ingestion_plan(user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Stub: Build a high-level plan for a daily ingestion run.

    This will eventually:
    - Read sources from Firestore.
    - Read topics for the given user (or default topics).
    - Decide which sub-agents to invoke and in what order.

    Args:
        user_id: Optional user whose topics should be used.

    Returns:
        A dict describing the plan (for debugging/telemetry).
    """
    # TODO: implement Firestore reads and real planning.
    return {
        "user_id": user_id,
        "steps": [
            "fetch_sources",
            "harvest_articles",
            "rank_articles",
            "write_brief",
            "check_alerts",
            "validate",
            "store",
        ],
    }
