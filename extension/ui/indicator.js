import GObject from 'gi://GObject';
import St from 'gi://St';
import Clutter from 'gi://Clutter';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import { ServerStatus } from '../lib/types.js';
import { AnimationController } from './animation.js';

export const LocalAiIndicator = GObject.registerClass(
  class LocalAiIndicator extends PanelMenu.Button {
    _init(extensionPath = null) {
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
        text: '0%',
        style_class: 'local-ai-badge',
        y_align: Clutter.ActorAlign.CENTER,
      });
      this._box.add_child(this._label);

      this.add_child(this._box);

      this._animController = new AnimationController(this._icon, extensionPath);
    }

    updateDisplay(ollamaState, gpuState, settings) {
      if (this._animController) {
        this._animController.update(ollamaState, gpuState, settings);
      }

      if (ollamaState && ollamaState.status === ServerStatus.ONLINE) {
        this._icon.style_class = 'system-status-icon local-ai-status-online';
      } else {
        this._icon.style_class = 'system-status-icon local-ai-status-offline';
      }

      if (!ollamaState || ollamaState.status !== ServerStatus.ONLINE) {
        this._label.set_text('Off');
        return;
      }

      const load = (gpuState && gpuState.hasGpu) ? (gpuState.utilizationPercent || 0) : 0;
      this._label.set_text(`${load}%`);
    }

    destroy() {
      if (this._animController) {
        this._animController.destroy();
        this._animController = null;
      }

      this._box = null;
      this._icon = null;
      this._label = null;
      super.destroy();
    }
  }
);
