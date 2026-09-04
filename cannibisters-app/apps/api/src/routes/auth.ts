import { Hono } from 'hono';
import { z } from 'zod';
import { DEMO_MEMBER, type Member } from '@cannibisters/shared';
import { isMock } from '../env';
import { signSession, type SessionPayload } from '../lib/session';
import { storefront, Q } from '../adapters/shopifyStorefront';
import type { Vars } from '../app';

const LoginInput = z.object({ email: z.string().email(), password: z.string().min(1) });

export const auth = new Hono<{ Variables: Vars }>();

/** POST /api/auth/login  -> { token, member } using the member's website credentials. */
auth.post('/login', async (c) => {
  const body = LoginInput.safeParse(await c.req.json().catch(() => ({})));
  if (!body.success) return c.json({ message: 'Enter your email and password.' }, 400);
  const { email, password } = body.data;

  if (isMock) {
    if (password !== 'demo') return c.json({ message: 'That password does not match. Try again or reset it.' }, 401);
    return c.json({ token: `mock.${Buffer.from(email).toString('base64')}`, member: { ...DEMO_MEMBER, email } });
  }

  type R = { customerAccessTokenCreate: { customerAccessToken: { accessToken: string; expiresAt: string } | null; customerUserErrors: { message: string }[] } };
  const r = await storefront<R>(Q.customerAccessTokenCreate, { input: { email, password } });
  const tok = r.customerAccessTokenCreate.customerAccessToken;
  if (!tok) return c.json({ message: r.customerAccessTokenCreate.customerUserErrors[0]?.message ?? 'Those details did not match.' }, 401);
  const member = await loadMember(tok.accessToken);
  const payload: SessionPayload = { customerId: member.id, customerAccessToken: tok.accessToken, email: member.email, exp: Math.floor(Date.parse(tok.expiresAt) / 1000) };
  return c.json({ token: signSession(payload), member });
});

auth.get('/me', async (c) => {
  const h = c.req.header('Authorization') ?? '';
  if (isMock || h.includes('mock.')) return c.json(DEMO_MEMBER);
  const { verifySession } = await import('../lib/session');
  const s = verifySession(h.replace('Bearer ', ''));
  if (!s) return c.json({ message: 'Sign in to continue.' }, 401);
  return c.json(await loadMember(s.customerAccessToken));
});

auth.post('/logout', (c) => c.json({ ok: true }));

/** Map a Storefront customer to the app's Member shape. Extend once the member-number source is confirmed. */
export async function loadMember(customerAccessToken: string): Promise<Member> {
  type R = { customer: { id: string; email: string; firstName: string | null; lastName: string | null; createdAt: string; tags: string[]; memberNumber: { value: string } | null; bonTier: { value: string } | null; bonStatus: { value: string } | null } | null };
  const r = await storefront<R>(Q.customer, { token: customerAccessToken });
  if (!r.customer) throw new Error('Session expired. Sign in again.');
  const cu = r.customer;
  const tierRaw = (cu.bonTier?.value ?? 'silver').toLowerCase();
  const tier = (['silver', 'gold', 'platinum', 'diamond'] as const).find((t) => tierRaw.includes(t)) ?? 'silver';
  // Membership status: TODO confirm source (Locksmith tag, membership order, or Customer Fields). Tags are a common convention.
  const active = cu.tags.some((t) => /member|active/i.test(t));
  return {
    id: cu.id,
    firstName: cu.firstName ?? '',
    lastName: cu.lastName ?? '',
    email: cu.email,
    memberNumber: Number(cu.memberNumber?.value ?? cu.id.split('/').pop()?.slice(-5) ?? 0),
    memberSince: cu.createdAt,
    tier,
    membership: { status: active ? 'active' : 'expired', plan: active ? 'Member' : 'Lapsed' },
  };
}
