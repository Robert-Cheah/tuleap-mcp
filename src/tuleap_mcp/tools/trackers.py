from typing import List, Dict, Any, Optional
from ..client import TuleapClient


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

    return await client.get(endpoint)


async def update_artifact(
    client: TuleapClient,
    artifact_id: int,
    values: List[Dict[str, Any]],
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an artifact's fields or add a comment."""
    payload = {"values": values}
    if comment:
        payload["comment"] = {"body": comment}
    return await client.put(f"/artifacts/{artifact_id}", json=payload)
