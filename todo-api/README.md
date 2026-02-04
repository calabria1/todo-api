# todo-api (AWS Lambda - Python 3.11)

Código da **API (CRUD de tarefas)** para rodar em **AWS Lambda** atrás de um **API Gateway HTTP API (payload v2.0)**.

## Rotas (HTTP API)
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{id}`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`

## Variáveis de ambiente
- `TABLE_NAME` (obrigatóriaa): nome da tabela DynamoDB.

## Requisitos
- Python **3.11+**
- AWS CLI configurada localmente (para testes locais usando AWS real):
  - `aws configure` ou profile via SSO

## Rodar/testar local (usando DynamoDB real na AWS)
1) Crie a infra (DynamoDB + Lambda + API) pelo repo `todo-infra`.
2) Exporte o nome da tabela:
   - PowerShell:
     ```powershell
     $env:TABLE_NAME="todo-dev-tasks"
     ```
   - Bash:
     ```bash
     export TABLE_NAME="todo-dev-tasks"
     ```
3) Instale dependências:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r services/tasks/requirements.txt -r requirements-dev.txt
   ```
4) Rode um teste manual (simula evento do API Gateway):
   ```bash
   python scripts/local_invoke.py
   ```

## Build do zip (para deploy)
No Windows PowerShell:
```powershell
./scripts/build.ps1
```

No Linux/Mac:
```bash
bash scripts/build.sh
```

O artefato sai em: `dist/tasks.zip`

## Deploy para AWS
Antes do deploy, garanta que a função Lambda já exista (criada via `todo-infra`) e tenha permissões para acessar a tabela DynamoDB.

Linux/Mac:
```bash
export LAMBDA_FUNCTION_NAME="todo-dev-tasks-handler"
export AWS_REGION="us-east-1"  # opcional se já estiver configurado
bash scripts/deploy.sh
```

Windows PowerShell:
```powershell
$env:LAMBDA_FUNCTION_NAME="todo-dev-tasks-handler"
$env:AWS_REGION="us-east-1"  # opcional se já estiver configurado
./scripts/deploy.ps1
```
