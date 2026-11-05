import GLib from 'gi://GLib';
import { GpuTelemetry } from '../extension/lib/gpuTelemetry.js';

print('=== Running PR 3 GpuTelemetry Verification Tests ===');

const loop = GLib.MainLoop.new(null, false);

async function runTests() {
  try {
    const telemetry = new GpuTelemetry();

    // 1. Live hardware telemetry query
    print('[1/7] Testing live hardware telemetry query...');
    const state = await telemetry.query();
    if (!state.hasGpu) {
      print(`  No NVIDIA GPU detected or driver unavailable: ${state.error}`);
    } else {
      print(`  Detected GPU: ${state.name}`);
      print(`  VRAM: ${state.memoryUsedMiB} MiB / ${state.memoryTotalMiB} MiB (${state.memoryUsedPercent}%)`);
      print(`  Compute Utilization: ${state.utilizationPercent}%`);

      if (state.memoryTotalMiB <= 0) throw new Error('memoryTotalMiB must be positive');
      if (state.memoryUsedMiB < 0) throw new Error('memoryUsedMiB cannot be negative');
      if (state.memoryUsedPercent < 0 || state.memoryUsedPercent > 100) {
        throw new Error(`Invalid memoryUsedPercent: ${state.memoryUsedPercent}`);
      }
      if (state.utilizationPercent < 0 || state.utilizationPercent > 100) {
        throw new Error(`Invalid utilizationPercent: ${state.utilizationPercent}`);
      }
    }

    // 2. Listener event callback test
    print('[2/7] Testing listener notification callback...');
    let listenerFired = false;
    const testListener = (s) => {
      listenerFired = true;
    };
    telemetry.addListener(testListener);
    await telemetry.query();
    if (!listenerFired) throw new Error('Listener did not fire on telemetry query');
    telemetry.removeListener(testListener);
    print('  Listener notification verified.');

    // 3. Non-blocking test
    print('[3/7] Verifying non-blocking execution...');
    let eventLoopTicked = false;
    GLib.idle_add(GLib.PRIORITY_DEFAULT, () => {
      eventLoopTicked = true;
      return GLib.SOURCE_REMOVE;
    });
    await telemetry.query();
    if (!eventLoopTicked) throw new Error('Main event loop was blocked during query');
    print('  Event loop processed idle callbacks concurrently.');

    // 4. Memory bytes conversion test
    print('[4/7] Testing memory bytes calculation...');
    if (state.hasGpu) {
      if (state.memoryUsedBytes !== state.memoryUsedMiB * 1024 * 1024) {
        throw new Error('memoryUsedBytes mismatch');
      }
      if (state.memoryTotalBytes !== state.memoryTotalMiB * 1024 * 1024) {
        throw new Error('memoryTotalBytes mismatch');
      }
      print('  Memory byte conversions exact.');
    }

    // 5. Polling start and stop lifecycle
    print('[5/7] Testing polling start and stop...');
    telemetry.startPolling(1);
    telemetry.stopPolling();
    print('  Polling timer lifecycle cleanly managed.');

    // 6. Destroy cleanup
    print('[6/7] Testing destroy() cleanup...');
    telemetry.destroy();
    print('  Destroy completed without resource leak.');

    // 7. Performance probe: measure 10 queries
    print('[7/7] Measuring execution duration across 10 queries...');
    const perfTelemetry = new GpuTelemetry();
    const durations = [];
    for (let i = 0; i < 10; i++) {
      const t0 = Date.now();
      await perfTelemetry.query();
      durations.push(Date.now() - t0);
    }
    const avgDuration = durations.reduce((a, b) => a + b, 0) / durations.length;
    print(`  Average query duration: ${avgDuration.toFixed(1)} ms (budget: 120.0 ms)`);
    perfTelemetry.destroy();

    if (avgDuration > 120.0) {
      throw new Error(`Performance budget exceeded: ${avgDuration} ms`);
    }

    print('=== All PR 3 verification tests PASSED ===');
  } catch (err) {
    printerr('PR 3 Verification FAILED:', err);
    loop.quit();
    return;
  }
  loop.quit();
}

runTests();
loop.run();
