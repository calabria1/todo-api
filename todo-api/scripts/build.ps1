\
$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Dist = Join-Path $Root "dist"
$Build = Join-Path $Root ".build\tasks"

if (Test-Path $Dist) { Remove-Item -Recurse -Force $Dist }
if (Test-Path $Build) { Remove-Item -Recurse -Force $Build }
New-Item -ItemType Directory -Force -Path $Dist | Out-Null
New-Item -ItemType Directory -Force -Path $Build | Out-Null

python -m pip install --upgrade pip | Out-Null
python -m pip install -r (Join-Path $Root "services\tasks\requirements.txt") -t $Build | Out-Null

New-Item -ItemType Directory -Force -Path (Join-Path $Build "services\tasks\src") | Out-Null
Copy-Item -Recurse -Force (Join-Path $Root "services\tasks\src\*") (Join-Path $Build "services\tasks\src")

$ZipPath = Join-Path $Dist "tasks.zip"
if (Test-Path $ZipPath) { Remove-Item -Force $ZipPath }

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($Build, $ZipPath)

Write-Host "Created: $ZipPath"
