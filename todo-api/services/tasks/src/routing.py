from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class Request:
    method: str
    path: str
    path_params: Dict[str, str]
    body_json: Dict[str, Any]

def parse_http_api_event(event: dict) -> Request:
    rc = event.get("requestContext", {})
    http = rc.get("http", {})
    method = (http.get("method") or "").upper()
    path = event.get("rawPath") or ""
    path_params = event.get("pathParameters") or {}

    body = event.get("body")
    if isinstance(body, str) and body.strip():
        import json
        body_json = json.loads(body)
    elif isinstance(body, dict):
        body_json = body
    else:
        body_json = {}

    return Request(method=method, path=path, path_params=path_params, body_json=body_json)
