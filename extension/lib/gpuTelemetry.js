import Gio from 'gi://Gio';
import GLib from 'gi://GLib';

Gio._promisify(Gio.Subprocess.prototype, 'communicate_utf8_async', 'communicate_utf8_finish');

export class GpuTelemetry {
  constructor() {
    this._cancellable = new Gio.Cancellable();
    this._pollSourceId = null;
    this._isQuerying = false;
    this._listeners = new Set();

    this.state = {
      hasGpu: false,
      name: '',
      memoryUsedMiB: 0,
      memoryTotalMiB: 0,
      memoryUsedBytes: 0,
      memoryTotalBytes: 0,
      memoryUsedPercent: 0,
      utilizationPercent: 0,
      lastQuery: 0,
      error: null,
    };
  }

  addListener(callback) {
    this._listeners.add(callback);
  }

  removeListener(callback) {
    this._listeners.delete(callback);
  }

  _notify() {
    for (const listener of this._listeners) {
      try {
        listener(this.state);
      } catch (e) {
        logError(e, 'GpuTelemetry listener notification failed');
      }
    }
  }

  async query() {
    if (this._isQuerying) {
      return this.state;
    }

    this._isQuerying = true;
    try {
      const proc = new Gio.Subprocess({
        argv: [
          'nvidia-smi',
          '--query-gpu=name,memory.used,memory.total,utilization.gpu',
          '--format=csv,noheader,nounits',
        ],
        flags: Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
      });

      proc.init(this._cancellable);
      const [stdout, stderr] = await proc.communicate_utf8_async(null, this._cancellable);

      if (!proc.get_successful()) {
        const errMsg = stderr ? stderr.trim() : 'nvidia-smi failed';
        throw new Error(errMsg);
      }

      if (stderr && stderr.trim()) {
        throw new Error(stderr.trim());
      }

      const line = (stdout || '').trim().split('\n')[0];
      if (!line) {
        throw new Error('Empty nvidia-smi output');
      }

      const parts = line.split(',').map((p) => p.trim());
      if (parts.length < 4) {
        throw new Error(`Unexpected nvidia-smi format: ${line}`);
      }

      const name = parts[0];
      const memoryUsedMiB = parseInt(parts[1], 10) || 0;
      const memoryTotalMiB = parseInt(parts[2], 10) || 0;
      const utilizationPercent = parseInt(parts[3], 10) || 0;

      const memoryUsedPercent =
        memoryTotalMiB > 0
          ? Math.round((memoryUsedMiB / memoryTotalMiB) * 100)
          : 0;

      this.state = {
        hasGpu: true,
        name,
        memoryUsedMiB,
        memoryTotalMiB,
        memoryUsedBytes: memoryUsedMiB * 1024 * 1024,
        memoryTotalBytes: memoryTotalMiB * 1024 * 1024,
        memoryUsedPercent,
        utilizationPercent,
        lastQuery: Date.now(),
        error: null,
      };
    } catch (e) {
      this.state = {
        hasGpu: false,
        name: '',
        memoryUsedMiB: 0,
        memoryTotalMiB: 0,
        memoryUsedBytes: 0,
        memoryTotalBytes: 0,
        memoryUsedPercent: 0,
        utilizationPercent: 0,
        lastQuery: Date.now(),
        error: e.message,
      };
    } finally {
      this._isQuerying = false;
      this._notify();
    }

    return this.state;
  }

  startPolling(intervalSec = 3, onUpdate = null) {
    if (onUpdate) {
      this.addListener(onUpdate);
    }

    this.stopPolling();
    this.query();

    this._pollSourceId = GLib.timeout_add_seconds(
      GLib.PRIORITY_DEFAULT,
      Math.max(1, intervalSec),
      () => {
        this.query();
        return GLib.SOURCE_CONTINUE;
      }
    );
  }

  stopPolling() {
    if (this._pollSourceId) {
      GLib.Source.remove(this._pollSourceId);
      this._pollSourceId = null;
    }
  }

  destroy() {
    this.stopPolling();
    this._listeners.clear();
    this._cancellable.cancel();
  }
}
