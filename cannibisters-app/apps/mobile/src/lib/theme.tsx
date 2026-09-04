import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { isNightOwl, msUntilNextFlip } from '@cannibisters/shared';
import { localNightOwlStatus } from './api/nightowl';

/**
 * Day / Night theme. Night = the Night Owl window (00:00-07:00 Africa/Johannesburg).
 * `preview` lets a member (or a screenshot run via ?night=1) force a mode.
 */
export type ThemeMode = 'day' | 'night';

interface ThemeCtx {
  mode: ThemeMode;
  isNight: boolean;
  natural: boolean;          // what the clock says
  preview: ThemeMode | null; // manual override
  setPreview: (m: ThemeMode | null) => void;
  nextFlipAt: Date;
  /** The Night Owl takeover animation plays once per visit to night mode. */
  takeoverPending: boolean;
  dismissTakeover: () => void;
  status: ReturnType<typeof localNightOwlStatus>;
}

const Ctx = createContext<ThemeCtx | null>(null);
const PREVIEW_KEY = 'cb.theme.preview';

function readPreview(): ThemeMode | null {
  try {
    const q = new URLSearchParams(window.location.search).get('night');
    if (q === '1') return 'night';
    if (q === '0') return 'day';
    const v = localStorage.getItem(PREVIEW_KEY);
    return v === 'night' || v === 'day' ? v : null;
  } catch { return null; }
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [natural, setNatural] = useState(() => isNightOwl());
  const [preview, setPreviewState] = useState<ThemeMode | null>(readPreview);
  const [takeoverPending, setTakeoverPending] = useState(false);
  const [lastMode, setLastMode] = useState<ThemeMode | null>(null);

  useEffect(() => {
    let t: ReturnType<typeof setTimeout>;
    const tick = () => { setNatural(isNightOwl()); t = setTimeout(tick, Math.min(msUntilNextFlip() + 500, 60_000)); };
    tick();
    const vis = () => setNatural(isNightOwl());
    document.addEventListener('visibilitychange', vis);
    return () => { clearTimeout(t); document.removeEventListener('visibilitychange', vis); };
  }, []);

  const isNight = preview ? preview === 'night' : natural;
  const mode: ThemeMode = isNight ? 'night' : 'day';

  useEffect(() => {
    document.documentElement.dataset.theme = mode;
    document.body.classList.toggle('grain', mode === 'night');
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', mode === 'night' ? '#05060c' : '#F8F4EA');
    if (mode === 'night' && lastMode !== 'night') {
      const suppress = new URLSearchParams(window.location.search).get('takeover') === '0';
      setTakeoverPending(!suppress);
    }
    setLastMode(mode);
  }, [mode, lastMode]);

  const value = useMemo<ThemeCtx>(() => ({
    mode, isNight, natural, preview,
    setPreview: (m) => { setPreviewState(m); try { m ? localStorage.setItem(PREVIEW_KEY, m) : localStorage.removeItem(PREVIEW_KEY); } catch { /* ignore */ } },
    nextFlipAt: new Date(Date.now() + msUntilNextFlip()),
    takeoverPending,
    dismissTakeover: () => setTakeoverPending(false),
    status: localNightOwlStatus(),
  }), [mode, isNight, natural, preview, takeoverPending]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useTheme(): ThemeCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useTheme outside ThemeProvider');
  return ctx;
}
