import { describe, it } from "node:test";
import assert from "node:assert";

import { run, classify, haversineKm } from "./index.js";

const SAME_DAY = {
  handle: "same-day",
  title: "Cape Town Same Day - 25kms range - no minimum order value",
};
// Note the double space in the live rate title — matching must survive it.
const FREE_25KM = {
  handle: "free-25km",
  title: "Cape Town  up to 25kms range - FREE - minimum order value R700",
};
const BEYOND_25KM = {
  handle: "beyond-25km",
  title: "Western Cape 25kms + from our club - minimum order value R650",
};
const COLLECT = { handle: "collect", title: "Collect in-store" };
const FREE_NATIONWIDE = {
  handle: "free-nationwide",
  title: "Free Delivery Nationwide - Same Day in Cape Town!",
};

const ALL_OPTIONS = [SAME_DAY, FREE_25KM, BEYOND_25KM, COLLECT, FREE_NATIONWIDE];

function inputFor(deliveryAddress, config = undefined) {
  return {
    cart: { deliveryGroups: [{ deliveryAddress, deliveryOptions: ALL_OPTIONS }] },
    deliveryCustomization: config ? { metafield: { jsonValue: config } } : null,
  };
}

function hiddenHandles(result) {
  return result.operations
    .map((operation) => operation.deliveryOptionHide.deliveryOptionHandle)
    .sort();
}

describe("haversineKm", () => {
  it("measures a known Cape Town distance", () => {
    // Sea Point to Hout Bay, roughly 13km as the crow flies.
    const km = haversineKm(-33.919, 18.386, -34.039, 18.356);
    assert.ok(km > 11 && km < 15, `expected ~13km, got ${km}`);
  });

  it("returns zero for the same point", () => {
    assert.equal(haversineKm(-33.919, 18.386, -33.919, 18.386), 0);
  });
});

describe("classify", () => {
  const config = {
    originLatitude: -33.919,
    originLongitude: 18.386,
    radiusKm: 25,
    insideOnlyTitles: [],
    outsideOnlyTitles: [],
    countryCode: "ZA",
    provinceCode: "WC",
    metroZips: ["8001", "8005", "8060", "7441", "7806"],
    allowZips: [],
    denyZips: [],
  };

  it("treats a nearby address as inside regardless of its postcode", () => {
    // 8060 is not on any allow-list; the coordinates are what matter.
    assert.equal(
      classify({ zip: "8060", latitude: -33.915, longitude: 18.384 }, config),
      "inside",
    );
  });

  it("treats Hermanus as outside", () => {
    assert.equal(
      classify({ zip: "7200", latitude: -34.4187, longitude: 19.2345 }, config),
      "outside",
    );
  });

  // Checkout frequently supplies no coordinates for shipping-rate calculation.
  // The first production release treated that as unclassifiable and hid
  // nothing, so every address — Hermanus, and a European one — was offered the
  // local rates. These cover the fallback that replaced it.
  it("falls back to the postcode list when there are no coordinates", () => {
    assert.equal(classify({ zip: "8005", provinceCode: "WC" }, config), "inside");
  });

  it("treats a non-metro postcode as outside when there are no coordinates", () => {
    assert.equal(classify({ zip: "7200", provinceCode: "WC" }, config), "outside");
  });

  it("treats a foreign address as outside", () => {
    assert.equal(
      classify({ zip: "95700", countryCode: "FR", provinceCode: "WC" }, config),
      "outside",
    );
  });

  it("treats another province as outside", () => {
    assert.equal(
      classify({ zip: "2191", countryCode: "ZA", provinceCode: "GP" }, config),
      "outside",
    );
  });

  it("returns unknown only when there is neither a postcode nor coordinates", () => {
    assert.equal(classify({ city: "Cape Town" }, config), "unknown");
  });

  it("honours an allow-list entry before measuring distance", () => {
    assert.equal(
      classify({ zip: "7200" }, { ...config, allowZips: ["7200"] }),
      "inside",
    );
  });

  it("honours a deny-list entry over the distance check", () => {
    assert.equal(
      classify(
        { zip: "8060", latitude: -33.915, longitude: 18.384 },
        { ...config, denyZips: ["8060"] },
      ),
      "outside",
    );
  });

  it("ignores whitespace in postcodes", () => {
    assert.equal(
      classify({ zip: " 80 60 " }, { ...config, allowZips: ["8060"] }),
      "inside",
    );
  });
});

describe("run", () => {
  it("keeps the free 25km rate for a Sea Point address on postcode 8060", () => {
    // The regression this function exists to fix: inside the radius, wrong-ish
    // postcode, previously lost both Cape Town rates.
    const result = run(inputFor({ zip: "8060", latitude: -33.915, longitude: 18.384 }));
    assert.deepEqual(hiddenHandles(result), ["beyond-25km"]);
  });

  it("keeps the free 25km rate for Hout Bay (7806)", () => {
    const result = run(inputFor({ zip: "7806", latitude: -34.039, longitude: 18.356 }));
    assert.deepEqual(hiddenHandles(result), ["beyond-25km"]);
  });

  it("keeps the free 25km rate for Table View (7441)", () => {
    const result = run(inputFor({ zip: "7441", latitude: -33.823, longitude: 18.49 }));
    assert.deepEqual(hiddenHandles(result), ["beyond-25km"]);
  });

  it("hides the within-25km rates for Hermanus", () => {
    const result = run(inputFor({ zip: "7200", latitude: -34.4187, longitude: 19.2345 }));
    assert.deepEqual(hiddenHandles(result), ["free-25km", "same-day"]);
  });

  it("hides the within-25km rates for Hermanus with no coordinates", () => {
    // The production regression: this returned no operations, so Hermanus was
    // offered both Cape Town rates.
    const result = run(inputFor({ zip: "7200", city: "Hermanus", provinceCode: "WC", countryCode: "ZA" }));
    assert.deepEqual(hiddenHandles(result), ["free-25km", "same-day"]);
  });

  it("hides the within-25km rates for a foreign address", () => {
    const result = run(inputFor({ zip: "95700", city: "Roissy-en-France", countryCode: "FR" }));
    assert.deepEqual(hiddenHandles(result), ["free-25km", "same-day"]);
  });

  it("keeps the free rate for Sea Point with no coordinates", () => {
    const result = run(inputFor({ zip: "8005", city: "Sea Point", provinceCode: "WC", countryCode: "ZA" }));
    assert.deepEqual(hiddenHandles(result), ["beyond-25km"]);
  });

  it("hides nothing when the address has neither postcode nor coordinates", () => {
    const result = run(inputFor({ city: "Cape Town" }));
    assert.deepEqual(result.operations, []);
  });

  it("hides nothing when there is no delivery address at all", () => {
    const result = run(inputFor(null));
    assert.deepEqual(result.operations, []);
  });

  it("never hides collect-in-store or the nationwide rate", () => {
    for (const address of [
      { zip: "8060", latitude: -33.915, longitude: 18.384 },
      { zip: "7200", latitude: -34.4187, longitude: 19.2345 },
    ]) {
      const hidden = hiddenHandles(run(inputFor(address)));
      assert.ok(!hidden.includes("collect"));
      assert.ok(!hidden.includes("free-nationwide"));
    }
  });

  it("applies a radius override from the config metafield", () => {
    const result = run(
      inputFor({ zip: "7200", latitude: -34.4187, longitude: 19.2345 }, { radiusKm: 150 }),
    );
    assert.deepEqual(hiddenHandles(result), ["beyond-25km"]);
  });
});
