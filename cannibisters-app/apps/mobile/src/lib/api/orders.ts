import { DEMO_ORDERS, type Order } from '@cannibisters/shared';
import { http, isMock, delay } from './http';

export async function getOrders(): Promise<Order[]> {
  if (isMock) { await delay(180); return DEMO_ORDERS; }
  return http<Order[]>('/orders');
}
