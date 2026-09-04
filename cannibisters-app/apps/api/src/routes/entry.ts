import { Hono } from 'hono';
import { DEMO_MEMBER, type EntryPass } from '@cannibisters/shared';
import { isMock } from '../env';
import { issueEntryToken, verifyEntryToken } from '../services/entryToken';
import { loadMember } from './auth';
import type { Vars } from '../app';

export const entry = new Hono<{ Variables: Vars }>();

/** POST /api/entry/pass -> short-lived signed QR payload for the door. */
entry.post('/pass', async (c) => {
  const s = c.get('session');
  const member = isMock ? DEMO_MEMBER : await loadMember(s.customerAccessToken);
  const t = issueEntryToken(member.memberNumber);
  const pass: EntryPass = {
    token: t.token,
    memberNumber: member.memberNumber,
    name: `${member.firstName} ${member.lastName.charAt(0)}.`,
    tier: member.tier,
    membershipStatus: member.membership.status,
    issuedAt: t.issuedAt,
    expiresAt: t.expiresAt,
  };
  return c.json(pass);
});

/** POST /api/entry/verify { token } -> for the door scanner / staff app. */
entry.post('/verify', async (c) => {
  const { token } = (await c.req.json().catch(() => ({}))) as { token?: string };
  if (!token) return c.json({ ok: false, reason: 'format' }, 400);
  const r = verifyEntryToken(token);
  return c.json(r, r.ok ? 200 : 401);
});
