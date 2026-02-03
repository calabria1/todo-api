#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${LAMBDA_FUNCTION_NAME:-}" ]]; then
  echo "LAMBDA_FUNCTION_NAME is required (e.g. export LAMBDA_FUNCTION_NAME=todo-dev-tasks-handler)" >&2
  exit 1
fi

bash "$ROOT_DIR/scripts/build.sh"

ZIP_PATH="$ROOT_DIR/dist/tasks.zip"

if [[ -n "${AWS_REGION:-${AWS_DEFAULT_REGION:-}}" ]]; then
  REGION_VALUE="${AWS_REGION:-${AWS_DEFAULT_REGION:-}}"
  aws lambda update-function-code \
    --function-name "$LAMBDA_FUNCTION_NAME" \
    --zip-file "fileb://$ZIP_PATH" \
    --region "$REGION_VALUE"
else
  aws lambda update-function-code \
    --function-name "$LAMBDA_FUNCTION_NAME" \
    --zip-file "fileb://$ZIP_PATH"
fi

echo "Deployed $ZIP_PATH to $LAMBDA_FUNCTION_NAME"
