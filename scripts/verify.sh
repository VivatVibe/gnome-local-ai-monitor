#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " Running Full Verification Suite for Local AI Monitor "
echo "=========================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. PR 1 Scaffold
echo ""
echo ">> Step 1/5: Verifying PR 1 Scaffold & Schemas..."
bash "${ROOT_DIR}/tests/test_scaffold.sh"

# 2. PR 2 Ollama Client
echo ""
echo ">> Step 2/5: Verifying PR 2 Ollama Client & Async Networking..."
gjs -m "${ROOT_DIR}/tests/test_ollama_client.js"

# 3. PR 3 GPU Telemetry
echo ""
echo ">> Step 3/5: Verifying PR 3 GPU VRAM Telemetry..."
gjs -m "${ROOT_DIR}/tests/test_gpu_telemetry.js"

# 4. PR 4 UI Assembly
echo ""
echo ">> Step 4/5: Verifying PR 4 UI Assembly & Packaging..."
bash "${ROOT_DIR}/tests/test_ui_assembly.sh"

# 5. PR 5 Package Build & Inspection
echo ""
echo ">> Step 5/5: Building Final Distribution Package..."
bash "${ROOT_DIR}/scripts/package.sh"

echo ""
echo "=========================================================="
echo " ALL 5 PHASES VERIFIED SUCCESSFULLY "
echo "=========================================================="
