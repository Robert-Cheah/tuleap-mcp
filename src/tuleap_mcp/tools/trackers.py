from typing import List, Dict, Any, Optional
from ..client import TuleapClient

def _slim_artifact(artifact: Dict[str, Any]) -> Dict[str, Any]:
    """Return only essential fields from an artifact."""
    return {
        "id": artifact.get("id"),
        "title": artifact.get("title"),
        "status": artifact.get("status"),
        "assignees": [a.get("display_name") for a in artifact.get("assignees", [])],
        "last_modified_date": artifact.get("last_modified_date"),
    }

async def get_artifact_details(
    client: TuleapClient, artifact_id: int
) -> Dict[str, Any]:
    """Get details of a specific artifact."""
    return await client.get(f"/artifacts/{artifact_id}")


async def search_artifacts(
    client: TuleapClient, tracker_id: int, filters: Optional[dict] = None
) -> List[Dict[str, Any]]:
    """Search for artifacts in a tracker, with optional filters as a dict."""
    import json

    endpoint = f"/trackers/{tracker_id}/artifacts"
    if filters:
        query_json = json.dumps(filters)
        endpoint = f"{endpoint}?query={query_json}"

    results = await client.get_paginated(endpoint)
    return [_slim_artifact(a) for a in results]


async def update_artifact(
    client: TuleapClient,
    artifact_id: int,
    values: List[Dict[str, Any]],
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an artifact's fields or add a comment."""
    payload = {"values": values}
    if comment:
        payload["comment"] = {"body": comment, "format": "text"}
    result = await client.put(f"/artifacts/{artifact_id}", json=payload)
    return result if result is not None else {"status": "success", "artifact_id": artifact_id}

async def create_artifact(
    client: TuleapClient, tracker_id: int, values: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a new artifact in a tracker."""
    payload = {"tracker": {"id": tracker_id}, "values": values}
    return await client.post("/artifacts", json=payload)