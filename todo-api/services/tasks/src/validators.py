from __future__ import annotations
from .models import ALLOWED_STATUS

def validate_payload(data: dict, creating: bool) -> None:
    if creating and not data.get("titulo"):
        raise ValueError("Field 'titulo' is required")

    status = data.get("status")
    if status is not None and status not in ALLOWED_STATUS:
        raise ValueError(f"Invalid status. Allowed: {sorted(ALLOWED_STATUS)}")
