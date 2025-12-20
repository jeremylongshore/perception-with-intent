"""
Tools for Agent 8 (Technology Desk Editor).

These functions curate and enhance the Technology section of daily briefs.
The Tech Editor is the first vertical section editor, demonstrating how
future editors (Business, Politics, etc.) will work.

Phase E2E: Implements production-ready tech section curation.
"""

from typing import Any, Dict, List
import logging
import json

logger = logging.getLogger(__name__)


def select_top_tech_articles(articles: List[Dict[str, Any]], max_articles: int = 5) -> List[Dict[str, Any]]:
    """
    Select the top technology articles from scored articles.

    Args:
        articles: List of scored articles with section tags
        max_articles: Maximum number of tech articles to select

    Returns:
        List of top tech articles sorted by relevance score
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_8",
        "operation": "select_top_tech_articles",
        "input_count": len(articles),
        "max_articles": max_articles
    }))

    # Filter for Tech section articles
    tech_articles = [a for a in articles if a.get("section") == "Tech"]

    # Sort by relevance score (descending)
    tech_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    # Take top N
    selected = tech_articles[:max_articles]

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_8",
        "operation": "select_top_tech_articles",
        "tech_article_count": len(tech_articles),
        "selected_count": len(selected)
    }))

    return selected


def propose_tech_headline(tech_articles: List[Dict[str, Any]]) -> str:
    """
    Propose a compelling headline for the Technology section.

    Analyzes the top tech articles and generates a headline that captures
    the main themes or most important development.

    Args:
        tech_articles: List of selected tech articles

    Returns:
        Proposed headline string
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_8",
        "operation": "propose_tech_headline",
        "article_count": len(tech_articles)
    }))

    if not tech_articles:
        return "Technology Update"

    # Analyze AI tags to find common themes
    all_tags = []
    for article in tech_articles:
        tags = article.get("ai_tags", [])
        all_tags.extend(tags)

    # Count tag frequency
    tag_counts = {}
    for tag in all_tags:
        tag_lower = tag.lower()
        tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1

    # Get most common themes
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    top_themes = [tag for tag, count in sorted_tags[:3]]

    # Build headline based on themes
    if "ai" in top_themes or "artificial intelligence" in top_themes:
        headline = "AI Developments Lead Technology News"
    elif "cloud" in top_themes or "kubernetes" in top_themes:
        headline = "Cloud Computing and Infrastructure Updates"
    elif "startup" in top_themes or "acquisition" in top_themes:
        headline = "Tech Industry M&A and Startup Activity"
    else:
        # Fallback: use highest-scored article title as inspiration
        top_article = tech_articles[0]
        title = top_article.get("title", "Technology Update")
        # Extract key phrase (simplified approach)
        if len(title) > 50:
            headline = f"Technology: {title[:47]}..."
        else:
            headline = f"Technology: {title}"

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_8",
        "operation": "propose_tech_headline",
        "headline": headline,
        "top_themes": top_themes
    }))

    return headline


def enhance_tech_section(section_data: Dict[str, Any], tech_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Enhance the Technology section with editor curation.

    Takes the basic Tech section from brief builder and enhances it with:
    - Curated article selection
    - Custom headline
    - Theme analysis

    Args:
        section_data: Original Tech section from brief builder
        tech_articles: Selected tech articles from editor

    Returns:
        Enhanced section dict
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_8",
        "operation": "enhance_tech_section",
        "original_article_count": len(section_data.get("top_articles", [])),
        "selected_article_count": len(tech_articles)
    }))

    # Propose headline
    headline = propose_tech_headline(tech_articles)

    # Build enhanced key points
    key_points = []
    for article in tech_articles[:5]:  # Top 5 for key points
        title = article.get("title", "Untitled")
        score = article.get("relevance_score", 0)
        tags = article.get("ai_tags", [])
        tag_str = f" [{', '.join(tags[:2])}]" if tags else ""
        key_point = f"• {title}{tag_str} (score: {score})"
        key_points.append(key_point)

    # Build article references
    article_refs = []
    for article in tech_articles:
        article_ref = {
            "title": article.get("title", "Untitled"),
            "url": article.get("url", ""),
            "source_id": article.get("source_id", ""),
            "relevance_score": article.get("relevance_score", 0),
            "ai_tags": article.get("ai_tags", [])
        }
        article_refs.append(article_ref)

    enhanced = {
        "section_name": "Technology",
        "editor_headline": headline,
        "key_points": key_points,
        "top_articles": article_refs,
        "meta": {
            "editor": "agent_8_tech_editor",
            "article_count": len(tech_articles),
            "curated": True
        }
    }

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_8",
        "operation": "enhance_tech_section",
        "headline": headline,
        "final_article_count": len(article_refs)
    }))

    return enhanced
