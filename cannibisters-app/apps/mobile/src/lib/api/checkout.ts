import { DAY_PASS_VARIANT_ID, type CartLineInput, type CheckoutHandoff } from '@cannibisters/shared';
import { http, isMock, delay } from './http';

/**
 * Create a Shopify cart for the signed-in member and return the checkout URL.
 * Live: BFF `cartCreate` + `cartBuyerIdentityUpdate` (customer access token) so checkout is already signed in.
 * The membership gate mirrors the website: checkout needs an active membership or a day pass in the basket.
 */
export async function createCheckout(lines: CartLineInput[], discountCodes: string[] = []): Promise<CheckoutHandoff> {
  if (isMock) {
    await delay(500);
    const ids = lines.map((l) => `${l.variantId.split('/').pop()}:${l.quantity}`).join(',');
    const q = discountCodes.length ? `?discount=${encodeURIComponent(discountCodes[0]!)}` : '';
    return { checkoutUrl: `https://cannibisters.com/cart/${ids}${q}`, requiresMembership: false, dayPassVariantId: DAY_PASS_VARIANT_ID };
  }
  return http<CheckoutHandoff>('/cart/checkout', { json: { lines, discountCodes } });
}
