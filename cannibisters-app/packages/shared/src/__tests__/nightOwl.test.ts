import { describe, it, expect } from 'vitest';
import { isNightOwl, hourInZone, msUntilNextFlip } from '../nightOwl';

// 2026-09-03T22:30:00Z is 00:30 SAST (UTC+2)
const justAfterMidnight = new Date('2026-09-03T22:30:00Z');
const lateEvening = new Date('2026-09-03T21:30:00Z'); // 23:30 SAST
const earlyMorning = new Date('2026-09-04T04:59:00Z'); // 06:59 SAST
const sevenAm = new Date('2026-09-04T05:00:00Z');      // 07:00 SAST

describe('night owl window', () => {
  it('reads the hour in Johannesburg', () => {
    expect(hourInZone(justAfterMidnight)).toBe(0);
    expect(hourInZone(lateEvening)).toBe(23);
  });
  it('is active from midnight (inclusive) to 7am (exclusive)', () => {
    expect(isNightOwl(justAfterMidnight)).toBe(true);
    expect(isNightOwl(earlyMorning)).toBe(true);
    expect(isNightOwl(sevenAm)).toBe(false);
    expect(isNightOwl(lateEvening)).toBe(false);
  });
  it('knows when the next flip is', () => {
    const ms = msUntilNextFlip(lateEvening);
    expect(ms).toBeGreaterThan(29 * 60_000);
    expect(ms).toBeLessThanOrEqual(31 * 60_000);
  });
});
