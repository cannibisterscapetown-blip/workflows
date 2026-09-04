import { Hono } from 'hono';
import { DEMO_ORDERS, DEMO_SPECIALS, DAY_PASS_VARIANT_ID, isNightOwl, msUntilNextFlip, NIGHT_OWL_TZ, type NightOwlStatus } from '@cannibisters/shared';
import { env, isMock } from '../env';
import { storefront, Q } from '../adapters/shopifyStorefront';
import type { Vars } from '../app';

const pub = new Hono<{ Variables: Vars }>();
const member = new Hono<{ Variables: Vars }>();

pub.get('/nightowl/status', (c) => {
  const now = new Date();
  const opts = { startHour: env.nightOwlStart, endHour: env.nightOwlEnd };
  const status: NightOwlStatus = {
    active: isNightOwl(now, opts), startHour: env.nightOwlStart, endHour: env.nightOwlEnd, timeZone: NIGHT_OWL_TZ,
    discountCode: env.nightOwlCode, discountPct: 15, nextChangeAt: new Date(now.getTime() + msUntilNextFlip(now, opts)).toISOString(),
  };
  return c.json(status);
});

member.get('/specials', (c) => c.json(DEMO_SPECIALS));
member.get('/orders', (c) => c.json(DEMO_ORDERS));

/** POST /api/cart/checkout { lines, discountCodes } -> { checkoutUrl } signed in as the member. */
member.post('/cart/checkout', async (c) => {
  const s = c.get('session');
  const body = (await c.req.json().catch(() => ({}))) as { lines?: { variantId: string; quantity: number }[]; discountCodes?: string[] };
  const lines = (body.lines ?? []).filter((l) => l.variantId && l.quantity > 0);
  if (!lines.length) return c.json({ message: 'Your basket is empty.' }, 400);
  if (isMock) {
    const ids = lines.map((l) => `${l.variantId.split('/').pop()}:${l.quantity}`).join(',');
    return c.json({ checkoutUrl: `https://cannibisters.com/cart/${ids}`, requiresMembership: false, dayPassVariantId: DAY_PASS_VARIANT_ID });
  }
  type R = { cartCreate: { cart: { id: string; checkoutUrl: string } | null; userErrors: { message: string }[] } };
  const r = await storefront<R>(Q.cartCreate, {
    input: {
      lines: lines.map((l) => ({ merchandiseId: l.variantId, quantity: l.quantity })),
      discountCodes: body.discountCodes ?? [],
      buyerIdentity: { customerAccessToken: s.customerAccessToken, email: s.email, countryCode: 'ZA' },
    },
  });
  if (!r.cartCreate.cart) return c.json({ message: r.cartCreate.userErrors[0]?.message ?? 'Could not start checkout.' }, 400);
  return c.json({ checkoutUrl: r.cartCreate.cart.checkoutUrl, requiresMembership: false, dayPassVariantId: DAY_PASS_VARIANT_ID });
});

export const misc = { public: pub, member };
