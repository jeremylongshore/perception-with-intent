"""Configuration helpers for IAMJVP agent integrations."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


def _env(*keys: str) -> Optional[str]:
    for key in keys:
        value = os.getenv(key)
        if value:
            return value
    return None


@dataclass(frozen=True)
class Settings:
    """Environment-driven settings for cloud integrations."""

    project_id: Optional[str] = _env("VERTEX_PROJECT_ID", "GCP_PROJECT_ID", "PROJECT_ID")
    location: Optional[str] = _env("VERTEX_LOCATION", "REGION", "LOCATION")
    agent_engine_id: Optional[str] = _env("VERTEX_AGENT_ENGINE_ID", "AGENT_ENGINE_ID")
    search_data_store_id: Optional[str] = _env(
        "VERTEX_SEARCH_DATA_STORE_ID", "SEARCH_DATA_STORE_ID"
    )

    @property
    def has_remote_agent_services(self) -> bool:
        return bool(self.project_id and self.location and self.agent_engine_id)

    @property
    def has_vertex_search(self) -> bool:
        return bool(self.project_id and self.location and self.search_data_store_id)

    @property
    def serving_config_path(self) -> Optional[str]:
        if not self.has_vertex_search:
            return None
        return (
            f"projects/{self.project_id}/locations/{self.location}/collections/"
            f"default_collection/dataStores/{self.search_data_store_id}"
            "/servingConfigs/default_serving_config"
        )

settings = Settings()
