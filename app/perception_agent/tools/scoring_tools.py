"""
Relevance Scoring Tools for Agent 3: Relevance Scorer
Scores articles based on keyword matching and ranking algorithms
"""

from typing import Dict, List, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


async def calculate_relevance_score(
    article: Dict[str, Any],
    keywords: List[str],
    boost_sources: List[str] = None
) -> Dict[str, Any]:
    """
    Calculate relevance score for an article.

    Scoring algorithm:
    - Title match: +3 points per keyword
    - Content match: +1 point per keyword
    - Source authority: +1-2 points
    - Recency: +1 point if < 24 hours

    Args:
        article: Article data (title, content, source, published)
        keywords: List of keywords to match against
        boost_sources: Optional list of authoritative sources

    Returns:
        Article with relevance_score and match details
    """
    logger.info(f"Scoring article: {article.get('title', '')[:50]}")

    score = 0
    matched_keywords = []
    match_locations = []

    title = article.get("title", "").lower()
    content = article.get("content", "").lower()

    # Title matches (worth more)
    for keyword in keywords:
        if keyword.lower() in title:
            score += 3
            matched_keywords.append(keyword)
            match_locations.append("title")

    # Content matches
    for keyword in keywords:
        if keyword.lower() in content and keyword not in matched_keywords:
            score += 1
            matched_keywords.append(keyword)
            match_locations.append("content")

    # Source authority bonus
    if boost_sources and article.get("source") in boost_sources:
        score += 2

    # Recency bonus
    published = article.get("published")
    if published:
        # TODO: Parse datetime and check if < 24 hours
        pass

    return {
        "article": article,
        "relevance_score": min(score, 10),  # Cap at 10
        "matched_keywords": list(set(matched_keywords)),
        "match_locations": list(set(match_locations))
    }


async def rank_articles(
    articles: List[Dict[str, Any]],
    keywords: List[str],
    top_n: int = 50
) -> List[Dict[str, Any]]:
    """
    Score and rank multiple articles.

    Args:
        articles: List of articles to score
        keywords: Keywords to match against
        top_n: Number of top articles to return

    Returns:
        Ranked list of top N articles
    """
    logger.info(f"Ranking {len(articles)} articles")

    scored_articles = []

    for article in articles:
        scored = await calculate_relevance_score(article, keywords)
        scored_articles.append(scored)

    # Sort by relevance_score descending
    ranked = sorted(scored_articles, key=lambda x: x["relevance_score"], reverse=True)

    return ranked[:top_n]


async def filter_by_threshold(
    articles: List[Dict[str, Any]],
    min_score: int = 5
) -> List[Dict[str, Any]]:
    """
    Filter articles by minimum relevance score.

    Args:
        articles: List of scored articles
        min_score: Minimum score to include

    Returns:
        Filtered list of articles
    """
    logger.info(f"Filtering articles with min_score >= {min_score}")

    return [a for a in articles if a.get("relevance_score", 0) >= min_score]
