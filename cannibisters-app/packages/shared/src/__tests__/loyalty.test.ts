import { describe, it, expect } from 'vitest';
import { tierForSpend, tierProgress, pointsForSpend, randValueOfPoints, formatRand } from '../loyalty';

describe('loyalty maths', () => {
  it('assigns tiers by 180-day spend', () => {
    expect(tierForSpend(0)).toBe('silver');
    expect(tierForSpend(9_999)).toBe('silver');
    expect(tierForSpend(10_000)).toBe('gold');
    expect(tierForSpend(25_000)).toBe('platinum');
    expect(tierForSpend(50_000)).toBe('diamond');
  });
  it('reports progress to the next tier', () => {
    const p = tierProgress(15_000);
    expect(p.tier).toBe('gold');
    expect(p.nextTier).toBe('platinum');
    expect(p.amountToNext).toBe(5_000);
    expect(p.pct).toBe(50);
    expect(tierProgress(60_000).nextTier).toBeUndefined();
  });
  it('multiplies points by tier', () => {
    expect(pointsForSpend(100, 'silver')).toBe(1000);
    expect(pointsForSpend(100, 'gold')).toBe(1200);
  });
  it('values points in Rand', () => {
    expect(randValueOfPoints(42_860)).toBe(428);
    expect(formatRand(1000)).toBe('R1,000');
    expect(formatRand(12.5)).toBe('R12.50');
  });
});
