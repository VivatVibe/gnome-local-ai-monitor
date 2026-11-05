#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXT_DIR="${ROOT_DIR}/extension"
BUILD_DIR="${ROOT_DIR}/build"
SCHEMAS_DIR="${EXT_DIR}/schemas"

echo "=== Packaging Local AI Monitor GNOME Extension ==="

# 1. Compile GSettings schema
echo "Compiling GSettings schemas..."
glib-compile-schemas "${SCHEMAS_DIR}"

# 2. Prepare build directory
mkdir -p "${BUILD_DIR}"

# 3. Pack extension bundle
echo "Packaging extension bundle..."
gnome-extensions pack \
  --force \
  --extra-source=lib \
  --extra-source=ui \
  --extra-source=resources \
  --out-dir="${BUILD_DIR}" \
  "${EXT_DIR}"

ZIP_NAME="local-ai-monitor@local-ai.mrnv.shell-extension.zip"
ZIP_PATH="${BUILD_DIR}/${ZIP_NAME}"

if [ ! -f "${ZIP_PATH}" ]; then
  echo "Error: Bundle package failed to create at ${ZIP_PATH}" >&2
  exit 1
fi

SIZE_BYTES=$(stat -c%s "${ZIP_PATH}")
SIZE_KB=$((SIZE_BYTES / 1024))

echo "=== Packaging Complete ==="
echo "Artifact: ${ZIP_PATH}"
echo "Size: ${SIZE_KB} KB (${SIZE_BYTES} bytes)"
echo ""
echo "To install locally:"
echo "  gnome-extensions install --force ${ZIP_PATH}"
echo "  gnome-extensions enable local-ai-monitor@local-ai.mrnv"
