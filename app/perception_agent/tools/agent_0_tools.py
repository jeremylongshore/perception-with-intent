"""
Tools for Agent 0 (Perception Orchestrator).

These functions are invoked by the orchestration agent to:
- Start and update ingestion run records.
- Coordinate calls to sub-agents (via ADK / Agent Engine mechanisms).
- Aggregate results for logging and status reporting.

Phase E2E: Implements production-ready orchestration with full pipeline coordination.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging
import json
import asyncio

# Import agent tools
from .agent_1_tools import harvest_all_sources
from .agent_2_tools import get_active_topics
from .agent_3_tools import score_articles, filter_top_articles
from .agent_4_tools import build_brief_payload
from .agent_6_tools import validate_articles, validate_brief
from .agent_7_tools import store_articles, store_brief, update_ingestion_run

logger = logging.getLogger(__name__)


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


async def run_daily_ingestion(user_id: Optional[str] = None, trigger: str = "scheduled") -> Dict[str, Any]:
    """
    Execute the complete daily ingestion pipeline.

    This orchestrates the full E2E flow:
    1. Start ingestion run (Agent 0)
    2. Get active topics (Agent 2)
    3. Harvest all sources (Agent 1)
    4. Score articles (Agent 3)
    5. Filter top articles (Agent 3)
    6. Build brief payload (Agent 4)
    7. Validate articles and brief (Agent 6)
    8. Store articles and brief (Agent 7)
    9. Update ingestion run with final status (Agent 7)

    Args:
        user_id: Optional user ID (defaults to system user)
        trigger: What triggered this run (scheduled, manual, etc.)

    Returns:
        Complete ingestion result with:
        - run_id: Ingestion run ID
        - status: success or failed
        - stats: Counts and metrics
        - brief_id: Generated brief ID
        - errors: Any errors encountered
    """
    # Default to system user if not specified
    if user_id is None:
        user_id = "system"

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_0",
        "operation": "run_daily_ingestion",
        "trigger": trigger,
        "user_id": user_id
    }))

    # Step 1: Start ingestion run
    run_info = start_ingestion_run(trigger)
    run_id = run_info["run_id"]

    errors = []
    stats = {
        "articles_harvested": 0,
        "articles_scored": 0,
        "articles_selected": 0,
        "articles_stored": 0,
        "brief_id": None
    }

    try:
        # Step 2: Get active topics (Agent 2)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "get_active_topics",
            "run_id": run_id
        }))

        topics = get_active_topics(user_id)

        # If no topics, use default topics for E2E testing
        if not topics:
            logger.warning(json.dumps({
                "severity": "WARNING",
                "tool": "agent_0",
                "operation": "run_daily_ingestion",
                "message": "No topics found, using default test topics",
                "run_id": run_id
            }))
            # Default test topics for E2E
            topics = [
                {
                    "topic_id": "tech-ai",
                    "name": "AI & Machine Learning",
                    "keywords": ["ai", "artificial intelligence", "machine learning", "llm", "gpt", "gemini"],
                    "category": "technology",
                    "active": True
                },
                {
                    "topic_id": "tech-cloud",
                    "name": "Cloud Computing",
                    "keywords": ["cloud", "aws", "gcp", "azure", "kubernetes", "serverless"],
                    "category": "technology",
                    "active": True
                }
            ]

        # Step 3: Harvest all sources (Agent 1)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "harvest_all_sources",
            "run_id": run_id
        }))

        harvest_result = await harvest_all_sources(time_window_hours=24, max_items_per_source=50)
        articles = harvest_result.get("articles", [])
        stats["articles_harvested"] = len(articles)

        if not articles:
            logger.warning(json.dumps({
                "severity": "WARNING",
                "tool": "agent_0",
                "operation": "run_daily_ingestion",
                "message": "No articles harvested",
                "run_id": run_id
            }))
            # Update run as success with no articles
            update_ingestion_run(run_id, "success", stats)
            return {
                "run_id": run_id,
                "status": "success",
                "stats": stats,
                "brief_id": None,
                "errors": []
            }

        # Step 4: Score articles (Agent 3)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "score_articles",
            "run_id": run_id,
            "article_count": len(articles)
        }))

        scored_articles = score_articles(articles, topics)
        stats["articles_scored"] = len(scored_articles)

        # Step 5: Filter top articles (Agent 3)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "filter_top_articles",
            "run_id": run_id
        }))

        top_articles = filter_top_articles(scored_articles, max_per_topic=10, min_score=5)
        stats["articles_selected"] = len(top_articles)

        # Step 6: Build brief payload (Agent 4)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "build_brief_payload",
            "run_id": run_id
        }))

        brief = build_brief_payload(top_articles, run_id=run_id)
        stats["brief_id"] = brief.get("brief_id")

        # Step 7: Validate articles and brief (Agent 6)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "validate",
            "run_id": run_id
        }))

        articles_validation = validate_articles(top_articles)
        if not articles_validation["valid"]:
            errors.extend(articles_validation["errors"])
            logger.error(json.dumps({
                "severity": "ERROR",
                "tool": "agent_0",
                "operation": "run_daily_ingestion",
                "step": "validate_articles",
                "errors": articles_validation["errors"],
                "run_id": run_id
            }))

        brief_validation = validate_brief(brief)
        if not brief_validation["valid"]:
            errors.extend(brief_validation["errors"])
            logger.error(json.dumps({
                "severity": "ERROR",
                "tool": "agent_0",
                "operation": "run_daily_ingestion",
                "step": "validate_brief",
                "errors": brief_validation["errors"],
                "run_id": run_id
            }))

        # If validation failed, stop here
        if errors:
            logger.error(json.dumps({
                "severity": "ERROR",
                "tool": "agent_0",
                "operation": "run_daily_ingestion",
                "message": "Validation failed, stopping pipeline",
                "run_id": run_id,
                "error_count": len(errors)
            }))
            update_ingestion_run(run_id, "failed", stats)
            return {
                "run_id": run_id,
                "status": "failed",
                "stats": stats,
                "brief_id": None,
                "errors": errors
            }

        # Step 8: Store articles and brief (Agent 7)
        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "store_articles",
            "run_id": run_id
        }))

        storage_result = store_articles(top_articles)
        stats["articles_stored"] = storage_result.get("stored_count", 0)
        if storage_result.get("errors"):
            errors.extend(storage_result["errors"])

        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "store_brief",
            "run_id": run_id
        }))

        brief_storage_result = store_brief(brief)
        if brief_storage_result.get("status") != "stored":
            error_msg = brief_storage_result.get("error", "Brief storage failed")
            errors.append(error_msg)

        # Step 9: Update ingestion run with final status (Agent 7)
        final_status = "success" if not errors else "failed"

        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "step": "finalize",
            "run_id": run_id,
            "status": final_status
        }))

        update_ingestion_run(run_id, final_status, stats)

        return {
            "run_id": run_id,
            "status": final_status,
            "stats": stats,
            "brief_id": stats["brief_id"],
            "errors": errors
        }

    except Exception as e:
        error_msg = f"Pipeline failed: {str(e)}"
        errors.append(error_msg)

        logger.error(json.dumps({
            "severity": "ERROR",
            "tool": "agent_0",
            "operation": "run_daily_ingestion",
            "error": error_msg,
            "run_id": run_id
        }))

        # Try to update run status even if pipeline failed
        try:
            update_ingestion_run(run_id, "failed", stats)
        except Exception:
            pass  # Best effort

        return {
            "run_id": run_id,
            "status": "failed",
            "stats": stats,
            "brief_id": None,
            "errors": errors
        }
