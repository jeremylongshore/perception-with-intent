"""
Tools for Agent 3 (Relevance & Ranking).

These functions score articles against user topics using Gemini analysis
and filter by relevance thresholds.

Implementation details (Gemini API calls) will be added in later phases.
"""

from typing import Any, Dict, List


def score_article_relevance(
    article: Dict[str, Any], topics: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Stub: Score an article's relevance against all topics using Gemini.

    Args:
        article: Article dict with title, content, etc.
        topics: List of topic dicts with keywords and criteria.

    Returns:
        Scoring result with:
        - article_id
        - topic_scores: dict mapping topic_id -> relevance score (1-10)
        - matched_topics: list of topic IDs that matched
        - matched_keywords: list of keywords that triggered matches
        - overall_score: highest topic score
    """
    # TODO: implement Gemini API call for relevance scoring
    return {
        "article_id": article.get("url"),
        "topic_scores": {},
        "matched_topics": [],
        "matched_keywords": [],
        "overall_score": 0,
    }


def match_article_to_topics(
    article: Dict[str, Any], topics: List[Dict[str, Any]], threshold: int = 5
) -> List[str]:
    """
    Stub: Identify which topics match an article above threshold.

    Args:
        article: Article dict.
        topics: List of topics to check.
        threshold: Minimum relevance score to be considered a match.

    Returns:
        List of topic IDs that matched.
    """
    # TODO: implement topic matching logic
    return []


def calculate_importance(article: Dict[str, Any], topic_scores: Dict[str, int]) -> int:
    """
    Calculate overall importance score for an article.

    Args:
        article: Article dict.
        topic_scores: Dict mapping topic_id -> relevance score.

    Returns:
        Overall importance score (1-10).
    """
    if not topic_scores:
        return 0

    # Simple implementation: use highest topic score
    # TODO: enhance with factors like source authority, recency, sentiment
    return max(topic_scores.values())


def filter_by_threshold(
    articles: List[Dict[str, Any]], threshold: int = 5
) -> List[Dict[str, Any]]:
    """
    Filter articles below relevance threshold.

    Args:
        articles: List of scored articles.
        threshold: Minimum relevance score to keep.

    Returns:
        Filtered list of articles.
    """
    return [
        article
        for article in articles
        if article.get("relevance_score", 0) >= threshold
    ]


def rank_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort articles by importance/relevance score descending.

    Args:
        articles: List of scored articles.

    Returns:
        Sorted list of articles (highest score first).
    """
    return sorted(
        articles, key=lambda x: x.get("importance_score", 0), reverse=True
    )
