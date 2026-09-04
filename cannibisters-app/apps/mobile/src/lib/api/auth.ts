import { DEMO_MEMBER, type Member } from '@cannibisters/shared';
import { http, isMock, delay, setSessionToken } from './http';

export interface SignInResult { token: string; member: Member }

/**
 * Sign in with the member's cannibisters.com email + password.
 * Live: BFF exchanges credentials via Storefront `customerAccessTokenCreate` and returns an app session.
 * Mock: any email works with password "demo". Emails containing "new" get a pending membership,
 * "lapsed" an expired one, so every entry state can be demoed.
 */
export async function signIn(email: string, password: string): Promise<SignInResult> {
  if (isMock) {
    await delay(650);
    if (!email.includes('@')) throw new Error('Enter the email you use on cannibisters.com.');
    if (password !== 'demo' && password.length < 6) throw new Error('That password does not match. Try again or reset it.');
    const lower = email.toLowerCase();
    const member: Member = {
      ...DEMO_MEMBER,
      email,
      membership: lower.includes('new')
        ? { status: 'none', plan: 'Application pending' }
        : lower.includes('lapsed')
          ? { status: 'expired', plan: '30 days', expiresAt: '2026-08-20' }
          : DEMO_MEMBER.membership,
    };
    const token = `mock.${btoa(email)}.${Date.now()}`;
    setSessionToken(token);
    return { token, member };
  }
  const r = await http<SignInResult>('/auth/login', { json: { email, password } });
  setSessionToken(r.token);
  return r;
}

export async function fetchMe(): Promise<Member> {
  if (isMock) { await delay(120); return DEMO_MEMBER; }
  return http<Member>('/auth/me');
}

export async function signOut(): Promise<void> {
  if (!isMock) { try { await http('/auth/logout', { method: 'POST' }); } catch { /* ignore */ } }
  setSessionToken(null);
}
