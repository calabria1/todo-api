$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")

if (-not $env:LAMBDA_FUNCTION_NAME) {
  Write-Error "LAMBDA_FUNCTION_NAME is required (e.g. $env:LAMBDA_FUNCTION_NAME='todo-dev-tasks-handler')"
}

& (Join-Path $RootDir "scripts" "build.ps1")

$ZipPath = Join-Path $RootDir "dist" "tasks.zip"

if ($env:AWS_REGION) {
  $Region = $env:AWS_REGION
  aws lambda update-function-code --function-name $env:LAMBDA_FUNCTION_NAME --zip-file "fileb://$ZipPath" --region $Region
} elseif ($env:AWS_DEFAULT_REGION) {
  $Region = $env:AWS_DEFAULT_REGION
  aws lambda update-function-code --function-name $env:LAMBDA_FUNCTION_NAME --zip-file "fileb://$ZipPath" --region $Region
} else {
  aws lambda update-function-code --function-name $env:LAMBDA_FUNCTION_NAME --zip-file "fileb://$ZipPath"
}

Write-Host "Deployed $ZipPath to $env:LAMBDA_FUNCTION_NAME"
