import { b64url, fromB64url, hmac, safeEqual } from './signing';
import { env } from '../env';

/**
 * App session token: `<payload>.<sig>` where payload is base64url JSON.
 * Carries the Shopify customer id + the Storefront customer access token so the BFF can act for the member.
 */
export interface SessionPayload {
  customerId: string;          // gid://shopify/Customer/...
  customerAccessToken: string; // Storefront token (classic accounts)
  email: string;
  exp: number;                 // unix seconds
}

export function signSession(p: SessionPayload, secret = env.sessionSecret): string {
  const body = b64url(JSON.stringify(p));
  return `${body}.${hmac(secret, body)}`;
}

export function verifySession(token: string, secret = env.sessionSecret, now = Date.now()): SessionPayload | null {
  const [body, sig] = token.split('.');
  if (!body || !sig || !safeEqual(hmac(secret, body), sig)) return null;
  try {
    const p = JSON.parse(fromB64url(body).toString('utf8')) as SessionPayload;
    if (typeof p.exp !== 'number' || p.exp * 1000 < now) return null;
    return p;
  } catch { return null; }
}
