import type { TierKey } from './types';

/**
 * Programme constants mirrored from the live loyalty bundle (1 Sep 2026).
 * Confirm BASE_RATE / REDEEM_RATE / diamond threshold against the loyalty backend config.
 */
export const BASE_RATE_PTS_PER_RAND = 10;   // points earned per R1, before tier multiplier
export const REDEEM_RATE_PTS_PER_RAND = 100; // points per R1 of reward value
export const POINTS_VALID_DAYS = 365;
export const TIER_WINDOW_DAYS = 180;
export const CANNISINO_MIN_STAKE = 500;

export interface TierMeta { key: TierKey; label: string; threshold: number; multiplier: number; discount: number }

export const TIER_ORDER: TierKey[] = ['silver', 'gold', 'platinum', 'diamond'];

export const TIERS: Record<TierKey, TierMeta> = {
  silver: { key: 'silver', label: 'Silver', threshold: 0, multiplier: 1.0, discount: 0 },
  gold: { key: 'gold', label: 'Gold', threshold: 10_000, multiplier: 1.2, discount: 10 },
  platinum: { key: 'platinum', label: 'Platinum', threshold: 20_000, multiplier: 1.4, discount: 20 },
  diamond: { key: 'diamond', label: 'Diamond', threshold: 40_000, multiplier: 1.7, discount: 25 },
};

export function tierForSpend(spend180d: number): TierKey {
  let tier: TierKey = 'silver';
  for (const key of TIER_ORDER) if (spend180d >= TIERS[key].threshold) tier = key;
  return tier;
}

export function tierProgress(spend180d: number): { tier: TierKey; nextTier?: TierKey; amountToNext?: number; pct: number } {
  const tier = tierForSpend(spend180d);
  const idx = TIER_ORDER.indexOf(tier);
  const next = TIER_ORDER[idx + 1];
  if (!next) return { tier, pct: 100 };
  const from = TIERS[tier].threshold;
  const to = TIERS[next].threshold;
  const pct = Math.max(0, Math.min(100, Math.round(((spend180d - from) / (to - from)) * 100)));
  return { tier, nextTier: next, amountToNext: Math.max(0, to - spend180d), pct };
}

export function pointsForSpend(rand: number, tier: TierKey): number {
  return Math.round(rand * BASE_RATE_PTS_PER_RAND * TIERS[tier].multiplier);
}

export function randValueOfPoints(points: number): number {
  return Math.floor(points / REDEEM_RATE_PTS_PER_RAND);
}

export function formatPoints(points: number): string {
  return new Intl.NumberFormat('en-ZA').format(Math.round(points));
}

export function formatRand(amount: number): string {
  const whole = Number.isInteger(amount);
  return 'R' + new Intl.NumberFormat('en-ZA', { minimumFractionDigits: whole ? 0 : 2, maximumFractionDigits: 2 }).format(amount).replace(/\s/g, ',');
}
