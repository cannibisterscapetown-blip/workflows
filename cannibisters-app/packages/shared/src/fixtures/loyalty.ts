import type { LoyaltySummary, Reward, PointEvent } from '../types';
import { tierProgress, TIERS, randValueOfPoints } from '../loyalty';

export const DEMO_REWARDS: Reward[] = [
  { id: 'r-pre-roll', title: 'Free pre-roll', description: 'Any premium top-shelf joint, on the house.', cost: 15_000, kind: 'product', valueRand: 150 },
  { id: 'r-10off', title: '10% off your next order', description: 'Applied at checkout. Online or in store.', cost: 8_000, kind: 'discount' },
  { id: 'r-100', title: 'R100 in-store credit', description: 'A voucher for the counter at Regent Road.', cost: 10_000, kind: 'voucher', valueRand: 100 },
  { id: 'r-gram', title: 'A gram of the flower of the week', description: 'This week: Rock Star.', cost: 20_000, kind: 'product', valueRand: 200 },
  { id: 'r-app-drink', title: 'Infused drink at the bar', description: 'App members only. Show the code at the bar.', cost: 6_000, kind: 'experience', appOnly: true },
  { id: 'r-hat', title: 'Cannibisters bucket hat', description: 'Members merch. Limited run.', cost: 35_000, kind: 'product', valueRand: 350 },
];

export const DEMO_HISTORY: PointEvent[] = [
  { id: 'h1', date: '2026-08-30', label: 'Order #48211', delta: 6900, kind: 'earn' },
  { id: 'h2', date: '2026-08-24', label: 'Wheel of Fortune', delta: 2500, kind: 'game' },
  { id: 'h3', date: '2026-08-16', label: 'Order #47903', delta: 4560, kind: 'earn' },
  { id: 'h4', date: '2026-08-10', label: 'Redeemed 10% off', delta: -8000, kind: 'redeem' },
  { id: 'h5', date: '2026-08-01', label: 'Referral · Sipho joined', delta: 2500, kind: 'bonus' },
  { id: 'h6', date: '2026-07-29', label: 'Order #47415', delta: 11400, kind: 'earn' },
  { id: 'h7', date: '2026-07-12', label: 'Birthday month', delta: 1000, kind: 'bonus' },
];

export function demoLoyalty(): LoyaltySummary {
  const spend180d = 12_640;
  const points = 42_860;
  const tp = tierProgress(spend180d);
  return {
    points,
    pointsValueRand: randValueOfPoints(points),
    tier: tp.tier,
    multiplier: TIERS[tp.tier].multiplier,
    tierProgress: { spend180d, nextTier: tp.nextTier, amountToNext: tp.amountToNext, pct: tp.pct },
    expiringSoon: { points: 1_200, on: '2026-09-30' },
    history: DEMO_HISTORY,
    rewards: DEMO_REWARDS,
    playWallet: 3_500,
    referralCode: 'THANDI-1834',
  };
}
