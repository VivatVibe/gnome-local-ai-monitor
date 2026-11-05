# Local AI Monitor (GNOME Shell Extension)

A native GNOME Shell extension for developers and AI enthusiasts running local LLMs on Linux.
Monitors your local Ollama instance and GPU VRAM usage directly from the top panel.

## Features

- **Cute Animated Ollama Alpaca (RunCat-style):** Mascot dynamically gallops based on GPU compute load and sleeps peacefully with `z Z` bubbles at 0% load.
- **Installed Models Submenu:** One-click preloading to warm any installed model into VRAM directly from the panel.
- **Real-time Ollama Status:** Shows server connectivity status (ONLINE/OFFLINE) and version.
- **Active Model Detection:** Displays the model currently resident in GPU memory.
- **VRAM & Compute Telemetry:** Tracks memory consumption (MiB / GiB) and utilization percentage on NVIDIA GPUs.
- **One-Click Unload:** Easily unload the active model from VRAM from the dropdown menu to free GPU memory.
- **Non-blocking Architecture:** Built with modern GJS ESM using asynchronous Soup 3.0 and Gio.Subprocess calls.
- **Customizable Preferences:** Configure the API endpoint, polling interval, and top-panel display options via Libadwaita preferences.

## Supported GNOME Versions

- GNOME Shell 45, 46, 47, 48, 49, 50, 51

## Requirements

- **GNOME Shell:** 45+
- **Ollama:** Running on `http://127.0.0.1:11434` (or custom configured endpoint)
- **NVIDIA GPU (Optional):** With `nvidia-smi` driver utilities installed for hardware telemetry

## Installation

### From Package Bundle

Build the extension package:

```bash
bash scripts/package.sh
```

Install and enable the extension:

```bash
gnome-extensions install --force build/local-ai-monitor@local-ai.mrnv.shell-extension.zip
gnome-extensions enable local-ai-monitor@local-ai.mrnv
```

Restart GNOME Shell (or log out and log back in on Wayland).

## Settings & Configuration

Open preferences from the extension menu or run:

```bash
gnome-extensions prefs local-ai-monitor@local-ai.mrnv
```

Options include:
- **Ollama API Endpoint:** Customize the host URL (default: `http://127.0.0.1:11434`).
- **Refresh Interval:** Adjust polling frequency between 1 and 60 seconds (default: 3s).
- **Display Active Model Name:** Toggle model name visibility on the top bar.
- **Display GPU VRAM Percentage:** Toggle VRAM percentage on the top bar.

## Verification & Testing

Run the full end-to-end verification suite:

```bash
bash scripts/verify_local_ai.sh
```
