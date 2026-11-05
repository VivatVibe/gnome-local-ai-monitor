import {
  REFRESH_INTERVALS,
  getIndexForInterval,
  getIntervalForIndex,
} from '../extension/lib/preferencesHelper.js';

function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

console.log('Testing Preferences Refresh Rate Interval Mapping...');

// Test 1: Supported choices
assert(REFRESH_INTERVALS.length === 3, 'REFRESH_INTERVALS must contain exactly 3 choices');
assert(REFRESH_INTERVALS[0] === 1, 'Choice 0 must be 1s');
assert(REFRESH_INTERVALS[1] === 2, 'Choice 1 must be 2s');
assert(REFRESH_INTERVALS[2] === 5, 'Choice 2 must be 5s');

// Test 2: getIndexForInterval
assert(getIndexForInterval(1) === 0, '1s should map to index 0');
assert(getIndexForInterval(2) === 1, '2s should map to index 1');
assert(getIndexForInterval(5) === 2, '5s should map to index 2');
assert(getIndexForInterval(3) === 1, 'Unrecognized interval 3s should fallback to index 1 (2s)');
assert(getIndexForInterval(10) === 1, 'Unrecognized interval 10s should fallback to index 1 (2s)');

// Test 3: getIntervalForIndex
assert(getIntervalForIndex(0) === 1, 'Index 0 should map to 1s');
assert(getIntervalForIndex(1) === 2, 'Index 1 should map to 2s');
assert(getIntervalForIndex(2) === 5, 'Index 2 should map to 5s');
assert(getIntervalForIndex(99) === 2, 'Out of bounds index should fallback to 2s');

console.log('PASS: All Preferences Refresh Rate unit tests passed (3 suites).');
