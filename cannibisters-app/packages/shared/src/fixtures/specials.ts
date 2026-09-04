import type { Special } from '../types';

const CDN = 'https://cdn.shopify.com/s/files/1/0631/7749/0644';

export const DEMO_SPECIALS: Special[] = [
  { id: 's-app-first', kind: 'app-only', title: 'R50 off your first app order', subtitle: 'A welcome from the Club', description: 'Order through the app once and R50 comes off at checkout. Minimum R300.', code: 'CB-APP-WELCOME', savings: 'Save R50', nudge: 'Applied automatically on your first app order.' },
  { id: 's-app-gram', kind: 'app-only', title: 'Third gram on the house', subtitle: 'Flower, app only', description: 'Add any three grams of flower and the third is free. Weekdays only.', code: 'CB-APP-3FOR2', collectionHandle: 'premium-bud', image: `${CDN}/collections/Cherry_Pie.png?v=1713855900`, savings: 'Save R200', endsAt: '2026-09-30', nudge: 'Two grams in your basket. One more and it is free.' },
  { id: 's-night', kind: 'night-owl', title: 'Night Owl · 15% off', subtitle: 'Midnight to 7am', description: 'The apothecary keeps later hours than the city does. Order between midnight and 7am and take 15% off.', code: 'NIGHTOWL15', savings: '15% off', image: `${CDN}/files/night-owl-gold-360.png?v=1788083361`, nudge: 'The quiet hours belong to the members who keep them.' },
  { id: 's-sept', kind: 'monthly', title: 'September specials', subtitle: 'Rosin flower hits · R75', description: 'Ask at the counter, 65 Regent Rd. Online special on selected flower all month.', collectionHandle: 'specials', savings: 'From R75', endsAt: '2026-09-30' },
  { id: 's-gold', kind: 'tier', title: 'Gold members · 10% off every order', subtitle: 'Your tier, your rate', description: 'Gold members save 10% on every order. Platinum saves 20%.', savings: '10% off', nudge: 'R7,360 more in the next 180 days and Platinum is yours.' },
];
