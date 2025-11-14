"""
Tools for Agent 1 (Source Harvester).

These helpers will:
- Load enabled sources from Firestore.
- Call MCP tools to fetch content (RSS, APIs, web pages).
- Normalize results into a standard article structure.

Implementation details (Firestore + MCP HTTP calls) will be added in later phases.
"""

from typing import Any, Dict, List


def load_sources_from_config() -> List[Dict[str, Any]]:
    """
    Stub: Load enabled sources from Firestore.

    In later phases, this will:
    - Query the /sources collection.
    - Filter for enabled == true.
    - Return a list of source dicts with fields:
      - source_id
      - name
      - type (rss|api|web)
      - url
      - category
    """
    # TODO: implement Firestore read.
    return []


def normalize_article(
    raw: Dict[str, Any], source_id: str, category: str | None = None
) -> Dict[str, Any]:
    """
    Normalize a raw article payload from an MCP tool into a standard structure.

    Args:
        raw: Raw article dict from fetch_rss_feed, fetch_api_feed, or fetch_webpage.
        source_id: The ID of the source that produced this article.
        category: Optional category label for the source.

    Returns:
        A normalized article dict with common fields:
        - title
        - url
        - source_id
        - category
        - published_at (ISO8601, or None if unknown)
        - content (best-effort text content)
    """
    # TODO: refine this once MCP tool response schemas are finalized.
    return {
        "title": raw.get("title"),
        "url": raw.get("url"),
        "source_id": source_id,
        "category": category,
        "published_at": raw.get("published_at"),
        "content": raw.get("content") or raw.get("summary"),
    }


def harvest_all_sources() -> Dict[str, Any]:
    """
    High-level stub for the harvesting process.

    This is the function the agent will conceptually call to:
    - Load all enabled sources.
    - Dispatch the right MCP fetch tool per source type.
    - Normalize and aggregate all articles.

    Returns:
        A dict with:
        - articles: List[Dict[str, Any]] of normalized article objects.
        - source_count: number of sources processed.
    """
    # TODO: implement:
    # - Call load_sources_from_config()
    # - For each source, call appropriate MCP tool.
    # - Normalize and aggregate.
    sources: List[Dict[str, Any]] = []
    articles: List[Dict[str, Any]] = []

    return {
        "articles": articles,
        "source_count": len(sources),
    }
