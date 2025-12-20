"""
Tools for Agent 1 (Source Harvester).

These functions fetch articles from configured news sources via MCP tools.

Phase 5: Real MCP integration with fetch_rss_feed endpoint.
"""

from typing import Any, Dict, List, Optional
import os
import csv
import httpx
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# MCP service base URL (configurable via environment)
# Local dev: http://localhost:8080
# Production: https://perception-mcp-<hash>-uc.a.run.app (set via Agent Engine runtime config)
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8080")


def load_sources_from_csv() -> List[Dict[str, Any]]:
    """
    Load enabled sources from data/initial_feeds.csv.

    In Phase 6+, this will be replaced with Firestore queries.

    Returns:
        List of source dicts with fields:
        - source_id
        - name
        - type (rss|api|web)
        - url
        - category
        - enabled
    """
    csv_path = Path(__file__).parent.parent.parent.parent / "data" / "initial_feeds.csv"

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_1",
        "operation": "load_sources_from_csv",
        "csv_path": str(csv_path)
    }))

    sources = []
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('enabled', '').lower() == 'true':
                    sources.append({
                        'source_id': row['source_id'],
                        'name': row['name'],
                        'type': row['type'],
                        'url': row['url'],
                        'category': row['category'],
                        'enabled': True
                    })

        logger.info(json.dumps({
            "severity": "INFO",
            "tool": "agent_1",
            "operation": "load_sources_from_csv",
            "sources_loaded": len(sources)
        }))

        return sources
    except FileNotFoundError:
        logger.error(json.dumps({
            "severity": "ERROR",
            "tool": "agent_1",
            "operation": "load_sources_from_csv",
            "error": f"CSV file not found: {csv_path}"
        }))
        return []
    except Exception as e:
        logger.error(json.dumps({
            "severity": "ERROR",
            "tool": "agent_1",
            "operation": "load_sources_from_csv",
            "error": str(e)
        }))
        return []


def load_sources_from_firestore() -> List[Dict[str, Any]]:
    """
    TODO Phase 6: Load enabled sources from Firestore /sources collection.

    This will replace load_sources_from_csv in production.

    Returns:
        List of source dicts.
    """
    # TODO: implement Firestore read
    # from google.cloud import firestore
    # db = firestore.Client()
    # sources_ref = db.collection('sources')
    # query = sources_ref.where('enabled', '==', True)
    # return [doc.to_dict() for doc in query.stream()]
    return []


async def fetch_rss(feed_url: str, time_window_hours: int = 24, max_items: int = 50, request_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Call the MCP fetch_rss_feed endpoint to get articles from an RSS feed.

    Args:
        feed_url: RSS feed URL
        time_window_hours: Only return articles from last N hours
        max_items: Maximum articles to return
        request_id: Optional tracking ID

    Returns:
        List of normalized article dicts
    """
    endpoint = f"{MCP_BASE_URL}/mcp/tools/fetch_rss_feed"

    payload = {
        "feed_url": feed_url,
        "time_window_hours": time_window_hours,
        "max_items": max_items,
        "request_id": request_id
    }

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_1",
        "operation": "fetch_rss",
        "feed_url": feed_url,
        "mcp_endpoint": endpoint
    }))

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

            logger.info(json.dumps({
                "severity": "INFO",
                "tool": "agent_1",
                "operation": "fetch_rss",
                "feed_url": feed_url,
                "article_count": data.get('article_count', 0)
            }))

            return data.get('articles', [])

    except httpx.HTTPStatusError as e:
        logger.error(json.dumps({
            "severity": "ERROR",
            "tool": "agent_1",
            "operation": "fetch_rss",
            "feed_url": feed_url,
            "http_status": e.response.status_code,
            "error": e.response.text
        }))
        return []
    except Exception as e:
        logger.error(json.dumps({
            "severity": "ERROR",
            "tool": "agent_1",
            "operation": "fetch_rss",
            "feed_url": feed_url,
            "error": str(e)
        }))
        return []


def normalize_article(raw: Dict[str, Any], source_id: str, category: Optional[str] = None) -> Dict[str, Any]:
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
        - summary
        - content
        - content_snippet
        - author
        - categories (list of tags)
    """
    return {
        "title": raw.get("title", "Untitled"),
        "url": raw.get("url", ""),
        "source_id": source_id,
        "category": category,
        "published_at": raw.get("published_at"),
        "summary": raw.get("summary"),
        "content": raw.get("raw_content") or raw.get("summary") or raw.get("content_snippet"),
        "content_snippet": raw.get("content_snippet"),
        "author": raw.get("author"),
        "categories": raw.get("categories", [])
    }


async def harvest_all_sources(time_window_hours: int = 24, max_items_per_source: int = 50) -> Dict[str, Any]:
    """
    High-level harvesting process.

    Loads all enabled sources and fetches articles from each one.

    Args:
        time_window_hours: Only fetch articles from last N hours
        max_items_per_source: Max articles per source

    Returns:
        A dict with:
        - articles: List[Dict[str, Any]] of normalized article objects
        - source_count: number of sources processed
        - total_fetched: total articles fetched before normalization
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_1",
        "operation": "harvest_all_sources",
        "time_window_hours": time_window_hours,
        "max_items_per_source": max_items_per_source
    }))

    # Load sources from CSV (Phase 5)
    # TODO Phase 6: Replace with load_sources_from_firestore()
    sources = load_sources_from_csv()

    if not sources:
        logger.warning(json.dumps({
            "severity": "WARNING",
            "tool": "agent_1",
            "operation": "harvest_all_sources",
            "message": "No enabled sources found"
        }))
        return {
            "articles": [],
            "source_count": 0,
            "total_fetched": 0
        }

    # Fetch from each source
    all_articles = []
    total_fetched = 0

    for source in sources:
        source_type = source.get('type')
        source_id = source.get('source_id')
        source_url = source.get('url')
        category = source.get('category')

        if source_type == 'rss':
            # Fetch RSS feed via MCP
            raw_articles = await fetch_rss(
                feed_url=source_url,
                time_window_hours=time_window_hours,
                max_items=max_items_per_source,
                request_id=f"harvest_{source_id}"
            )

            # Normalize each article
            for raw in raw_articles:
                normalized = normalize_article(raw, source_id, category)
                all_articles.append(normalized)

            total_fetched += len(raw_articles)

        # TODO Phase 6: Handle 'api' and 'web' source types
        # elif source_type == 'api':
        #     raw_articles = await fetch_api_feed(...)
        # elif source_type == 'web':
        #     raw_articles = await fetch_webpage(...)

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_1",
        "operation": "harvest_all_sources",
        "source_count": len(sources),
        "total_fetched": total_fetched,
        "articles_after_normalization": len(all_articles)
    }))

    return {
        "articles": all_articles,
        "source_count": len(sources),
        "total_fetched": total_fetched
    }
