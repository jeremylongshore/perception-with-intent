"""
Data Validation Tools for Agent 6: Validator
Ensures data quality before storage
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)


async def validate_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a single article for required fields and format.

    Args:
        article: Article data to validate

    Returns:
        Validation result with errors/warnings
    """
    errors = []
    warnings = []

    # Required fields
    required = ["title", "url", "source", "summary", "ai_tags"]
    for field in required:
        if not article.get(field):
            errors.append(f"Missing required field: {field}")

    # URL format
    url = article.get("url", "")
    if url and not re.match(r"^https?://", url):
        errors.append(f"Invalid URL format: {url}")

    # Tags count
    tags = article.get("ai_tags", [])
    if len(tags) != 4:
        warnings.append(f"Expected 4 tags, got {len(tags)}")

    # Summary length
    summary = article.get("summary", "")
    if summary and len(summary.split(". ")) < 3:
        warnings.append("Summary less than 3 sentences")

    # Importance score range
    score = article.get("importance_score")
    if score and (score < 1 or score > 10):
        errors.append(f"Importance score out of range (1-10): {score}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


async def validate_batch(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate multiple articles and remove duplicates.

    Args:
        articles: List of articles to validate

    Returns:
        Validation report with stats
    """
    logger.info(f"Validating batch of {len(articles)} articles")

    valid_articles = []
    rejected = []
    all_errors = []
    all_warnings = []

    # Track URLs to detect duplicates
    seen_urls = set()
    duplicate_count = 0

    for article in articles:
        # Check for duplicate URL
        url = article.get("url")
        if url in seen_urls:
            duplicate_count += 1
            rejected.append({"article": article, "reason": "duplicate_url"})
            continue

        seen_urls.add(url)

        # Validate article
        validation = await validate_article(article)

        if validation["valid"]:
            valid_articles.append(article)
        else:
            rejected.append({"article": article, "reason": validation["errors"]})

        all_errors.extend(validation["errors"])
        all_warnings.extend(validation["warnings"])

    return {
        "valid": len(rejected) == 0,
        "validated_items": len(valid_articles),
        "rejected_items": len(rejected),
        "rejection_reasons": {
            "duplicate_urls": duplicate_count,
            "validation_errors": len(rejected) - duplicate_count
        },
        "errors": all_errors,
        "warnings": all_warnings,
        "valid_articles": valid_articles
    }


async def validate_daily_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate daily summary document.

    Args:
        summary: Daily summary to validate

    Returns:
        Validation result
    """
    errors = []
    warnings = []

    # Required fields
    required = ["date", "executive_summary", "highlights", "metrics"]
    for field in required:
        if not summary.get(field):
            errors.append(f"Missing required field: {field}")

    # Date format
    date_str = summary.get("date")
    if date_str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            errors.append(f"Invalid date format: {date_str}")

    # Highlights count
    highlights = summary.get("highlights", [])
    if len(highlights) < 3:
        warnings.append(f"Only {len(highlights)} highlights (recommend 5-7)")

    # Executive summary length
    exec_summary = summary.get("executive_summary", "")
    if exec_summary and len(exec_summary.split()) < 100:
        warnings.append("Executive summary may be too short")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


async def check_data_quality(data: Any, data_type: str = "article") -> bool:
    """
    Quick quality check for any data type.

    Args:
        data: Data to check
        data_type: Type of data (article, summary, etc.)

    Returns:
        True if passes quality check
    """
    logger.info(f"Quality checking {data_type}")

    if data_type == "article":
        result = await validate_article(data)
    elif data_type == "summary":
        result = await validate_daily_summary(data)
    else:
        return True

    return result["valid"]
