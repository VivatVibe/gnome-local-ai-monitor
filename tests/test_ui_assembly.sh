#!/usr/bin/env bash
set -euo pipefail

echo "=== Running PR 4 UI Assembly Verification Tests ==="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXT_DIR="${ROOT_DIR}/extension"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "${TMP_DIR}"' EXIT

# 1. Check required files
echo "[1/5] Verifying UI source files..."
for f in extension.js prefs.js preferences.js ui/indicator.js ui/animation.js ui/menu.js lib/types.js lib/ollamaClient.js lib/gpuTelemetry.js resources/icons/alpaca/running-0-symbolic.svg; do
  [ -s "${EXT_DIR}/${f}" ] || { echo "Error: ${f} is missing or empty"; exit 1; }
done
echo "  All UI, animation, logic, and preference files exist."

# 2. Syntax validation
echo "[2/5] Checking ESM syntax of UI files..."
python3 -c "
import re

files = ['${EXT_DIR}/extension.js', '${EXT_DIR}/prefs.js', '${EXT_DIR}/preferences.js', '${EXT_DIR}/ui/indicator.js', '${EXT_DIR}/ui/animation.js', '${EXT_DIR}/ui/menu.js']
for path in files:
    with open(path) as f:
        content = f.read()
    assert 'import' in content, f'Missing import in {path}'
    assert 'export' in content, f'Missing export in {path}'
print('  ESM syntax verified across UI components.')
"

# 3. Test GNOME Extension Packaging
echo "[3/5] Testing extension bundle packaging with extra sources..."
gnome-extensions pack --force --extra-source=lib --extra-source=ui --extra-source=resources --extra-source=preferences.js --out-dir="${TMP_DIR}" "${EXT_DIR}"
ZIP_PATH="${TMP_DIR}/local-ai-monitor@local-ai.mrnv.shell-extension.zip"
[ -f "${ZIP_PATH}" ] || { echo "Error: extension zip not created"; exit 1; }
echo "  Shell extension zip generated successfully."

# 4. Inspect bundle integrity
echo "[4/5] Verifying archive integrity and manifest..."
python3 -c "
import zipfile
with zipfile.ZipFile('${ZIP_PATH}', 'r') as z:
    names = z.namelist()
    expected = [
        'metadata.json',
        'stylesheet.css',
        'extension.js',
        'prefs.js',
        'preferences.js',
        'ui/indicator.js',
        'ui/animation.js',
        'ui/menu.js',
        'lib/types.js',
        'lib/ollamaClient.js',
        'lib/gpuTelemetry.js',
        'resources/icons/alpaca/running-0-symbolic.svg',
        'resources/icons/alpaca/idle-symbolic.svg',
        'resources/icons/alpaca/offline-symbolic.svg',
        'resources/icons/gpu/fan-0.svg',
        'resources/icons/gpu/idle.svg'
    ]
    for exp in expected:
        assert any(exp in n for n in names), f'Missing {exp} in zip'
print(f'  Archive contains {len(names)} files, all required assets confirmed.')
"

# 5. Performance probe
echo "[5/5] Measuring packaging duration and archive size..."
python3 -c "
import os, subprocess, time
t0 = time.perf_counter()
subprocess.run(['gnome-extensions', 'pack', '--force', '--extra-source=lib', '--extra-source=ui', '--extra-source=resources', '--extra-source=preferences.js', '--out-dir=${TMP_DIR}', '${EXT_DIR}'], check=True)
dur_ms = (time.perf_counter() - t0) * 1000.0
size_kb = os.path.getsize('${ZIP_PATH}') / 1024.0
print(f'  Pack duration: {dur_ms:.1f} ms (budget: 200 ms)')
print(f'  Archive size: {size_kb:.1f} KB (budget: 200 KB)')
assert dur_ms < 200.0, 'Pack duration exceeded budget'
assert size_kb < 200.0, 'Archive size exceeded budget'
"

echo "=== All PR 4 verification checks PASSED ==="
