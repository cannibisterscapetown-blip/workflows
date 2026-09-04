import { PRODUCTS, COLLECTIONS, productsInCollection, findProduct, type Product, type Collection, type StrainType } from '@cannibisters/shared';
import { http, isMock, delay } from './http';

export interface ProductQuery { collection?: string; q?: string; type?: StrainType; limit?: number }

export async function getCollections(): Promise<Collection[]> {
  if (isMock) { await delay(150); return COLLECTIONS; }
  return http<Collection[]>('/catalog/collections');
}

export async function getProducts(query: ProductQuery = {}): Promise<Product[]> {
  if (isMock) {
    await delay(200);
    let list = query.collection ? productsInCollection(query.collection) : PRODUCTS.filter((p) => p.category !== 'membership');
    if (query.type) list = list.filter((p) => p.strainType === query.type);
    if (query.q) {
      const q = query.q.toLowerCase();
      list = list.filter((p) => [p.title, p.flavours, p.profile, p.lineage, ...(p.effects ?? []), ...p.tags].filter(Boolean).join(' ').toLowerCase().includes(q));
    }
    return query.limit ? list.slice(0, query.limit) : list;
  }
  const params = new URLSearchParams();
  if (query.collection) params.set('collection', query.collection);
  if (query.q) params.set('q', query.q);
  if (query.type) params.set('type', query.type);
  if (query.limit) params.set('limit', String(query.limit));
  return http<Product[]>(`/catalog/products?${params}`);
}

export async function getProduct(handle: string): Promise<Product | undefined> {
  if (isMock) { await delay(150); return findProduct(handle); }
  return http<Product>(`/catalog/products/${encodeURIComponent(handle)}`);
}

export interface Featured { sotw?: Product; newArrivals: Product[]; popularTonight: Product[]; membership: Product[] }

export async function getFeatured(): Promise<Featured> {
  if (isMock) {
    await delay(180);
    return {
      sotw: PRODUCTS.find((p) => p.badges?.includes('sotw')),
      newArrivals: PRODUCTS.filter((p) => p.badges?.includes('new') && !p.badges.includes('sotw')).slice(0, 8),
      popularTonight: ['gastro-pops', 'el-pancho', 'gelato-frosting-joint', 'gummie-bears-thc', 'red-velvet', 'blockberry'].map(findProduct).filter((p): p is Product => !!p),
      membership: PRODUCTS.filter((p) => p.category === 'membership'),
    };
  }
  return http<Featured>('/catalog/featured');
}
