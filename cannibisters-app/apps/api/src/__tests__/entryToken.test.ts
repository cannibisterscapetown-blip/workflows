import { describe, it, expect } from 'vitest';
import { issueEntryToken, verifyEntryToken } from '../services/entryToken';
import { signSession, verifySession } from '../lib/session';

describe('entry token', () => {
  const now = Date.parse('2026-09-03T20:00:00Z');
  it('round-trips and expires', () => {
    const t = issueEntryToken(18342, now, 90, 'secret');
    expect(t.token.startsWith('CB1.18342.')).toBe(true);
    expect(verifyEntryToken(t.token, now + 10_000, 'secret')).toMatchObject({ ok: true, memberNumber: 18342 });
    expect(verifyEntryToken(t.token, now + 120_000, 'secret')).toMatchObject({ ok: false, reason: 'expired' });
  });
  it('rejects tampering and wrong secrets', () => {
    const t = issueEntryToken(18342, now, 90, 'secret');
    expect(verifyEntryToken(t.token.replace('18342', '18343'), now, 'secret')).toMatchObject({ ok: false, reason: 'signature' });
    expect(verifyEntryToken(t.token, now, 'other')).toMatchObject({ ok: false, reason: 'signature' });
    expect(verifyEntryToken('nonsense', now, 'secret')).toMatchObject({ ok: false, reason: 'format' });
  });
});

describe('app session', () => {
  it('signs and verifies', () => {
    const exp = Math.floor(Date.now() / 1000) + 60;
    const tok = signSession({ customerId: 'gid://shopify/Customer/1', customerAccessToken: 'abc', email: 'a@b.c', exp }, 's');
    expect(verifySession(tok, 's')?.email).toBe('a@b.c');
    expect(verifySession(tok, 'x')).toBeNull();
    expect(verifySession(tok + 'z', 's')).toBeNull();
  });
});
