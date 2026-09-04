import { Hono } from 'hono';
import { COLLECTIONS, PRODUCTS, productsInCollection, findProduct } from '@cannibisters/shared';
import { isMock } from '../env';
import type { Vars } from '../app';

/** Catalog routes. Live mode: TODO map Storefront products (see adapters/shopifyStorefront.ts Q.products) into Product. */
export const catalog = new Hono<{ Variables: Vars }>();

catalog.get('/collections', (c) => c.json(COLLECTIONS));

catalog.get('/products', (c) => {
  const collection = c.req.query('collection'); const q = c.req.query('q')?.toLowerCase(); const type = c.req.query('type'); const limit = Number(c.req.query('limit') ?? 0);
  let list = collection ? productsInCollection(collection) : PRODUCTS.filter((p) => p.category !== 'membership');
  if (type) list = list.filter((p) => p.strainType === type);
  if (q) list = list.filter((p) => [p.title, p.flavours, p.profile, ...p.tags].filter(Boolean).join(' ').toLowerCase().includes(q));
  if (!isMock) { /* live catalog mapping lands here */ }
  return c.json(limit ? list.slice(0, limit) : list);
});

catalog.get('/products/:handle', (c) => {
  const p = findProduct(c.req.param('handle'));
  return p ? c.json(p) : c.json({ message: 'Not found' }, 404);
});

catalog.get('/featured', (c) => c.json({
  sotw: PRODUCTS.find((p) => p.badges?.includes('sotw')),
  newArrivals: PRODUCTS.filter((p) => p.badges?.includes('new')).slice(0, 8),
  popularTonight: ['gastro-pops', 'el-pancho', 'gelato-frosting-joint', 'gummie-bears-thc', 'red-velvet', 'blockberry'].map(findProduct).filter(Boolean),
  membership: PRODUCTS.filter((p) => p.category === 'membership'),
}));
