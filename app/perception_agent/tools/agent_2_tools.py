"""
Tools for Agent 2 (Topic Manager).

These functions handle CRUD operations for user topics and provide
active topic lists for relevance scoring.

Implementation details (Firestore CRUD) will be added in later phases.
"""

from typing import Any, Dict, List, Optional


def get_active_topics(user_id: str) -> List[Dict[str, Any]]:
    """
    Stub: Retrieve active topics for a user.

    Args:
        user_id: User ID whose topics to retrieve.

    Returns:
        List of topic dicts with:
        - topic_id
        - name
        - keywords (list of strings)
        - category
        - threshold (relevance score minimum)
        - active (boolean)
    """
    # TODO: implement Firestore query: /users/{user_id}/topics where active == true
    return []


def create_topic(user_id: str, topic_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stub: Create a new topic for a user.

    Args:
        user_id: User ID who owns this topic.
        topic_data: Topic fields (name, keywords, category, etc.)

    Returns:
        Created topic dict with generated topic_id.
    """
    # TODO: implement Firestore write to /users/{user_id}/topics/{topic_id}
    return {
        "topic_id": "generated_id",
        **topic_data,
    }


def update_topic(
    user_id: str, topic_id: str, updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Stub: Update an existing topic.

    Args:
        user_id: User ID who owns the topic.
        topic_id: Topic ID to update.
        updates: Fields to update.

    Returns:
        Updated topic dict.
    """
    # TODO: implement Firestore update
    return {
        "topic_id": topic_id,
        **updates,
    }


def delete_topic(user_id: str, topic_id: str) -> bool:
    """
    Stub: Delete a topic.

    Args:
        user_id: User ID who owns the topic.
        topic_id: Topic ID to delete.

    Returns:
        True if deleted successfully.
    """
    # TODO: implement Firestore delete
    return True


def validate_topic_structure(topic_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a topic structure has required fields.

    Args:
        topic_data: Topic dict to validate.

    Returns:
        Validation result with:
        - valid (boolean)
        - errors (list of error messages)
    """
    errors: List[str] = []

    if not topic_data.get("name"):
        errors.append("Topic name is required")

    if not topic_data.get("keywords"):
        errors.append("At least one keyword is required")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }
