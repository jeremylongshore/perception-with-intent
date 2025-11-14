"""
Article Analysis Tools for Agent 4: Article Analyst
Generates summaries and extracts tags using Gemini AI
"""

from typing import Dict, List, Any
import logging
import httpx

logger = logging.getLogger(__name__)


async def generate_summary(article_text: str, max_sentences: int = 5) -> str:
    """
    Generate AI summary of article content.

    Calls LLMToolsMCP for Gemini-powered summarization.

    Args:
        article_text: Full article content
        max_sentences: Maximum sentences in summary (default 5)

    Returns:
        AI-generated summary
    """
    logger.info(f"Generating summary for article ({len(article_text)} chars)")

    # TODO: Call LLMToolsMCP
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "http://llm-tools-mcp:8080/mcp/tools/summarize",
    #         json={"text": article_text, "max_sentences": max_sentences}
    #     )
    #     return response.json()["summary"]

    return "AI-generated summary placeholder"


async def extract_tags(article_text: str, topics: List[str], max_tags: int = 4) -> List[str]:
    """
    Extract relevant tags from article.

    Uses Gemini to identify key themes and categorize content.

    Args:
        article_text: Full article content
        topics: Available topics to consider
        max_tags: Exactly how many tags to return

    Returns:
        List of exactly max_tags AI-selected tags
    """
    logger.info(f"Extracting {max_tags} tags from article")

    # TODO: Call LLMToolsMCP tag extraction

    return ["tag1", "tag2", "tag3", "tag4"][:max_tags]


async def score_importance(article: Dict[str, Any]) -> int:
    """
    Score article importance (1-10).

    Considers:
    - Content significance
    - Source credibility
    - Timeliness
    - Relevance to tracked topics

    Args:
        article: Article data with title, content, source

    Returns:
        Importance score 1-10
    """
    logger.info(f"Scoring importance: {article.get('title', '')[:50]}")

    score = 5  # Base score

    # Keyword boost
    important_keywords = ["breaking", "exclusive", "urgent", "major", "critical"]
    title = article.get("title", "").lower()

    for keyword in important_keywords:
        if keyword in title:
            score += 2
            break

    # Topic relevance boost
    matched_topics = len(article.get("matched_keywords", []))
    if matched_topics > 2:
        score += 1.5

    return min(int(score), 10)


async def analyze_batch(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze multiple articles in batch.

    Generates summaries, tags, and importance scores for all.

    Args:
        articles: List of articles to analyze

    Returns:
        List of analyzed articles with AI enhancements
    """
    logger.info(f"Batch analyzing {len(articles)} articles")

    analyzed = []

    for article in articles:
        summary = await generate_summary(article.get("content", ""))
        tags = await extract_tags(article.get("content", ""), [])
        importance = await score_importance(article)

        analyzed.append({
            "article_id": article.get("url", ""),  # Use URL as temp ID
            "title": article.get("title"),
            "summary": summary,
            "ai_tags": tags,
            "importance_score": importance,
            "url": article.get("url"),
            "source": article.get("source")
        })

    return analyzed
