import { env } from '../env';

/** Storefront API client (Headless channel token). Classic customer accounts. */
export async function storefront<T>(query: string, variables: Record<string, unknown> = {}, buyerToken?: string): Promise<T> {
  const res = await fetch(`https://${env.shopDomain}/api/${env.storefrontVersion}/graphql.json`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Shopify-Storefront-Access-Token': env.storefrontToken,
      ...(buyerToken ? { 'Shopify-Storefront-Buyer-IP': '', 'X-Shopify-Customer-Access-Token': buyerToken } : {}),
    },
    body: JSON.stringify({ query, variables }),
  });
  const json = (await res.json()) as { data?: T; errors?: { message: string }[] };
  if (!res.ok || json.errors?.length) throw new Error(json.errors?.map((e) => e.message).join('; ') || `Storefront ${res.status}`);
  return json.data as T;
}

export const Q = {
  customerAccessTokenCreate: `mutation Login($input: CustomerAccessTokenCreateInput!) {
    customerAccessTokenCreate(input: $input) {
      customerAccessToken { accessToken expiresAt }
      customerUserErrors { code field message }
    }
  }`,
  customerAccessTokenRenew: `mutation Renew($token: String!) {
    customerAccessTokenRenew(customerAccessToken: $token) { customerAccessToken { accessToken expiresAt } userErrors { message } }
  }`,
  customer: `query Me($token: String!) {
    customer(customerAccessToken: $token) {
      id email firstName lastName createdAt tags
      memberNumber: metafield(namespace: "custom", key: "member_number") { value }
      bonPoints: metafield(namespace: "klaviyo", key: "bon_point") { value }
      bonTier: metafield(namespace: "klaviyo", key: "bon_vip_tier") { value }
      bonStatus: metafield(namespace: "klaviyo", key: "bon_member_status") { value }
      orders(first: 10, sortKey: PROCESSED_AT, reverse: true) {
        edges { node { id name processedAt financialStatus fulfillmentStatus totalPrice { amount } lineItems(first: 10) { edges { node { title quantity } } } } }
      }
    }
  }`,
  products: `query Products($first: Int!, $query: String, $after: String) {
    products(first: $first, query: $query, after: $after, sortKey: BEST_SELLING) {
      pageInfo { hasNextPage endCursor }
      edges { node {
        id handle title productType tags description totalInventory availableForSale
        featuredImage { url }
        priceRange { minVariantPrice { amount } }
        compareAtPriceRange { minVariantPrice { amount } }
        variants(first: 1) { edges { node { id availableForSale price { amount } compareAtPrice { amount } } } }
        profile: metafield(namespace: "my_fields", key: "profile") { value }
        lineage: metafield(namespace: "my_fields", key: "lineage") { value }
        flavours: metafield(namespace: "my_fields", key: "flavours") { value }
        effects: metafield(namespace: "my_fields", key: "effects") { value }
        thc: metafield(namespace: "my_fields", key: "average_thc_levels") { value }
        usedFor: metafield(namespace: "my_fields", key: "used_for") { value }
      } }
    }
  }`,
  collectionProducts: `query CollectionProducts($handle: String!, $first: Int!) {
    collection(handle: $handle) { title description image { url } products(first: $first) { edges { node { handle } } } }
  }`,
  collections: `query Collections($first: Int!) {
    collections(first: $first, sortKey: TITLE) { edges { node { handle title description image { url } } } }
  }`,
  cartCreate: `mutation CartCreate($input: CartInput!) {
    cartCreate(input: $input) { cart { id checkoutUrl } userErrors { field message } }
  }`,
};
