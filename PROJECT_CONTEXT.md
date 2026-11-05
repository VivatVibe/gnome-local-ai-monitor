# Local AI Monitor - Project Context

This is a standalone GNOME Shell Extension project for monitoring local AI (Ollama) and GPU VRAM usage.

## Repository Overview

- **Extension UUID:** `local-ai-monitor@local-ai.mrnv`
- **Supported GNOME Versions:** 45, 46, 47, 48, 49, 50, 51
- **Architecture:** GJS ESM modules (Libadwaita prefs, St panel indicator, Soup 3.0, Gio.Subprocess)

## Directory Structure

```text
local-ai-monitor/
├── extension/
│   ├── metadata.json                                            # Extension manifest & GNOME shell version support
│   ├── stylesheet.css                                           # Top panel badge & menu styling
│   ├── extension.js                                             # Main extension lifecycle (enable / disable)
│   ├── prefs.js                                                 # Libadwaita preferences window
│   ├── schemas/
│   │   └── org.gnome.shell.extensions.local-ai-monitor.gschema.xml  # GSettings schema definition
│   ├── lib/
│   │   ├── types.js                                             # Enums (ServerStatus) & byte/duration formatters
│   │   ├── ollamaClient.js                                      # Asynchronous Soup 3.0 REST client for Ollama API
│   │   └── gpuTelemetry.js                                      # Asynchronous Gio.Subprocess telemetry for nvidia-smi
│   └── ui/
│       ├── indicator.js                                         # Top bar PanelMenu.Button widget
│       └── menu.js                                              # Popup menu dropdown items
├── scripts/
│   ├── package.sh                                               # Builds .shell-extension.zip bundle
│   ├── install.sh                                               # Builds, installs, and enables in GSettings
│   └── verify.sh                                                # Runs full end-to-end verification suite
├── tests/
│   ├── test_scaffold.sh                                         # PR 1 schema & metadata tests
│   ├── test_ollama_client.js                                    # PR 2 Ollama async networking tests
│   ├── test_gpu_telemetry.js                                    # PR 3 GPU VRAM telemetry tests
│   └── test_ui_assembly.sh                                      # PR 4 UI assembly & packaging tests
├── docs/
│   └── local-ai-monitor-plan.md                                 # Full 5-phase verified multi-PR plan
├── README.md                                                    # User-facing documentation and instructions
└── .gitignore                                                   # Git exclusion rules
```

## How to Test and Verify

Run the full verification suite:

```bash
bash scripts/verify.sh
```

## How to Build and Install

```bash
bash scripts/install.sh
```

After logging out and logging back in (required on Wayland):

```bash
gnome-extensions prefs local-ai-monitor@local-ai.mrnv
```
