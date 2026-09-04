/** Thin fetch wrapper. When VITE_API_BASE is empty the app runs on built-in mock data. */
export const API_BASE = (import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '');
export const isMock = !API_BASE;

let sessionToken: string | null = null;
export function setSessionToken(token: string | null) { sessionToken = token; }
export function getSessionToken() { return sessionToken; }

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); }
}

export async function http<T>(path: string, init: RequestInit & { json?: unknown } = {}): Promise<T> {
  const { json, headers, ...rest } = init;
  const res = await fetch(`${API_BASE}/api${path}`, {
    ...rest,
    method: rest.method ?? (json !== undefined ? 'POST' : 'GET'),
    headers: {
      Accept: 'application/json',
      ...(json !== undefined ? { 'Content-Type': 'application/json' } : {}),
      ...(sessionToken ? { Authorization: `Bearer ${sessionToken}` } : {}),
      ...(headers as Record<string, string> | undefined),
    },
    body: json !== undefined ? JSON.stringify(json) : rest.body,
  });
  if (!res.ok) {
    let msg = res.statusText;
    try { msg = ((await res.json()) as { message?: string }).message ?? msg; } catch { /* ignore */ }
    throw new ApiError(res.status, msg);
  }
  return (await res.json()) as T;
}

/** Small artificial latency so mock mode feels like a network. */
export const delay = (ms = 220) => new Promise<void>((r) => setTimeout(r, ms));
export const uid = () => Math.random().toString(36).slice(2, 10);

/** Persisted mock state helper (localStorage, namespaced). */
export function mockStore<T>(key: string, initial: T): { get: () => T; set: (v: T) => void } {
  const k = `cb.mock.${key}`;
  return {
    get: () => { try { const raw = localStorage.getItem(k); return raw ? (JSON.parse(raw) as T) : initial; } catch { return initial; } },
    set: (v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* ignore */ } },
  };
}
