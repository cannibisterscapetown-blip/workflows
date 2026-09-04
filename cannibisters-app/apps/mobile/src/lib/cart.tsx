import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { COPY, type Product } from '@cannibisters/shared';

export interface CartLine { product: Product; qty: number }

interface CartCtx {
  lines: CartLine[];
  count: number;
  subtotal: number;
  add: (product: Product, qty?: number) => void;
  remove: (variantId: string) => void;
  setQty: (variantId: string, qty: number) => void;
  clear: () => void;
  codes: string[];
  addCode: (code: string) => void;
  removeCode: (code: string) => void;
  freeDeliveryRemaining: number;
}

const Ctx = createContext<CartCtx | null>(null);
const KEY = 'cb.cart';

export function CartProvider({ children }: { children: ReactNode }) {
  const [lines, setLines] = useState<CartLine[]>(() => { try { return JSON.parse(localStorage.getItem(KEY) ?? '[]'); } catch { return []; } });
  const [codes, setCodes] = useState<string[]>(() => { try { return JSON.parse(localStorage.getItem(KEY + '.codes') ?? '[]'); } catch { return []; } });

  useEffect(() => { try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch { /* ignore */ } }, [lines]);
  useEffect(() => { try { localStorage.setItem(KEY + '.codes', JSON.stringify(codes)); } catch { /* ignore */ } }, [codes]);

  const value = useMemo<CartCtx>(() => {
    const subtotal = lines.reduce((s, l) => s + l.product.price * l.qty, 0);
    return {
      lines,
      count: lines.reduce((s, l) => s + l.qty, 0),
      subtotal,
      add: (product, qty = 1) => setLines((ls) => {
        const i = ls.findIndex((l) => l.product.variantId === product.variantId);
        if (i === -1) return [...ls, { product, qty }];
        const copy = [...ls]; copy[i] = { product, qty: copy[i]!.qty + qty }; return copy;
      }),
      remove: (variantId) => setLines((ls) => ls.filter((l) => l.product.variantId !== variantId)),
      setQty: (variantId, qty) => setLines((ls) => qty <= 0 ? ls.filter((l) => l.product.variantId !== variantId) : ls.map((l) => (l.product.variantId === variantId ? { ...l, qty } : l))),
      clear: () => { setLines([]); setCodes([]); },
      codes,
      addCode: (code) => setCodes((cs) => (cs.includes(code) ? cs : [...cs, code])),
      removeCode: (code) => setCodes((cs) => cs.filter((c) => c !== code)),
      freeDeliveryRemaining: Math.max(0, COPY.freeDeliveryThreshold - subtotal),
    };
  }, [lines, codes]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useCart(): CartCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useCart outside CartProvider');
  return ctx;
}
