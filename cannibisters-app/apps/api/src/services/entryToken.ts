import { hmac, safeEqual } from '../lib/signing';
import { env } from '../env';

/**
 * Member entry QR payload: `CB1.<memberNumber>.<exp>.<sig>`
 *  - CB1: format version
 *  - memberNumber: the club's member number (what the door already knows)
 *  - exp: unix seconds; passes are short-lived (default 90s) and refreshed by the app
 *  - sig: HMAC-SHA256 over "CB1.<memberNumber>.<exp>" with ENTRY_TOKEN_SECRET
 * The door scanner verifies the signature and expiry offline, then checks membership status.
 * ASSUMPTION to confirm from the club's notes: the current site's QR encodes the member number;
 * if it encodes something else, change `payloadOf` and keep the signing.
 */
export const ENTRY_TTL_SEC = 90;

function payloadOf(memberNumber: number, exp: number) { return `CB1.${memberNumber}.${exp}`; }

export function issueEntryToken(memberNumber: number, now = Date.now(), ttlSec = ENTRY_TTL_SEC, secret = env.entryTokenSecret) {
  const exp = Math.floor(now / 1000) + ttlSec;
  const payload = payloadOf(memberNumber, exp);
  return { token: `${payload}.${hmac(secret, payload)}`, exp, issuedAt: new Date(now).toISOString(), expiresAt: new Date(exp * 1000).toISOString() };
}

export function verifyEntryToken(token: string, now = Date.now(), secret = env.entryTokenSecret): { ok: true; memberNumber: number; exp: number } | { ok: false; reason: 'format' | 'signature' | 'expired' } {
  const parts = token.split('.');
  if (parts.length !== 4 || parts[0] !== 'CB1') return { ok: false, reason: 'format' };
  const memberNumber = Number(parts[1]); const exp = Number(parts[2]);
  if (!Number.isInteger(memberNumber) || !Number.isInteger(exp)) return { ok: false, reason: 'format' };
  if (!safeEqual(hmac(secret, payloadOf(memberNumber, exp)), parts[3]!)) return { ok: false, reason: 'signature' };
  if (exp * 1000 < now) return { ok: false, reason: 'expired' };
  return { ok: true, memberNumber, exp };
}
