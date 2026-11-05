#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UUID="local-ai-monitor@local-ai.mrnv"
ZIP_PATH="${ROOT_DIR}/build/${UUID}.shell-extension.zip"

echo "=== Installing Local AI Monitor GNOME Extension ==="

# 1. Ensure package is built
bash "${ROOT_DIR}/scripts/package.sh"

# 2. Install extension into user extensions directory
echo "Installing extension bundle..."
gnome-extensions install --force "${ZIP_PATH}"

# 3. Add to GSettings enabled-extensions if not present
echo "Configuring GSettings enabled-extensions..."
CURRENT_EXTS=$(gsettings get org.gnome.shell enabled-extensions)
if [[ "${CURRENT_EXTS}" != *"${UUID}"* ]]; then
  NEW_EXTS=$(python3 -c "
import ast, sys
raw = sys.argv[1]
items = ast.literal_eval(raw)
if '${UUID}' not in items:
    items.append('${UUID}')
print(str(items))
" "${CURRENT_EXTS}")
  gsettings set org.gnome.shell enabled-extensions "${NEW_EXTS}"
  echo "  Enabled ${UUID} in GSettings."
else
  echo "  ${UUID} already present in enabled-extensions."
fi

echo ""
echo "=== Installation Successful ==="
echo "If on Wayland, log out and log back in to load into GNOME Shell."
echo "To open settings after logging in:"
echo "  gnome-extensions prefs ${UUID}"
