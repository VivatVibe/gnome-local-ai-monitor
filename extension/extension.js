import { Extension } from 'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import { OllamaClient } from './lib/ollamaClient.js';
import { GpuTelemetry } from './lib/gpuTelemetry.js';
import { LocalAiIndicator } from './ui/indicator.js';
import { LocalAiMenu } from './ui/menu.js';

export default class LocalAiMonitorExtension extends Extension {
  enable() {
    this._settings = this.getSettings();

    const endpoint = this._settings.get_string('ollama-endpoint') || 'http://127.0.0.1:11434';
    const intervalSec = this._settings.get_int('poll-interval') || 3;

    this._ollamaClient = new OllamaClient(endpoint);
    this._gpuTelemetry = new GpuTelemetry();

    this._indicator = new LocalAiIndicator();
    this._menu = new LocalAiMenu(
      this._indicator.menu,
      this._ollamaClient,
      this._gpuTelemetry,
      () => this.openPreferences()
    );

    Main.panel.addToStatusArea(this.uuid, this._indicator);

    this._updateHandler = () => {
      this._indicator.updateDisplay(
        this._ollamaClient.state,
        this._gpuTelemetry.state,
        this._settings
      );
      this._menu.update(
        this._ollamaClient.state,
        this._gpuTelemetry.state
      );
    };

    this._ollamaClient.addListener(this._updateHandler);
    this._gpuTelemetry.addListener(this._updateHandler);

    this._ollamaClient.startPolling(intervalSec);
    this._gpuTelemetry.startPolling(intervalSec);

    this._settingsChangedId = this._settings.connect('changed', (settings, key) => {
      if (key === 'poll-interval') {
        const newInterval = settings.get_int('poll-interval');
        this._ollamaClient.startPolling(newInterval);
        this._gpuTelemetry.startPolling(newInterval);
      } else if (key === 'ollama-endpoint') {
        const newEndpoint = settings.get_string('ollama-endpoint');
        this._ollamaClient.setEndpoint(newEndpoint);
        this._ollamaClient.poll();
      } else if (key === 'show-model-name' || key === 'show-gpu-vram') {
        this._updateHandler();
      }
    });

    this._updateHandler();
  }

  disable() {
    if (this._settingsChangedId) {
      this._settings.disconnect(this._settingsChangedId);
      this._settingsChangedId = null;
    }

    if (this._ollamaClient) {
      if (this._updateHandler) {
        this._ollamaClient.removeListener(this._updateHandler);
      }
      this._ollamaClient.destroy();
      this._ollamaClient = null;
    }

    if (this._gpuTelemetry) {
      if (this._updateHandler) {
        this._gpuTelemetry.removeListener(this._updateHandler);
      }
      this._gpuTelemetry.destroy();
      this._gpuTelemetry = null;
    }

    if (this._menu) {
      this._menu.destroy();
      this._menu = null;
    }

    if (this._indicator) {
      this._indicator.destroy();
      this._indicator = null;
    }

    this._settings = null;
    this._updateHandler = null;
  }
}
