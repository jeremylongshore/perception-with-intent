"""
Tools for Agent 3 (Relevance & Ranking).

These functions score articles against user topics using heuristic analysis
and filter by relevance thresholds.

Phase E2E: Implements production-ready scoring with keyword matching + basic heuristics.
"""

from typing import Any, Dict, List
import logging
import json

logger = logging.getLogger(__name__)


def score_articles(articles: List[Dict[str, Any]], topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Score all articles against topics using keyword matching and heuristics.

    Args:
        articles: List of article dicts from Agent 1
        topics: List of topic dicts from Agent 2

    Returns:
        List of scored article dicts with:
        - relevance_score (1-10)
        - ai_tags (list of strings)
        - section (str, e.g., "Tech", "Business", "General")
        - matched_topics (list of topic_ids)
    """
    scored_articles = []

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_3",
        "operation": "score_articles",
        "article_count": len(articles),
        "topic_count": len(topics)
    }))

    for article in articles:
        score_result = _score_single_article(article, topics)

        # Merge score results into article
        scored_article = {**article, **score_result}
        scored_articles.append(scored_article)

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_3",
        "operation": "score_articles",
        "scored_count": len(scored_articles),
        "avg_score": sum(a.get("relevance_score", 0) for a in scored_articles) / len(scored_articles) if scored_articles else 0
    }))

    return scored_articles


def _score_single_article(article: Dict[str, Any], topics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Score a single article against all topics.

    Returns dict with:
    - relevance_score: 1-10
    - ai_tags: list of matched keywords
    - section: inferred section name
    - matched_topics: list of topic IDs
    """
    title = article.get("title", "").lower()
    content = article.get("content", "") or article.get("content_snippet", "") or article.get("summary", "")
    content_lower = content.lower() if content else ""
    category = article.get("category", "").lower()

    matched_topics = []
    matched_keywords = []
    topic_scores = {}

    # Match against topics
    for topic in topics:
        topic_id = topic.get("topic_id", "")
        keywords = topic.get("keywords", [])

        matches = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title:
                matches += 3  # Title match worth more
                matched_keywords.append(keyword)
            elif keyword_lower in content_lower:
                matches += 1
                matched_keywords.append(keyword)

        if matches > 0:
            # Score 1-10 based on matches
            topic_score = min(10, matches + 3)  # At least 4 if any match
            topic_scores[topic_id] = topic_score
            matched_topics.append(topic_id)

    # Overall relevance score
    relevance_score = max(topic_scores.values()) if topic_scores else 5  # Default 5 if no topic match

    # Infer section based on category or content
    section = _infer_section(category, title, content_lower, matched_keywords)

    # Generate AI tags from matched keywords
    ai_tags = list(set(matched_keywords[:10]))  # Unique, max 10

    return {
        "relevance_score": relevance_score,
        "ai_tags": ai_tags,
        "section": section,
        "matched_topics": matched_topics
    }


def _infer_section(category: str, title: str, content: str, keywords: List[str]) -> str:
    """
    Infer section name based on category and content.

    Returns one of: Tech, Business, Politics, Sports, General
    """
    # Tech signals
    tech_signals = ["ai", "tech", "software", "hardware", "startup", "cloud", "data", "cyber", "crypto"]
    if any(sig in category for sig in ["tech", "ai", "software"]):
        return "Tech"
    if any(sig in title.lower() or sig in content for sig in tech_signals):
        return "Tech"

    # Business signals
    business_signals = ["business", "ceo", "earnings", "revenue", "market", "acquisition", "ipo", "investment"]
    if any(sig in category for sig in ["business", "finance", "market"]):
        return "Business"
    if any(sig in title.lower() or sig in content for sig in business_signals):
        return "Business"

    # Politics signals
    politics_signals = ["politics", "government", "congress", "senate", "legislation", "regulation", "policy"]
    if any(sig in category for sig in ["politics", "government"]):
        return "Politics"
    if any(sig in title.lower() or sig in content for sig in politics_signals):
        return "Politics"

    # Sports signals
    sports_signals = ["sports", "nfl", "nba", "mlb", "soccer", "football", "basketball"]
    if any(sig in category for sig in ["sports"]):
        return "Sports"
    if any(sig in title.lower() or sig in content for sig in sports_signals):
        return "Sports"

    return "General"


def filter_top_articles(scored_articles: List[Dict[str, Any]], max_per_topic: int = 10, min_score: int = 5) -> List[Dict[str, Any]]:
    """
    Filter scored articles to keep only top articles.

    Args:
        scored_articles: List of scored articles
        max_per_topic: Max articles to keep overall
        min_score: Minimum relevance score to keep

    Returns:
        Filtered list of top articles sorted by relevance_score descending
    """
    # Filter by minimum score
    filtered = [a for a in scored_articles if a.get("relevance_score", 0) >= min_score]

    # Sort by relevance score descending
    filtered.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    # Take top N
    top_articles = filtered[:max_per_topic * 5]  # max_per_topic * 5 for multiple topics

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_3",
        "operation": "filter_top_articles",
        "input_count": len(scored_articles),
        "output_count": len(top_articles),
        "min_score": min_score
    }))

    return top_articles
