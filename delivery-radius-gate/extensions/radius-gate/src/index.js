// @ts-check

/**
 * Delivery radius gate.
 *
 * Hides the "within 25km" Cape Town rates from addresses outside the radius,
 * and hides the "25km +" rate from addresses inside it.
 *
 * Distance is measured from the shop's coordinates to the buyer's geocoded
 * delivery address. Postal codes are only consulted as an explicit override —
 * they are not the primary signal, because a buyer 5km away who mistypes their
 * postcode (or lives in a suburb nobody added to a hand-maintained list) would
 * otherwise silently lose free delivery.
 *
 * When the address cannot be classified — no coordinates and no matching
 * override — this function HIDES NOTHING. Failing open occasionally gives a
 * far-away buyer a rate they shouldn't see; failing closed silently blocks
 * paying local customers at checkout, which is the more expensive mistake and
 * the bug this replaces.
 */

const NO_CHANGES = /** @type {const} */ ({ operations: [] });

const EARTH_RADIUS_KM = 6371;

/**
 * Defaults are overridden by the `$app:radius-gate` / `config` metafield on the
 * delivery customization, so the radius, origin and rate titles can be changed
 * in the admin without redeploying the function.
 */
const DEFAULT_CONFIG = {
  // 65 Regent Rd, Sea Point. Verify against the location in admin before relying
  // on it — a few hundred metres of drift is irrelevant at a 25km threshold.
  originLatitude: -33.919,
  originLongitude: 18.386,
  radiusKm: 25,
  // Rates only offered to buyers INSIDE the radius. Matched as normalised
  // substrings, so the rate titles' irregular spacing doesn't break matching.
  insideOnlyTitles: ["cape town same day", "cape town up to 25kms"],
  // Rates only offered to buyers OUTSIDE the radius.
  outsideOnlyTitles: ["western cape 25kms +"],
  // Anything outside these is out of range by definition, and this is the only
  // check that catches a foreign address.
  countryCode: "ZA",
  provinceCode: "WC",
  // Cape Town metro postcodes taken as within the radius when the address has
  // no coordinates. MERCHANT-REVIEWABLE: this is a starting set, not a surveyed
  // one. Anything missing can be added via `allowZips` in the config metafield
  // without redeploying.
  metroZips: [
    // City Bowl, Waterfront, Atlantic Seaboard
    "8000", "8001", "8005", "8010", "8018", "8040", "8045", "8051", "8060",
    // Woodstock, Observatory, southern suburbs
    "7700", "7701", "7705", "7706", "7707", "7708", "7709", "7725", "7730",
    "7735", "7740", "7745", "7750", "7760", "7764", "7780", "7785", "7790",
    "7800", "7801", "7806", "7808", "7809", "7925", "7935", "7941", "7945",
    "7950", "7975",
    // Northern suburbs within range
    "7405", "7435", "7441", "7443", "7446", "7460", "7463", "7490", "7500",
    "7530", "7550",
  ],
  // Known to be out of range. Only these are gated out; anything unrecognised
  // is shown rather than hidden.
  nonMetroZips: [
    "7200", // Hermanus
    "7130", // Somerset West / Strand side
    "6529", "6530", // George
    "7646", // Paarl
    "6600", "6620", "6665", // Karoo / Eastern Cape codes seen on orders
  ],
  // Explicit overrides, checked before everything else.
  allowZips: [],
  denyZips: [],
};

/**
 * @param {string | null | undefined} value
 * @returns {string}
 */
function normalise(value) {
  return (value ?? "").toLowerCase().replace(/\s+/g, " ").trim();
}

/**
 * @param {string | null | undefined} zip
 * @returns {string}
 */
function normaliseZip(zip) {
  return (zip ?? "").replace(/\s+/g, "").toLowerCase();
}

/**
 * Great-circle distance in kilometres.
 *
 * @param {number} lat1
 * @param {number} lon1
 * @param {number} lat2
 * @param {number} lon2
 * @returns {number}
 */
export function haversineKm(lat1, lon1, lat2, lon2) {
  const toRadians = (degrees) => (degrees * Math.PI) / 180;
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRadians(lat1)) *
      Math.cos(toRadians(lat2)) *
      Math.sin(dLon / 2) ** 2;
  return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(a));
}

/**
 * @param {any} address
 * @param {typeof DEFAULT_CONFIG} config
 * @returns {"inside" | "outside" | "unknown"}
 */
export function classify(address, config) {
  if (!address) return "unknown";

  const listHas = (list, value) =>
    (list ?? []).some((entry) => normaliseZip(String(entry)) === value);

  const zip = normaliseZip(address.zip);
  if (zip) {
    if (listHas(config.denyZips, zip)) return "outside";
    if (listHas(config.allowZips, zip)) return "inside";
  }

  // A different country or province is out of range regardless of anything
  // else, and this is what stops a foreign address being offered local rates.
  if (address.countryCode && address.countryCode !== config.countryCode) {
    return "outside";
  }
  if (address.provinceCode && address.provinceCode !== config.provinceCode) {
    return "outside";
  }

  // Preferred signal when it's available. In practice checkout often supplies
  // no coordinates for shipping-rate calculation, which is why this can't be
  // the only signal — relying on it alone made every address unclassifiable
  // and the gate stopped hiding anything at all.
  const { latitude, longitude } = address;
  if (typeof latitude === "number" && typeof longitude === "number") {
    const distance = haversineKm(
      config.originLatitude,
      config.originLongitude,
      latitude,
      longitude,
    );
    return distance <= config.radiusKm ? "inside" : "outside";
  }

  if (zip) {
    if (listHas(config.metroZips, zip)) return "inside";
    // Only postcodes known to be out of range are gated. An unrecognised one is
    // NOT treated as outside: a hand-maintained list is never complete, and
    // every gap silently costs a local customer their free delivery with no
    // signal at checkout. Mowbray (7705) was missing from metroZips and those
    // customers lost the free rate — the same failure as the original app.
    // Showing a rate to someone out of range is recoverable; blocking a paying
    // local customer is not.
    if (listHas(config.nonMetroZips, zip)) return "outside";
    return "unknown";
  }

  return "unknown";
}

/**
 * @param {any} input
 * @returns {any}
 */
export function run(input) {
  const overrides = input?.deliveryCustomization?.metafield?.jsonValue ?? {};
  const config = { ...DEFAULT_CONFIG, ...overrides };

  const insideOnly = config.insideOnlyTitles.map(normalise);
  const outsideOnly = config.outsideOnlyTitles.map(normalise);

  const operations = [];

  for (const group of input?.cart?.deliveryGroups ?? []) {
    const verdict = classify(group.deliveryAddress, config);
    if (verdict === "unknown") continue;

    for (const option of group.deliveryOptions ?? []) {
      const title = normalise(option.title);
      const gatedToInside = insideOnly.some((needle) => title.includes(needle));
      const gatedToOutside = outsideOnly.some((needle) => title.includes(needle));

      const shouldHide =
        (verdict === "outside" && gatedToInside) ||
        (verdict === "inside" && gatedToOutside);

      if (shouldHide) {
        operations.push({
          deliveryOptionHide: { deliveryOptionHandle: option.handle },
        });
      }
    }
  }

  return operations.length > 0 ? { operations } : NO_CHANGES;
}
