import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import type { Member } from '@cannibisters/shared';
import { signIn as apiSignIn, signOut as apiSignOut, fetchMe } from './api/auth';
import { setSessionToken, isMock } from './api/http';

const KEY = 'cb.session';

interface SessionState { status: 'loading' | 'anon' | 'member'; member: Member | null; token: string | null }
interface SessionCtx extends SessionState {
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  refresh: () => Promise<void>;
  /** Mock-only: patch the member for demos (e.g. after adding a day pass). */
  patchMember: (patch: Partial<Member>) => void;
}

const Ctx = createContext<SessionCtx | null>(null);

function load(): { token: string; member: Member } | null {
  try { const raw = localStorage.getItem(KEY); return raw ? JSON.parse(raw) : null; } catch { return null; }
}
function save(v: { token: string; member: Member } | null) {
  try { v ? localStorage.setItem(KEY, JSON.stringify(v)) : localStorage.removeItem(KEY); } catch { /* ignore */ }
}

export function SessionProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<SessionState>(() => {
    const saved = load();
    if (saved) { setSessionToken(saved.token); return { status: 'member', member: saved.member, token: saved.token }; }
    return { status: 'anon', member: null, token: null };
  });

  const refresh = useCallback(async () => {
    if (!state.token) return;
    try {
      const member = await fetchMe();
      setState((s) => ({ ...s, member: isMock ? s.member : member }));
      if (!isMock) save({ token: state.token, member });
    } catch { /* keep cached member */ }
  }, [state.token]);

  useEffect(() => { void refresh(); }, [refresh]);

  const value = useMemo<SessionCtx>(() => ({
    ...state,
    signIn: async (email, password) => {
      const r = await apiSignIn(email, password);
      save(r);
      setState({ status: 'member', member: r.member, token: r.token });
    },
    signOut: async () => {
      await apiSignOut();
      save(null);
      setState({ status: 'anon', member: null, token: null });
    },
    refresh,
    patchMember: (patch) => setState((s) => {
      if (!s.member) return s;
      const member = { ...s.member, ...patch };
      if (s.token) save({ token: s.token, member });
      return { ...s, member };
    }),
  }), [state, refresh]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useSession(): SessionCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useSession outside SessionProvider');
  return ctx;
}

/** Convenience: the signed-in member (throws if used on an unauthenticated route). */
export function useMember(): Member {
  const { member } = useSession();
  if (!member) throw new Error('useMember on an unauthenticated route');
  return member;
}

export function RequireMember({ children }: { children: ReactNode }) {
  const { status } = useSession();
  const loc = useLocation();
  if (status === 'loading') return null;
  if (status === 'anon') return <Navigate to="/sign-in" replace state={{ from: loc.pathname }} />;
  return <>{children}</>;
}
