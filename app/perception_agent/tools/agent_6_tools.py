"""
Tools for Agent 6 (Validator).

These functions validate data quality, check schemas, and detect duplicates
before allowing storage to Firestore.

Implementation details (Firestore duplicate checking) will be added in later phases.
"""

from typing import Any, Dict, List
import hashlib


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
