"""Helpers for configuring advanced ADK memory features."""

from __future__ import annotations

import inspect
from typing import Any, Dict

# Newer ADK releases expose ContextCacheConfig / EventsCompactionConfig under
# google.adk.services. Fall back gracefully when running against older builds.
try:  # pragma: no cover - import path differs across ADK versions.
    from google.adk.services import ContextCacheConfig, EventsCompactionConfig
except ImportError:  # pragma: no cover
    ContextCacheConfig = None  # type: ignore[assignment]
    EventsCompactionConfig = None  # type: ignore[assignment]


# Default heuristics follow the Cloud Run memory tutorial guidance.
CONTEXT_CACHE_MIN_TOKENS = 500
CONTEXT_CACHE_TTL_SECONDS = 30 * 60
CONTEXT_CACHE_MAX_REUSE = 10

COMPACTION_INTERVAL = 5
COMPACTION_OVERLAP = 1


def runner_memory_kwargs(runner_cls: type) -> Dict[str, Any]:
    """
    Return keyword arguments for `google.adk.Runner` enabling context caching
    and event compaction when the installed ADK supports them.

    The signature inspection keeps the code compatible with earlier releases
    that have not yet shipped these knobs.
    """
    kwargs: Dict[str, Any] = {}

    runner_params = inspect.signature(runner_cls).parameters

    if (
        "context_cache_config" in runner_params
        and ContextCacheConfig is not None  # type: ignore[truthy-function]
    ):
        kwargs["context_cache_config"] = ContextCacheConfig(
            min_tokens=CONTEXT_CACHE_MIN_TOKENS,
            ttl_seconds=CONTEXT_CACHE_TTL_SECONDS,
            cache_intervals=CONTEXT_CACHE_MAX_REUSE,
        )

    if (
        "events_compaction_config" in runner_params
        and EventsCompactionConfig is not None  # type: ignore[truthy-function]
    ):
        kwargs["events_compaction_config"] = EventsCompactionConfig(
            compaction_interval=COMPACTION_INTERVAL,
            overlap_size=COMPACTION_OVERLAP,
        )

    return kwargs
