import St from 'gi://St';
import Clutter from 'gi://Clutter';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import { ServerStatus, formatBytes } from '../lib/types.js';

export class LocalAiMenu {
  constructor(menu, ollamaClient, gpuTelemetry, onOpenPrefs = null) {
    this._menu = menu;
    this._ollamaClient = ollamaClient;
    this._gpuTelemetry = gpuTelemetry;
    this._onOpenPrefs = onOpenPrefs;
    this._lastModelsSig = null;

    this._buildStaticSections();
  }

  _buildStaticSections() {
    this._menu.removeAll();

    // 1. Server Header
    this._serverItem = new PopupMenu.PopupMenuItem('Server: Checking...', {
      reactive: false,
    });
    this._menu.addMenuItem(this._serverItem);

    this._menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

    // 2. Active Model Section
    this._activeSectionHeader = new PopupMenu.PopupMenuItem('ACTIVE MODEL', {
      reactive: false,
      style_class: 'local-ai-menu-header',
    });
    this._menu.addMenuItem(this._activeSectionHeader);

    this._activeModelItem = new PopupMenu.PopupMenuItem('None loaded', {
      reactive: false,
    });
    this._menu.addMenuItem(this._activeModelItem);

    this._unloadItem = new PopupMenu.PopupMenuItem('⏏ Unload Active Model', {
      reactive: true,
    });
    this._unloadItem.connect('activate', () => {
      const loaded = this._ollamaClient.state.loadedModels;
      if (loaded && loaded.length > 0) {
        this._ollamaClient.unloadModel(loaded[0].name);
      }
    });
    this._menu.addMenuItem(this._unloadItem);

    // 3. Installed Models SubMenu
    this._installedSubMenu = new PopupMenu.PopupSubMenuMenuItem('📦 Installed Models');
    this._menu.addMenuItem(this._installedSubMenu);

    this._menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

    // 4. GPU Telemetry Section
    this._gpuSectionHeader = new PopupMenu.PopupMenuItem('GPU TELEMETRY', {
      reactive: false,
      style_class: 'local-ai-menu-header',
    });
    this._menu.addMenuItem(this._gpuSectionHeader);

    this._gpuNameItem = new PopupMenu.PopupMenuItem('GPU: Detecting...', {
      reactive: false,
    });
    this._menu.addMenuItem(this._gpuNameItem);

    this._vramItem = new PopupMenu.PopupMenuItem('VRAM: --', {
      reactive: false,
    });
    this._menu.addMenuItem(this._vramItem);

    this._menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

    // 5. Preferences item
    if (this._onOpenPrefs) {
      const prefsItem = new PopupMenu.PopupMenuItem('⚙ Extension Settings');
      prefsItem.connect('activate', () => {
        this._onOpenPrefs();
      });
      this._menu.addMenuItem(prefsItem);
    }
  }

  update(ollamaState, gpuState) {
    // 1. Update Server status
    if (ollamaState.status === ServerStatus.ONLINE) {
      this._serverItem.label.set_text(`● Ollama ONLINE (v${ollamaState.version || '?'})`);
      this._serverItem.label.style_class = 'local-ai-status-online';
    } else {
      this._serverItem.label.set_text('○ Ollama OFFLINE');
      this._serverItem.label.style_class = 'local-ai-status-offline';
    }

    // 2. Update Active Model
    const loaded = ollamaState.loadedModels || [];
    if (loaded.length > 0) {
      const model = loaded[0];
      const vramText = model.sizeVram > 0 ? ` (${formatBytes(model.sizeVram)} VRAM)` : '';
      this._activeModelItem.label.set_text(`${model.name}${vramText}`);
      this._unloadItem.setSensitive(true);
    } else {
      this._activeModelItem.label.set_text('No model currently in VRAM');
      this._unloadItem.setSensitive(false);
    }

    // 3. Update Installed Models SubMenu
    if (ollamaState.status !== ServerStatus.ONLINE) {
      if (this._lastModelsSig !== 'offline') {
        this._lastModelsSig = 'offline';
        this._installedSubMenu.menu.removeAll();
        const offItem = new PopupMenu.PopupMenuItem('Server offline', { reactive: false });
        this._installedSubMenu.menu.addMenuItem(offItem);
        this._installedSubMenu.setSensitive(false);
      }
    } else {
      const available = ollamaState.availableModels || [];
      const loadedNames = new Set(loaded.map((m) => m.name));
      const sig = `${available.map((m) => m.name).join(',')}:${[...loadedNames].join(',')}`;

      if (this._lastModelsSig !== sig) {
        this._lastModelsSig = sig;
        this._installedSubMenu.menu.removeAll();

        if (available.length === 0) {
          const emptyItem = new PopupMenu.PopupMenuItem('No models installed', { reactive: false });
          this._installedSubMenu.menu.addMenuItem(emptyItem);
        } else {
          for (const m of available) {
            const isLoaded = loadedNames.has(m.name);
            const label = isLoaded
              ? `● ${m.name} (Active)`
              : `○ ${m.name} (${formatBytes(m.size)})`;
            const modelItem = new PopupMenu.PopupMenuItem(label, {
              reactive: !isLoaded,
            });
            if (!isLoaded) {
              modelItem.connect('activate', () => {
                this._ollamaClient.loadModel(m.name);
              });
            }
            this._installedSubMenu.menu.addMenuItem(modelItem);
          }
        }
        this._installedSubMenu.setSensitive(true);
      }
    }

    // 4. Update GPU Telemetry
    if (gpuState && gpuState.hasGpu) {
      this._gpuNameItem.label.set_text(`GPU: ${gpuState.name}`);
      this._vramItem.label.set_text(
        `VRAM: ${gpuState.memoryUsedMiB} MiB / ${gpuState.memoryTotalMiB} MiB (${gpuState.memoryUsedPercent}%) | GPU Load: ${gpuState.utilizationPercent}%`
      );
    } else {
      this._gpuNameItem.label.set_text('GPU: No NVIDIA GPU detected');
      this._vramItem.label.set_text('VRAM: --');
    }
  }

  destroy() {
    this._serverItem = null;
    this._activeModelItem = null;
    this._unloadItem = null;
    this._installedSubMenu = null;
    this._gpuNameItem = null;
    this._vramItem = null;
    this._menu = null;
  }
}
