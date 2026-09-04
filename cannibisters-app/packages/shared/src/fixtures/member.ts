import type { Member, Order, EntryPass } from '../types';

export const DEMO_MEMBER: Member = {
  id: 'gid://shopify/Customer/6100000000001',
  firstName: 'Thandi',
  lastName: 'Mokoena',
  email: 'demo@cannibisters.com',
  memberNumber: 18342,
  memberSince: '2023-04-18',
  tier: 'gold',
  membership: { status: 'active', plan: '3 months', expiresAt: '2026-11-12' },
};

export const DEMO_ORDERS: Order[] = [
  { id: 'o1', name: '#48211', date: '2026-08-30', status: 'delivered', total: 575, items: [{ title: 'Red Velvet Gary', qty: 2 }, { title: 'Gelato Frosting Joint', qty: 1 }], pointsEarned: 6900 },
  { id: 'o2', name: '#47903', date: '2026-08-16', status: 'collected', total: 380, items: [{ title: 'Gummy Bears · THC', qty: 1 }, { title: 'Chocolope', qty: 1 }], pointsEarned: 4560 },
  { id: 'o3', name: '#47415', date: '2026-07-29', status: 'delivered', total: 950, items: [{ title: 'Ultimate Canni Resin Vape · Berry Gelato', qty: 1 }], pointsEarned: 11400 },
];

export function demoEntryPass(now = new Date()): EntryPass {
  const exp = new Date(now.getTime() + 90_000);
  return {
    token: `CB1.${DEMO_MEMBER.memberNumber}.${Math.floor(exp.getTime() / 1000)}.demo-signature`,
    memberNumber: DEMO_MEMBER.memberNumber,
    name: `${DEMO_MEMBER.firstName} ${DEMO_MEMBER.lastName.charAt(0)}.`,
    tier: DEMO_MEMBER.tier,
    membershipStatus: DEMO_MEMBER.membership.status,
    issuedAt: now.toISOString(),
    expiresAt: exp.toISOString(),
  };
}
