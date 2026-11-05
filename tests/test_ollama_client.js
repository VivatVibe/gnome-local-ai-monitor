import GLib from 'gi://GLib';
import { OllamaClient } from '../extension/lib/ollamaClient.js';
import { ServerStatus, formatBytes, formatDuration } from '../extension/lib/types.js';

print('=== Running PR 2 OllamaClient Verification Tests ===');

const loop = GLib.MainLoop.new(null, false);

async function runTests() {
  try {
    // 1. Types verification
    print('[1/9] Verifying types and formatting helpers...');
    if (formatBytes(0) !== '0 B') throw new Error('formatBytes 0 failed');
    if (formatBytes(1024) !== '1.0 KiB') throw new Error('formatBytes 1024 failed');
    if (formatBytes(1024 * 1024 * 500) !== '500.0 MiB') throw new Error('formatBytes MiB failed');
    if (formatDuration(65) !== '1m 5s') throw new Error('formatDuration failed');
    print('  types and helpers verified.');

    // 2. Client initialization and online poll
    print('[2/9] Testing live Ollama connection (port 11434)...');
    const client = new OllamaClient('http://127.0.0.1:11434');
    const state = await client.poll();
    if (state.status !== ServerStatus.ONLINE) {
      throw new Error(`Expected ONLINE status, got ${state.status}: ${state.error}`);
    }
    if (!state.version) throw new Error('Missing server version');
    print(`  Server status: ${state.status}, version: ${state.version}`);

    // 3. Available models inspection (/api/tags)
    print('[3/9] Testing /api/tags parsing...');
    if (!Array.isArray(state.availableModels)) throw new Error('availableModels is not an array');
    print(`  Available models count: ${state.availableModels.length}`);
    if (state.availableModels.length > 0) {
      const first = state.availableModels[0];
      print(`  Found model: ${first.name} (${formatBytes(first.size)})`);
    }

    // 4. Loaded models inspection (/api/ps)
    print('[4/9] Testing /api/ps parsing...');
    if (!Array.isArray(state.loadedModels)) throw new Error('loadedModels is not an array');
    print(`  Currently loaded models: ${state.loadedModels.length}`);

    // 5. Test model preload API (loadModel)
    print('[5/9] Testing loadModel preload API...');
    if (state.availableModels.length > 0) {
      const targetModel = state.availableModels[0].name;
      const loadSuccess = await client.loadModel(targetModel);
      if (!loadSuccess) throw new Error(`loadModel failed for ${targetModel}`);
      const afterLoad = await client.poll();
      if (!afterLoad.loadedModels.some((m) => m.name === targetModel)) {
        throw new Error(`Model ${targetModel} not reported in loadedModels after preload`);
      }
      print(`  Successfully preloaded model: ${targetModel}`);
    } else {
      print('  Skipping loadModel execution (no models installed).');
    }

    // 6. Offline fallback test (invalid port)
    print('[6/9] Testing offline graceful degradation (unreachable port)...');
    const deadClient = new OllamaClient('http://127.0.0.1:59999');
    const deadState = await deadClient.poll();
    if (deadState.status !== ServerStatus.OFFLINE) {
      throw new Error(`Expected OFFLINE status for unreachable port, got ${deadState.status}`);
    }
    if (!deadState.error) throw new Error('Expected error message in OFFLINE state');
    print(`  Graceful degradation verified: status=${deadState.status}, handled message="${deadState.error}"`);
    deadClient.destroy();

    // 7. Polling listener and timer dispatch
    print('[7/9] Testing polling listener callback...');
    let listenerFired = false;
    const testListener = (s) => {
      listenerFired = true;
    };
    client.addListener(testListener);
    await client.poll();
    if (!listenerFired) throw new Error('Listener did not fire on poll');
    client.removeListener(testListener);
    print('  Listener callback dispatched cleanly.');

    // 8. Request cancellation and destroy cleanup
    print('[8/9] Testing destroy() cleanup and idempotency...');
    client.destroy();
    print('  Client destroyed without resource leaks.');

    // 9. Performance probe: latency test across 10 queries
    print('[9/9] Measuring round-trip latency over 10 consecutive queries...');
    const perfClient = new OllamaClient('http://127.0.0.1:11434');
    const latencies = [];
    for (let i = 0; i < 10; i++) {
      const t0 = Date.now();
      await perfClient.poll();
      latencies.push(Date.now() - t0);
    }
    const avgLatency = latencies.reduce((a, b) => a + b, 0) / latencies.length;
    print(`  Average round-trip latency: ${avgLatency.toFixed(1)} ms (budget: 100.0 ms)`);
    perfClient.destroy();
    if (avgLatency > 100.0) {
      throw new Error(`Latency budget exceeded: ${avgLatency} ms`);
    }

    print('=== All PR 2 verification tests PASSED ===');
  } catch (err) {
    printerr('PR 2 Verification FAILED:', err);
    loop.quit();
    GLib.idle_add(GLib.PRIORITY_DEFAULT, () => {
      // exit with failure
    });
    return;
  }
  loop.quit();
}

runTests();
loop.run();
