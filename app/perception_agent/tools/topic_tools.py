"""
Topic Management Tools for Agent 1: Topic Manager
Interacts with Firestore to manage topics and keywords
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


async def fetch_active_topics() -> Dict[str, List[Dict[str, Any]]]:
    """
    Fetch all active topics from Firestore.

    Connects to Firestore collection: topics_to_monitor
    Filters for active=true topics

    Returns:
        List of active topics with keywords and metadata
    """
    logger.info("Fetching active topics from Firestore")

    # TODO: Replace with actual Firestore client call via StorageMCP
    # For now, return mock data structure

    return {
        "topics": [
            {
                "topic_id": "sample_topic_1",
                "keywords": ["example", "keyword"],
                "category": "tech",
                "active": True
            }
        ]
    }


async def get_keywords_by_category(category: str) -> List[str]:
    """
    Get all keywords for a specific category.

    Args:
        category: Category to filter (e.g., 'sports', 'tech', 'business')

    Returns:
        List of keywords for that category
    """
    logger.info(f"Fetching keywords for category: {category}")

    # TODO: Implement Firestore query via StorageMCP

    return ["keyword1", "keyword2", "keyword3"]


async def update_topic_status(topic_id: str, active: bool) -> Dict[str, Any]:
    """
    Activate or deactivate a topic.

    Args:
        topic_id: Unique identifier for topic
        active: True to activate, False to deactivate

    Returns:
        Update confirmation
    """
    logger.info(f"Updating topic {topic_id} status to active={active}")

    # TODO: Implement Firestore update via StorageMCP

    return {
        "status": "updated",
        "topic_id": topic_id,
        "active": active
    }


async def get_topic_metadata(topic_id: str) -> Dict[str, Any]:
    """
    Get full metadata for a specific topic.

    Args:
        topic_id: Unique identifier for topic

    Returns:
        Complete topic document
    """
    logger.info(f"Fetching metadata for topic: {topic_id}")

    # TODO: Implement Firestore document fetch via StorageMCP

    return {
        "topic_id": topic_id,
        "keywords": [],
        "category": "unknown",
        "created_at": None,
        "updated_at": None
    }
