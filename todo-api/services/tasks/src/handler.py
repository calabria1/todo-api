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

    # /tarefas e /tarefas/{id}
    tarefa_id = (req.path_params or {}).get("id")

    try:
        if req.method == "POST" and req.path == "/tarefas":
            validate_payload(req.body_json, creating=True)
            criada = _repo.create(req.body_json)
            return response(201, criada)

        if req.method == "GET" and req.path == "/tarefas":
            return response(200, _repo.list_all())

        if req.method == "GET" and tarefa_id:
            item = _repo.get(tarefa_id)
            if not item:
                return response(404, {"mensagem": "Tarefa não encontrada"})
            return response(200, item)

        if req.method == "PUT" and tarefa_id:
            validate_payload(req.body_json, creating=False)
            atualizada = _repo.update(tarefa_id, req.body_json)
            if not atualizada:
                return response(404, {"mensagem": "Tarefa não encontrada"})
            return response(200, atualizada)

        if req.method == "DELETE" and tarefa_id:
            ok = _repo.delete(tarefa_id)
            if not ok:
                return response(404, {"mensagem": "Tarefa não encontrada"})
            return response(204, None)

        # OPTIONS (CORS preflight)
        if req.method == "OPTIONS":
            return response(204, None)

        return response(404, {"mensagem": "Rota não encontrada"})
    except ValueError as e:
        return response(400, {"mensagem": str(e)})
    except Exception as e:
        return response(500, {"mensagem": "Erro interno", "detalhe": str(e)})
