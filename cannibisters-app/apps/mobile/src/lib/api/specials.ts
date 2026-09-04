import { DEMO_SPECIALS, type Special } from '@cannibisters/shared';
import { http, isMock, delay } from './http';

export async function getSpecials(): Promise<Special[]> {
  if (isMock) { await delay(140); return DEMO_SPECIALS; }
  return http<Special[]>('/specials');
}
