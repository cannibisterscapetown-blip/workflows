import type { CannisinoGame, WheelPrize } from '../types';

export const CANNISINO_GAMES: CannisinoGame[] = [
  { key: 'wheel', title: 'Wheel of Fortune', tagline: 'Spin the house wheel for member prizes.', native: true },
  { key: 'predictions', title: 'Predictions', tagline: 'Pick a winner, or call the exact score, on real fixtures.', native: false, minStake: 500 },
  { key: 'claw', title: 'Claw Machine', tagline: 'Send the claw down and see what it brings back.', native: false, minStake: 500 },
  { key: 'mines', title: 'Mines', tagline: 'Clear the board square by square. Bank your run before you hit a mine.', native: false, minStake: 500 },
];

/** Wheel prize tables by tier, adapted from the club's Wheel of Fortune. */
export const WHEEL_PRIZES: Record<'silver' | 'gold' | 'platinum' | 'diamond', WheelPrize[]> = {
  silver: [
    { label: 'Free pre-roll', kind: 'product' }, { label: '5% off', kind: 'discount', value: 5 }, { label: 'Lighter', kind: 'product' },
    { label: 'One Hit Wonder puff', kind: 'product' }, { label: 'Strain sample', kind: 'product' }, { label: '5,000 points', kind: 'points', value: 5000 },
    { label: 'Canni water', kind: 'product' }, { label: 'Hot or cold drink', kind: 'product' }, { label: 'Snack', kind: 'product' }, { label: 'Spin again', kind: 'points', value: 0 },
  ],
  gold: [
    { label: '10% off', kind: 'discount', value: 10 }, { label: 'Strain sample', kind: 'product' }, { label: 'One Hit Wonder puff', kind: 'product' },
    { label: 'One Hit Wonder capsule', kind: 'product' }, { label: 'Bucket hat', kind: 'product' }, { label: 'Free pre-roll', kind: 'product' },
    { label: '10,000 points', kind: 'points', value: 10000 }, { label: 'Infused drink', kind: 'product' }, { label: 'Snack', kind: 'product' }, { label: 'Lighter', kind: 'product' },
  ],
  platinum: [
    { label: 'Infused drink', kind: 'product' }, { label: 'Strain sample', kind: 'product' }, { label: 'Bucket hat', kind: 'product' },
    { label: '15% off', kind: 'discount', value: 15 }, { label: '15,000 points', kind: 'points', value: 15000 }, { label: 'Free Moonstick', kind: 'product' },
    { label: '30mg rosin capsule', kind: 'product' }, { label: '20mg edibles', kind: 'product' }, { label: 'Dab hit', kind: 'product' }, { label: 'Indoor pre-roll', kind: 'product' },
  ],
  diamond: [
    { label: '20% off', kind: 'discount', value: 20 }, { label: '20,000 points', kind: 'points', value: 20000 }, { label: 'Free Moonstick', kind: 'product' },
    { label: 'Bucket hat', kind: 'product' }, { label: 'Infused drink', kind: 'product' }, { label: 'Strain sample', kind: 'product' },
    { label: '30mg rosin capsule', kind: 'product' }, { label: 'Dab hit', kind: 'product' }, { label: 'Indoor pre-roll', kind: 'product' }, { label: 'Consultation credit', kind: 'product' },
  ],
};
