export const NIGHT_OWL_TZ = 'Africa/Johannesburg';
export const NIGHT_OWL_START_HOUR = 0;   // inclusive
export const NIGHT_OWL_END_HOUR = 7;     // exclusive
export const NIGHT_OWL_DISCOUNT_PCT = 15;

/** Hour of day (0-23) in the given IANA time zone. */
export function hourInZone(date: Date, timeZone = NIGHT_OWL_TZ): number {
  const parts = new Intl.DateTimeFormat('en-GB', { hour: 'numeric', hourCycle: 'h23', timeZone }).formatToParts(date);
  const h = parts.find((p) => p.type === 'hour')?.value ?? '0';
  return Number(h) % 24;
}

/** True between startHour (inclusive) and endHour (exclusive) in the club's time zone. */
export function isNightOwl(
  date = new Date(),
  { timeZone = NIGHT_OWL_TZ, startHour = NIGHT_OWL_START_HOUR, endHour = NIGHT_OWL_END_HOUR } = {},
): boolean {
  const h = hourInZone(date, timeZone);
  return startHour < endHour ? h >= startHour && h < endHour : h >= startHour || h < endHour;
}

/** Milliseconds until the next Night Owl flip (on or off). Coarse: walks minute by minute. */
export function msUntilNextFlip(date = new Date(), opts?: Parameters<typeof isNightOwl>[1]): number {
  const now = isNightOwl(date, opts);
  const step = 60_000;
  const t = new Date(date);
  t.setSeconds(0, 0);
  for (let i = 1; i <= 24 * 60; i++) {
    const probe = new Date(t.getTime() + i * step);
    if (isNightOwl(probe, opts) !== now) return probe.getTime() - date.getTime();
  }
  return 24 * 3_600_000;
}
