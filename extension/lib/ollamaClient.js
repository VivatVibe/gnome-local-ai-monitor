import Soup from 'gi://Soup?version=3.0';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import { ServerStatus } from './types.js';

Gio._promisify(Soup.Session.prototype, 'send_and_read_async', 'send_and_read_finish');

export class OllamaClient {
  constructor(endpoint = 'http://127.0.0.1:11434') {
    this._endpoint = endpoint.replace(/\/+$/, '');
    this._session = new Soup.Session({
      timeout: 5,
    });
    this._cancellable = new Gio.Cancellable();
    this._pollSourceId = null;
    this._isPolling = false;
    this._listeners = new Set();

    this.state = {
      status: ServerStatus.CONNECTING,
      version: null,
      loadedModels: [],
      availableModels: [],
      lastPoll: 0,
      error: null,
    };
  }

  setEndpoint(endpoint) {
    this._endpoint = endpoint.replace(/\/+$/, '');
  }

  get endpoint() {
    return this._endpoint;
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
        logError(e, 'OllamaClient listener notification failed');
      }
    }
  }

  async _request(method, path, body = null) {
    const url = `${this._endpoint}${path}`;
    const message = Soup.Message.new(method, url);
    if (!message) {
      throw new Error(`Failed to create Soup message for ${url}`);
    }

    if (body) {
      const jsonStr = JSON.stringify(body);
      const bytes = new GLib.Bytes(new TextEncoder().encode(jsonStr));
      message.set_request_body_from_bytes('application/json', bytes);
    }

    const bytes = await this._session.send_and_read_async(
      message,
      GLib.PRIORITY_DEFAULT,
      this._cancellable
    );

    const statusCode = message.get_status();
    if (statusCode < 200 || statusCode >= 300) {
      throw new Error(`HTTP status ${statusCode} for ${path}`);
    }

    const text = new TextDecoder().decode(bytes.get_data());
    return text ? JSON.parse(text) : {};
  }

  async poll() {
    if (this._isPolling) {
      return this.state;
    }

    this._isPolling = true;
    try {
      const versionData = await this._request('GET', '/api/version');
      const version = versionData.version || 'unknown';

      const psData = await this._request('GET', '/api/ps');
      const loadedModels = (psData.models || []).map((m) => ({
        name: m.name,
        model: m.model,
        size: m.size || 0,
        sizeVram: m.size_vram || 0,
        expiresAt: m.expires_at || null,
        details: m.details || {},
      }));

      const tagsData = await this._request('GET', '/api/tags');
      const availableModels = (tagsData.models || []).map((m) => ({
        name: m.name,
        model: m.model,
        size: m.size || 0,
        modifiedAt: m.modified_at || null,
        details: m.details || {},
      }));

      this.state = {
        status: ServerStatus.ONLINE,
        version,
        loadedModels,
        availableModels,
        lastPoll: Date.now(),
        error: null,
      };
    } catch (e) {
      this.state = {
        status: ServerStatus.OFFLINE,
        version: null,
        loadedModels: [],
        availableModels: [],
        lastPoll: Date.now(),
        error: e.message,
      };
    } finally {
      this._isPolling = false;
      this._notify();
    }

    return this.state;
  }

  async unloadModel(modelName) {
    if (!modelName) return false;
    try {
      await this._request('POST', '/api/generate', {
        model: modelName,
        keep_alive: 0,
      });
      await this.poll();
      return true;
    } catch (e) {
      logError(e, `Failed to unload model ${modelName}`);
      return false;
    }
  }

  startPolling(intervalSec = 3, onUpdate = null) {
    if (onUpdate) {
      this.addListener(onUpdate);
    }

    this.stopPolling();
    this.poll();

    this._pollSourceId = GLib.timeout_add_seconds(
      GLib.PRIORITY_DEFAULT,
      Math.max(1, intervalSec),
      () => {
        this.poll();
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
    this._session.abort();
  }
}
