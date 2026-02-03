#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
BUILD_DIR="$ROOT_DIR/.build/tasks"

rm -rf "$DIST_DIR" "$BUILD_DIR"
mkdir -p "$DIST_DIR" "$BUILD_DIR"

# vendor dependencies
python -m pip install --upgrade pip >/dev/null
python -m pip install -r "$ROOT_DIR/services/tasks/requirements.txt" -t "$BUILD_DIR" >/dev/null

# copy source
mkdir -p "$BUILD_DIR/services/tasks/src"
cp -R "$ROOT_DIR/services/tasks/src/"* "$BUILD_DIR/services/tasks/src/"

# create zip
cd "$BUILD_DIR"
zip -r "$DIST_DIR/tasks.zip" . >/dev/null
echo "Created: $DIST_DIR/tasks.zip"
