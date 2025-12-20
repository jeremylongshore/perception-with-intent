#!/usr/bin/env python3
"""
Perception With Intent - Dev Ingestion Runner

Runs a single ingestion cycle locally for testing the E2E pipeline.

Usage:
    python scripts/run_ingestion_once.py [--user-id USER_ID] [--trigger TRIGGER]

Requirements:
    - MCP service running on http://localhost:8080 (or set MCP_BASE_URL)
    - Virtual environment activated
    - Firestore emulator (optional, will use production if not set)

Phase E2E: Development script for manual testing of the complete ingestion flow.
"""

import asyncio
import sys
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime, timezone

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from perception_agent.tools.agent_0_tools import run_daily_ingestion

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # JSON logs
)
logger = logging.getLogger(__name__)


async def main():
    """Run a single ingestion cycle."""
    parser = argparse.ArgumentParser(
        description="Run a single Perception ingestion cycle for testing"
    )
    parser.add_argument(
        "--user-id",
        default="system",
        help="User ID to run ingestion for (default: system)"
    )
    parser.add_argument(
        "--trigger",
        default="manual_dev",
        help="Trigger type for this run (default: manual_dev)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Starting dev ingestion run",
        "user_id": args.user_id,
        "trigger": args.trigger,
        "timestamp": datetime.now(tz=timezone.utc).isoformat()
    }))

    try:
        # Run the ingestion pipeline
        result = await run_daily_ingestion(
            user_id=args.user_id,
            trigger=args.trigger
        )

        # Print summary
        print("\n" + "=" * 60)
        print("INGESTION RUN COMPLETE")
        print("=" * 60)
        print(f"Run ID: {result.get('run_id')}")
        print(f"Status: {result.get('status')}")
        print(f"Brief ID: {result.get('brief_id')}")
        print("\nStats:")
        stats = result.get('stats', {})
        for key, value in stats.items():
            print(f"  {key}: {value}")

        errors = result.get('errors', [])
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")

        print("=" * 60)

        logger.info(json.dumps({
            "severity": "INFO",
            "message": "Dev ingestion run completed",
            "result": result
        }))

        # Exit code based on status
        sys.exit(0 if result.get('status') == 'success' else 1)

    except Exception as e:
        logger.error(json.dumps({
            "severity": "ERROR",
            "message": "Dev ingestion run failed",
            "error": str(e)
        }))
        print(f"\n❌ FATAL ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
