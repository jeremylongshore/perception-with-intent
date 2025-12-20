"""
Tools for Agent 6 (Validator).

These functions validate data quality, check schemas, and detect duplicates
before allowing storage to Firestore.

Phase E2E: Implements production-ready validation with schema checking.
"""

from typing import Any, Dict, List
import hashlib
import logging
import json

logger = logging.getLogger(__name__)


def validate_article_schema(article: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate an article has required fields with correct types.

    Args:
        article: Article dict to validate.

    Returns:
        Validation result with:
        - valid (boolean)
        - errors (list of error messages)
    """
    errors: List[str] = []
    required_fields = ["title", "url", "source_id"]

    for field in required_fields:
        if field not in article:
            errors.append(f"Missing required field: {field}")

    if "url" in article and not isinstance(article["url"], str):
        errors.append("Field 'url' must be a string")

    return {"valid": len(errors) == 0, "errors": errors}


def detect_duplicates(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Stub: Detect duplicate articles by URL hash.

    Args:
        articles: List of articles to check.

    Returns:
        List of duplicate article dicts with:
        - url
        - existing_id (if found in Firestore)
    """
    # TODO: implement Firestore query to check for existing URLs
    return []


def verify_data_quality(article: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify data quality checks.

    Args:
        article: Article dict to check.

    Returns:
        Quality check result with:
        - quality_score (0-10)
        - issues (list of quality issues found)
    """
    issues: List[str] = []
    score = 10

    # Check content length
    content = article.get("content", "")
    if len(content) < 50:
        issues.append("Content too short (< 50 characters)")
        score -= 3

    # Check title length
    title = article.get("title", "")
    if len(title) < 10:
        issues.append("Title too short (< 10 characters)")
        score -= 2

    # TODO: Add more quality checks:
    # - Encoding validation
    # - HTML sanitization
    # - URL validation

    return {"quality_score": max(0, score), "issues": issues}


def validate_brief_structure(brief: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate brief has all required fields.

    Args:
        brief: Brief dict to validate.

    Returns:
        Validation result with:
        - valid (boolean)
        - errors (list of error messages)
    """
    errors: List[str] = []
    required_fields = ["date", "executive_summary", "highlights"]

    for field in required_fields:
        if field not in brief:
            errors.append(f"Missing required field: {field}")

    if "highlights" in brief and not isinstance(brief["highlights"], list):
        errors.append("Field 'highlights' must be a list")

    return {"valid": len(errors) == 0, "errors": errors}


def generate_url_hash(url: str) -> str:
    """
    Generate a hash of a URL for duplicate detection.

    Args:
        url: URL to hash.

    Returns:
        SHA256 hash of the URL.
    """
    return hashlib.sha256(url.encode()).hexdigest()


def validate_articles(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate a list of articles.

    Args:
        articles: List of article dicts to validate

    Returns:
        Validation result with:
        - valid (bool): True if all articles pass validation
        - errors (list): List of error messages
        - valid_count (int): Number of valid articles
        - invalid_count (int): Number of invalid articles
    """
    errors = []
    valid_count = 0
    invalid_count = 0

    for i, article in enumerate(articles):
        result = validate_article_schema(article)
        if result["valid"]:
            valid_count += 1
        else:
            invalid_count += 1
            for error in result["errors"]:
                errors.append(f"Article {i}: {error}")

    is_valid = invalid_count == 0

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_6",
        "operation": "validate_articles",
        "total_count": len(articles),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "is_valid": is_valid
    }))

    return {
        "valid": is_valid,
        "errors": errors,
        "valid_count": valid_count,
        "invalid_count": invalid_count
    }


def validate_brief(brief: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a brief payload.

    Args:
        brief: Brief dict to validate

    Returns:
        Validation result with:
        - valid (bool): True if brief passes validation
        - errors (list): List of error messages
    """
    errors = []
    required_fields = ["brief_id", "date", "headline", "sections"]

    # Check required fields
    for field in required_fields:
        if field not in brief:
            errors.append(f"Missing required field: {field}")

    # Validate sections is a list
    if "sections" in brief:
        if not isinstance(brief["sections"], list):
            errors.append("Field 'sections' must be a list")
        elif len(brief["sections"]) == 0:
            errors.append("Brief must have at least one section")
        else:
            # Validate each section
            for i, section in enumerate(brief["sections"]):
                if not isinstance(section, dict):
                    errors.append(f"Section {i} must be a dict")
                    continue

                if "section_name" not in section:
                    errors.append(f"Section {i}: Missing 'section_name'")
                if "key_points" not in section:
                    errors.append(f"Section {i}: Missing 'key_points'")
                if "top_articles" not in section:
                    errors.append(f"Section {i}: Missing 'top_articles'")

    is_valid = len(errors) == 0

    logger.info(json.dumps({
        "severity": "INFO",
        "tool": "agent_6",
        "operation": "validate_brief",
        "brief_id": brief.get("brief_id"),
        "is_valid": is_valid,
        "error_count": len(errors)
    }))

    return {
        "valid": is_valid,
        "errors": errors
    }
