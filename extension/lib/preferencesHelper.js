export const REFRESH_INTERVALS = [1, 2, 5];

export function getIndexForInterval(val) {
  switch (val) {
    case 1:
      return 0;
    case 2:
      return 1;
    case 5:
      return 2;
    default:
      return 1; // Default fallback to 2s
  }
}

export function getIntervalForIndex(idx) {
  switch (idx) {
    case 0:
      return 1;
    case 1:
      return 2;
    case 2:
      return 5;
    default:
      return 2;
  }
}
