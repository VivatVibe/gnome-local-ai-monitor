import GObject from 'gi://GObject';
import St from 'gi://St';
import Clutter from 'gi://Clutter';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import { ServerStatus, formatBytes } from '../lib/types.js';

export const LocalAiIndicator = GObject.registerClass(
  class LocalAiIndicator extends PanelMenu.Button {
    _init() {
      super._init(0.0, 'Local AI Monitor', false);

      this._box = new St.BoxLayout({
        style_class: 'local-ai-panel-box',
        y_align: Clutter.ActorAlign.CENTER,
      });

      this._icon = new St.Icon({
        icon_name: 'utilities-terminal-symbolic',
        style_class: 'system-status-icon',
      });
      this._box.add_child(this._icon);

      this._label = new St.Label({
        text: 'AI',
        style_class: 'local-ai-badge',
        y_align: Clutter.ActorAlign.CENTER,
      });
      this._box.add_child(this._label);

      this.add_child(this._box);
    }

    updateDisplay(ollamaState, gpuState, settings) {
      const showModel = settings ? settings.get_boolean('show-model-name') : true;
      const showVram = settings ? settings.get_boolean('show-gpu-vram') : true;

      if (ollamaState.status === ServerStatus.ONLINE) {
        this._icon.icon_name = 'system-run-symbolic';
        this._icon.style_class = 'system-status-icon local-ai-status-online';
      } else {
        this._icon.icon_name = 'utilities-terminal-symbolic';
        this._icon.style_class = 'system-status-icon local-ai-status-offline';
      }

      let labelParts = [];
      if (showModel && ollamaState.loadedModels && ollamaState.loadedModels.length > 0) {
        const activeModelName = ollamaState.loadedModels[0].name.split(':')[0];
        labelParts.push(activeModelName);
      }

      if (showVram && gpuState && gpuState.hasGpu) {
        labelParts.push(`${gpuState.memoryUsedPercent}%`);
      }

      if (labelParts.length === 0) {
        labelParts.push(ollamaState.status === ServerStatus.ONLINE ? 'Ready' : 'Off');
      }

      this._label.set_text(labelParts.join(' | '));
    }

    destroy() {
      this._box = null;
      this._icon = null;
      this._label = null;
      super.destroy();
    }
  }
);
