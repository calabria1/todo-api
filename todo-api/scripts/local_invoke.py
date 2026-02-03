import os
import json
from services.tasks.src.handler import lambda_handler

# Ajuste isso no seu terminal antes de rodar:
# PowerShell: $env:TABLE_NAME="todo-dev-tasks"
# Bash: export TABLE_NAME="todo-dev-tasks"

def make_event(method: str, path: str, body=None, path_params=None):
    return {
        "requestContext": {"http": {"method": method}},
        "rawPath": path,
        "pathParameters": path_params or {},
        "body": json.dumps(body) if body is not None else None,
    }

if __name__ == "__main__":
    if not os.environ.get("TABLE_NAME"):
        raise SystemExit("Set TABLE_NAME env var before running (points to your DynamoDB table).")

    # 1) Create
    ev = make_event("POST", "/tasks", {
        "titulo": "Minha tarefa",
        "descricao": "testando local",
        "status": "Pendente",
        "criado_por": "arthur",
        "data_conclusao": ""
    })
    res = lambda_handler(ev, None)
    print("CREATE:", res)

    created = json.loads(res["body"])
    task_id = created["id"]

    # 2) Get
    ev = make_event("GET", f"/tasks/{task_id}", path_params={"id": task_id})
    print("GET:", lambda_handler(ev, None))

    # 3) List
    ev = make_event("GET", "/tasks")
    print("LIST:", lambda_handler(ev, None))

    # 4) Update
    ev = make_event("PUT", f"/tasks/{task_id}", body={"status": "Concluída"}, path_params={"id": task_id})
    print("UPDATE:", lambda_handler(ev, None))

    # 5) Delete
    ev = make_event("DELETE", f"/tasks/{task_id}", path_params={"id": task_id})
    print("DELETE:", lambda_handler(ev, None))
