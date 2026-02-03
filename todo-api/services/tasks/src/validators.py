from __future__ import annotations
from .models import ALLOWED_STATUS

def validate_payload(data: dict, creating: bool) -> None:
    if creating and not data.get("titulo"):
        raise ValueError("O campo 'titulo' é obrigatório")

    status = data.get("status")
    if status is not None and status not in ALLOWED_STATUS:
        permitidos = sorted(ALLOWED_STATUS)
        raise ValueError(f"Status inválido. Permitidos: {permitidos}")
