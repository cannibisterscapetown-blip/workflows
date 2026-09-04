import { isNightOwl, msUntilNextFlip, NIGHT_OWL_DISCOUNT_PCT, NIGHT_OWL_END_HOUR, NIGHT_OWL_START_HOUR, NIGHT_OWL_TZ, type NightOwlStatus } from '@cannibisters/shared';
import { http, isMock } from './http';

export function localNightOwlStatus(now = new Date()): NightOwlStatus {
  return {
    active: isNightOwl(now),
    startHour: NIGHT_OWL_START_HOUR,
    endHour: NIGHT_OWL_END_HOUR,
    timeZone: NIGHT_OWL_TZ,
    discountCode: 'NIGHTOWL15',
    discountPct: NIGHT_OWL_DISCOUNT_PCT,
    nextChangeAt: new Date(now.getTime() + msUntilNextFlip(now)).toISOString(),
  };
}

export async function getNightOwlStatus(): Promise<NightOwlStatus> {
  if (isMock) return localNightOwlStatus();
  try { return await http<NightOwlStatus>('/nightowl/status'); } catch { return localNightOwlStatus(); }
}
