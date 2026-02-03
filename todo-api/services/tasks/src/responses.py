from __future__ import annotations
import json
from typing import Any, Optional

def response(status_code: int, body: Optional[Any]):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        # API aberta + sem dor de CORS (browser)
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }
    if status_code == 204:
        return {"statusCode": 204, "headers": headers, "body": ""}

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body, ensure_ascii=False),
    }
