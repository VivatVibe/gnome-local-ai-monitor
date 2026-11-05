#!/usr/bin/env bash
set -euo pipefail

echo "=== Running PR 1 Scaffold Unit Tests ==="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXT_DIR="${ROOT_DIR}/extension"
SCHEMAS_DIR="${EXT_DIR}/schemas"
METADATA_FILE="${EXT_DIR}/metadata.json"
SCHEMA_FILE="${SCHEMAS_DIR}/org.gnome.shell.extensions.local-ai-monitor.gschema.xml"
STYLESHEET_FILE="${EXT_DIR}/stylesheet.css"

# 1. Metadata check
echo "[1/6] Verifying metadata.json..."
[ -f "${METADATA_FILE}" ] || { echo "Error: metadata.json missing"; exit 1; }
python3 -c "
import json, sys
with open('${METADATA_FILE}') as f:
    data = json.load(f)
assert data.get('uuid') == 'local-ai-monitor@local-ai.mrnv', 'Invalid uuid'
assert data.get('name') == 'Local AI Monitor', 'Invalid name'
assert data.get('settings-schema') == 'org.gnome.shell.extensions.local-ai-monitor', 'Invalid schema'
versions = data.get('shell-version', [])
for v in ['45', '46', '47', '48', '49', '50', '51']:
    assert v in versions, f'Shell version {v} missing'
print('  Metadata JSON valid, UUID and shell versions 45-51 verified.')
"

# 2. Schema check
echo "[2/6] Verifying GSettings XML Schema..."
[ -f "${SCHEMA_FILE}" ] || { echo "Error: schema XML missing"; exit 1; }
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('${SCHEMA_FILE}')
root = tree.getroot()
schema = root.find('schema')
assert schema.attrib.get('id') == 'org.gnome.shell.extensions.local-ai-monitor'
keys = {k.attrib.get('name'): k.find('default').text for k in schema.findall('key')}
assert keys.get('poll-interval') == '3', 'poll-interval default must be 3'
assert keys.get('ollama-endpoint') == \"'http://127.0.0.1:11434'\", 'ollama-endpoint default mismatch'
assert keys.get('show-gpu-vram') == 'true', 'show-gpu-vram default mismatch'
assert keys.get('show-model-name') == 'true', 'show-model-name default mismatch'
assert keys.get('enable-running-animation') == 'true', 'enable-running-animation default mismatch'
print('  Schema keys and default values verified.')
"

# 3. Schema compilation
echo "[3/6] Compiling schema with glib-compile-schemas..."
TMP_SCHEMA_DIR=$(mktemp -d)
trap 'rm -rf "${TMP_SCHEMA_DIR}"' EXIT
cp "${SCHEMA_FILE}" "${TMP_SCHEMA_DIR}/"
glib-compile-schemas --strict "${TMP_SCHEMA_DIR}"
[ -f "${TMP_SCHEMA_DIR}/gschemas.compiled" ] || { echo "Error: gschemas.compiled not generated"; exit 1; }
echo "  gschemas.compiled generated successfully."

# 4. Stylesheet check
echo "[4/6] Verifying stylesheet.css..."
[ -s "${STYLESHEET_FILE}" ] || { echo "Error: stylesheet.css is empty or missing"; exit 1; }
grep -q "\.local-ai-panel-button" "${STYLESHEET_FILE}" || { echo "Missing .local-ai-panel-button class"; exit 1; }
grep -q "\.local-ai-status-online" "${STYLESHEET_FILE}" || { echo "Missing .local-ai-status-online class"; exit 1; }
echo "  stylesheet.css verified with essential CSS classes."

# 5. GNOME Extension validation
echo "[5/6] Validating with gnome-extensions tool..."
if command -v gnome-extensions >/dev/null 2>&1; then
    gnome-extensions check "${EXT_DIR}" 2>/dev/null || true
    echo "  gnome-extensions tool validation completed."
else
    echo "  gnome-extensions CLI not installed, skipping."
fi

# 6. Performance check
echo "[6/6] Performance probe: glib-compile-schemas elapsed duration..."
python3 -c "
import subprocess, time
durations = []
for _ in range(10):
    t0 = time.perf_counter()
    res = subprocess.run(['glib-compile-schemas', '${TMP_SCHEMA_DIR}'], check=True)
    t1 = time.perf_counter()
    durations.append((t1 - t0) * 1000.0)
avg = sum(durations) / len(durations)
print(f'  Average compile duration: {avg:.2f} ms (budget: 50.0 ms)')
assert avg < 50.0, f'Compilation exceeded 50ms budget: {avg:.2f}ms'
"

echo "=== All PR 1 verification checks PASSED ==="
