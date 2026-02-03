from __future__ import annotations

import os
from typing import Any, Dict

from .repository import TaskRepository, RepoConfig
from .validators import validate_payload
from .responses import response
from .routing import parse_http_api_event

TABLE_NAME = os.environ.get("TABLE_NAME", "")

_repo = TaskRepository(RepoConfig(table_name=TABLE_NAME))

def lambda_handler(event: Dict[str, Any], context: Any):
    req = parse_http_api_event(event)

    # /tasks e /tasks/{id}
    task_id = (req.path_params or {}).get("id")

    try:
        if req.method == "POST" and req.path == "/tasks":
            validate_payload(req.body_json, creating=True)
            created = _repo.create(req.body_json)
            return response(201, created)

        if req.method == "GET" and req.path == "/tasks":
            return response(200, _repo.list_all())

        if req.method == "GET" and task_id:
            item = _repo.get(task_id)
            if not item:
                return response(404, {"message": "Task not found"})
            return response(200, item)

        if req.method == "PUT" and task_id:
            validate_payload(req.body_json, creating=False)
            updated = _repo.update(task_id, req.body_json)
            if not updated:
                return response(404, {"message": "Task not found"})
            return response(200, updated)

        if req.method == "DELETE" and task_id:
            ok = _repo.delete(task_id)
            if not ok:
                return response(404, {"message": "Task not found"})
            return response(204, None)

        # OPTIONS (CORS preflight)
        if req.method == "OPTIONS":
            return response(204, None)

        return response(404, {"message": "Route not found"})
    except ValueError as e:
        return response(400, {"message": str(e)})
    except Exception as e:
        # Mantém simples; depois podemos adicionar logs melhores
        return response(500, {"message": "Internal error", "detail": str(e)})
