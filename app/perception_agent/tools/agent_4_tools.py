"""
Tools for Agent 4 (Brief Writer).

These functions generate executive daily briefs from top-ranked articles,
creating summaries, highlights, and strategic insights.

Implementation details (Gemini API for summarization) will be added in later phases.
"""

from typing import Any, Dict, List
from datetime import date


def generate_executive_summary(articles: List[Dict[str, Any]]) -> str:
    """
    Stub: Generate a concise 1-2 sentence executive summary.

    Args:
        articles: List of top-ranked articles.

    Returns:
        Executive summary string.
    """
    # TODO: implement Gemini API call for summary generation
    return "No articles available for summary."


def extract_highlights(articles: List[Dict[str, Any]], max_highlights: int = 7) -> List[str]:
    """
    Stub: Extract 3-7 key highlights from articles.

    Args:
        articles: List of top-ranked articles.
        max_highlights: Maximum number of highlights to extract.

    Returns:
        List of highlight strings.
    """
    # TODO: implement Gemini API call to extract key points
    return []


def analyze_strategic_implications(
    articles: List[Dict[str, Any]], topics: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Stub: Analyze strategic implications per topic.

    Args:
        articles: List of articles.
        topics: List of topics to analyze.

    Returns:
        Dict mapping topic_id -> strategic implications string.
    """
    # TODO: implement Gemini API call for strategic analysis
    return {}


def calculate_brief_metrics(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate metrics for the brief.

    Args:
        articles: List of articles included in brief.

    Returns:
        Metrics dict with:
        - article_count
        - top_sources: dict of source_id -> count
        - main_topics: list of most frequent topics
    """
    metrics = {
        "article_count": len(articles),
        "top_sources": {},
        "main_topics": [],
    }

    # Count sources
    for article in articles:
        source_id = article.get("source_id")
        if source_id:
            metrics["top_sources"][source_id] = (
                metrics["top_sources"].get(source_id, 0) + 1
            )

    # TODO: extract main topics from article topics

    return metrics


def generate_brief(
    articles: List[Dict[str, Any]],
    topics: List[Dict[str, Any]],
    brief_date: str | None = None,
) -> Dict[str, Any]:
    """
    Stub: Generate complete daily brief.

    Args:
        articles: Top-ranked articles.
        topics: Active topics.
        brief_date: Date for brief (YYYY-MM-DD), defaults to today.

    Returns:
        Complete brief dict with:
        - date
        - executive_summary
        - highlights
        - strategic_implications
        - metrics
    """
    if brief_date is None:
        brief_date = date.today().isoformat()

    return {
        "date": brief_date,
        "executive_summary": generate_executive_summary(articles),
        "highlights": extract_highlights(articles),
        "strategic_implications": analyze_strategic_implications(articles, topics),
        "metrics": calculate_brief_metrics(articles),
    }
