import GLib from 'gi://GLib';
import Gio from 'gi://Gio';
import { ServerStatus } from '../lib/types.js';

export class AnimationController {
  constructor(iconActor, basePath) {
    this._iconActor = iconActor;
    this._basePath = basePath;
    this._runningFrames = [];
    this._sleepingFrame = null;
    this._offlineFrame = null;
    this._currentFrameIndex = 0;
    this._tickerId = null;
    this._currentInterval = null;

    this._loadIcons();
  }

  _loadIcons() {
    try {
      const gpuDir = `${this._basePath}/resources/icons/gpu`;
      const alpacaDir = `${this._basePath}/resources/icons/alpaca`;

      const hasGpuIcons = Gio.File.new_for_path(`${gpuDir}/idle.svg`).query_exists(null);

      if (hasGpuIcons) {
        this._sleepingFrame = Gio.icon_new_for_string(`${gpuDir}/idle.svg`);
        this._offlineFrame = Gio.icon_new_for_string(`${gpuDir}/offline.svg`);
        for (let i = 0; i < 4; i++) {
          const framePath = `${gpuDir}/fan-${i}.svg`;
          if (Gio.File.new_for_path(framePath).query_exists(null)) {
            this._runningFrames.push(Gio.icon_new_for_string(framePath));
          }
        }
      } else {
        const sleepingPath = `${alpacaDir}/sleeping-symbolic.svg`;
        const idlePath = `${alpacaDir}/idle-symbolic.svg`;
        const targetSleeping = Gio.File.new_for_path(sleepingPath).query_exists(null)
          ? sleepingPath
          : idlePath;

        if (Gio.File.new_for_path(targetSleeping).query_exists(null)) {
          this._sleepingFrame = Gio.icon_new_for_string(targetSleeping);
        }

        const offlinePath = `${alpacaDir}/offline-symbolic.svg`;
        if (Gio.File.new_for_path(offlinePath).query_exists(null)) {
          this._offlineFrame = Gio.icon_new_for_string(offlinePath);
        }

        for (let i = 0; i < 4; i++) {
          const framePath = `${alpacaDir}/running-${i}-symbolic.svg`;
          if (Gio.File.new_for_path(framePath).query_exists(null)) {
            this._runningFrames.push(Gio.icon_new_for_string(framePath));
          }
        }
      }
    } catch (e) {
      logError(e, 'Failed to load animation frames');
    }
  }

  _stopTicker() {
    if (this._tickerId) {
      GLib.Source.remove(this._tickerId);
      this._tickerId = null;
    }
    this._currentInterval = null;
  }

  _startTicker(intervalMs) {
    if (this._tickerId && this._currentInterval === intervalMs) {
      return;
    }

    this._stopTicker();
    this._currentInterval = intervalMs;

    this._tickerId = GLib.timeout_add(GLib.PRIORITY_DEFAULT, intervalMs, () => {
      if (!this._iconActor || this._runningFrames.length === 0) {
        return GLib.SOURCE_REMOVE;
      }

      this._currentFrameIndex = (this._currentFrameIndex + 1) % this._runningFrames.length;
      this._iconActor.gicon = this._runningFrames[this._currentFrameIndex];
      return GLib.SOURCE_CONTINUE;
    });
  }

  update(ollamaState, gpuState, settings) {
    if (!this._iconActor) return;

    const animEnabled = settings ? settings.get_boolean('enable-running-animation') : true;

    // 1. If animations are disabled in preferences
    if (!animEnabled || this._runningFrames.length === 0) {
      this._stopTicker();
      if (ollamaState && ollamaState.status === ServerStatus.ONLINE) {
        if (this._sleepingFrame) {
          this._iconActor.gicon = this._sleepingFrame;
        } else {
          this._iconActor.icon_name = 'system-run-symbolic';
        }
      } else {
        if (this._offlineFrame) {
          this._iconActor.gicon = this._offlineFrame;
        } else {
          this._iconActor.icon_name = 'utilities-terminal-symbolic';
        }
      }
      return;
    }

    // 2. Offline state: offline card
    if (!ollamaState || ollamaState.status !== ServerStatus.ONLINE) {
      this._stopTicker();
      if (this._offlineFrame) {
        this._iconActor.gicon = this._offlineFrame;
      } else if (this._sleepingFrame) {
        this._iconActor.gicon = this._sleepingFrame;
      }
      return;
    }

    // 3. 0% Load / Idle state: Zero-RPM mode (fans stationary)
    const gpuLoad = (gpuState && gpuState.hasGpu) ? (gpuState.utilizationPercent || 0) : 0;

    if (gpuLoad === 0) {
      this._stopTicker();
      if (this._sleepingFrame) {
        this._iconActor.gicon = this._sleepingFrame;
      }
      return;
    }

    // 4. Active load state (load > 0%): Dual fans spin dynamically
    const clampedLoad = Math.min(100, Math.max(1, gpuLoad));
    // Dynamic interval: 1% load = 200 ms, 100% load = 50 ms fast turbo spin
    const intervalMs = Math.max(50, Math.round(200 - (clampedLoad * 1.5)));

    this._startTicker(intervalMs);
  }

  destroy() {
    this._stopTicker();
    this._iconActor = null;
    this._runningFrames = [];
    this._sleepingFrame = null;
    this._offlineFrame = null;
  }
}
