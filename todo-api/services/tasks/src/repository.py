from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3

@dataclass(frozen=True)
class RepoConfig:
    table_name: str

class TaskRepository:
    def __init__(self, config: RepoConfig):
        if not config.table_name:
            raise ValueError("TABLE_NAME is required")
        self._table = boto3.resource("dynamodb").Table(config.table_name)

    @staticmethod
    def _now_date_br() -> str:
        # dd/mm/aaaa, conforme enunciado
        return datetime.now(timezone.utc).strftime("%d/%m/%Y")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        item: Dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "titulo": data["titulo"],
            "descricao": data.get("descricao", ""),
            "status": data.get("status", "Pendente"),
            "criado_por": data.get("criado_por", "system"),
            "data_criacao": self._now_date_br(),
            "data_conclusao": data.get("data_conclusao", ""),
        }
        self._table.put_item(Item=item)
        return item

    def list_all(self) -> List[Dict[str, Any]]:
        resp = self._table.scan()
        return resp.get("Items", [])

    def get(self, task_id: str) -> Optional[Dict[str, Any]]:
        resp = self._table.get_item(Key={"id": task_id})
        return resp.get("Item")

    def update(self, task_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        existing = self.get(task_id)
        if not existing:
            return None

        for k in ["titulo", "descricao", "status", "criado_por", "data_conclusao"]:
            if k in data and data[k] is not None:
                existing[k] = data[k]

        self._table.put_item(Item=existing)
        return existing

    def delete(self, task_id: str) -> bool:
        existing = self.get(task_id)
        if not existing:
            return False
        self._table.delete_item(Key={"id": task_id})
        return True
