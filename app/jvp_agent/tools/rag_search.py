"""Vertex AI Search (RAG) integration tool for IAMJVP."""

from __future__ import annotations

from typing import Any, Dict, List

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError
from google.cloud import discoveryengine_v1beta as discovery

from jvp_agent.config import settings


def vertex_ai_rag_search(query: str, page_size: int = 5) -> Dict[str, Any]:
    """
    Query Vertex AI Search for knowledge-grounded answers.

    Args:
        query: Natural language query to search over indexed content.
        page_size: Number of results to return (default 5).

    Returns:
        Dict containing matched documents with snippets.
    """
    if not settings.has_vertex_search:
        return {
            "status": "unconfigured",
            "message": (
                "Vertex AI Search datastore is not configured. "
                "Set VERTEX_SEARCH_DATA_STORE_ID to enable RAG search."
            ),
        }

    serving_config = settings.serving_config_path
    if not serving_config:
        return {
            "status": "error",
            "message": "Unable to compute serving config path for Vertex AI Search.",
        }

    client = discovery.SearchServiceClient(
        client_options=ClientOptions(api_endpoint=f"{settings.location}-discoveryengine.googleapis.com")
    )

    request = discovery.SearchRequest(
        serving_config=serving_config,
        query=query,
        page_size=page_size,
    )

    try:
        response = client.search(request=request)
    except GoogleAPIError as exc:
        return {
            "status": "error",
            "message": f"Vertex AI Search request failed: {exc!s}",
        }

    results: List[Dict[str, Any]] = []
    for result in response:
        document = result.document
        snippets = [
            snippet.snippet for snippet in result.document.derived_struct_data.get("snippets", [])
        ]
        results.append(
            {
                "id": document.id,
                "title": document.struct_data.get("title") if document.struct_data else None,
                "uri": document.struct_data.get("link") if document.struct_data else None,
                "snippets": snippets,
            }
        )

    return {
        "status": "success",
        "query": query,
        "results": results,
    }
