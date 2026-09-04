const e = process.env;

export const env = {
  port: Number(e.PORT ?? 8787),
  shopDomain: e.SHOPIFY_STORE_DOMAIN ?? 'cannibisters.myshopify.com',
  storefrontToken: e.SHOPIFY_STOREFRONT_TOKEN ?? '',
  storefrontVersion: e.SHOPIFY_STOREFRONT_API_VERSION ?? '2025-07',
  adminToken: e.SHOPIFY_ADMIN_TOKEN ?? '',
  adminVersion: e.SHOPIFY_ADMIN_API_VERSION ?? '2025-07',
  bonApiUrl: e.BON_API_URL ?? 'https://graph.bonloyalty.com/graphql',
  bonApiToken: e.BON_API_TOKEN ?? '',
  loyaltyApiBase: e.LOYALTY_API_BASE ?? 'https://cannibisters-loyalty.vercel.app',
  cannisinoEmbedBase: e.CANNISINO_EMBED_BASE ?? 'https://cannisino.vercel.app',
  entryTokenSecret: e.ENTRY_TOKEN_SECRET ?? 'dev-entry-secret',
  sessionSecret: e.APP_SESSION_SECRET ?? 'dev-session-secret',
  nightOwlStart: Number(e.NIGHT_OWL_START_HOUR ?? 0),
  nightOwlEnd: Number(e.NIGHT_OWL_END_HOUR ?? 7),
  nightOwlCode: e.NIGHT_OWL_DISCOUNT_CODE ?? 'NIGHTOWL15',
  corsOrigin: e.CORS_ORIGIN ?? '*',
};

/** Mock mode: no Storefront token configured. Fixtures from @cannibisters/shared are served. */
export const isMock = !env.storefrontToken;
