import { demoEntryPass, type EntryPass } from '@cannibisters/shared';
import { http, isMock, delay } from './http';

/** A short-lived signed pass for the door scanner. Refresh before `expiresAt`. */
export async function getEntryPass(): Promise<EntryPass> {
  if (isMock) { await delay(160); return demoEntryPass(); }
  return http<EntryPass>('/entry/pass', { method: 'POST' });
}
