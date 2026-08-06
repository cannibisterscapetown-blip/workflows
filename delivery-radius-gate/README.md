# delivery-radius-gate

Shopify Function that controls which Cape Town delivery rates appear at checkout,
based on how far the buyer's address actually is from the shop.

## Why this exists

The previously deployed version of this app gated the 25km rates on a
hand-maintained list of postal codes. That list was incomplete, and it failed
closed: any address whose postcode wasn't on the list lost both "Cape Town"
rates, including the free-over-R700 one — even when the buyer was a few
kilometres away.

The failure was invisible. Checkout simply showed fewer options, so buyers who
qualified for free delivery saw only the R279 rate or in-store collection, and a
number of them abandoned. Confirmed working postcodes were 8001, 7441 and 7806;
8005 (Sea Point / Green Point / Mouille Point) and 8060 were among those being
wrongly excluded.

This version measures the great-circle distance from the shop to the buyer's
geocoded address, so a mistyped or unlisted postcode can no longer block a local
customer.

## Behaviour

For each delivery group the buyer's address is classified:

| Classification | How it's reached | Effect |
| --- | --- | --- |
| `inside` | on `allowZips`, or within `radiusKm` of the origin | hides the `outsideOnlyTitles` rates |
| `outside` | on `denyZips`, or beyond `radiusKm` | hides the `insideOnlyTitles` rates |
| `unknown` | no coordinates and no override match | **hides nothing** |

`unknown` deliberately fails open. Occasionally showing a distant buyer a rate
they shouldn't see costs one delivery; silently blocking local customers at
checkout costs sales every day and generates support load — that's the bug this
replaces.

Rates not named in either list (`Collect in-store`, the nationwide free rate) are
never touched. Rate titles are matched as normalised, lowercased substrings, so
the irregular double space in `Cape Town  up to 25kms range …` doesn't break it.

## Configuration

Defaults live in `DEFAULT_CONFIG` in `extensions/radius-gate/src/run.js` and are
overridden at runtime by a JSON metafield on the delivery customization —
namespace `$app:radius-gate`, key `config`. Anything you set there takes effect
without redeploying:

```json
{
  "originLatitude": -33.919,
  "originLongitude": 18.386,
  "radiusKm": 25,
  "insideOnlyTitles": ["cape town same day", "cape town up to 25kms"],
  "outsideOnlyTitles": ["western cape 25kms +"],
  "allowZips": [],
  "denyZips": []
}
```

Verify `originLatitude` / `originLongitude` against the 65 Regent Rd location in
admin before relying on them. A few hundred metres of drift doesn't matter at a
25km threshold, but a wrong suburb would.

## Deploying

Requires Partner credentials, which aren't available from a Claude Code session.
Either run it locally:

```sh
cd delivery-radius-gate
npm install
npm test
npx shopify app deploy
```

…or create an **app automation token** (dev dashboard → the app → Settings → App
automation token) and set `SHOPIFY_CLI_PARTNERS_TOKEN` in CI.

The `client_id` in `shopify.app.toml` points at the existing
`delivery-radius-gate` app, so deploying publishes a new version of the app
already installed on the store rather than creating a second one. The client
secret is not in this repo and must never be committed.

After deploying, confirm the new version is live in **Settings → Shipping and
delivery → Delivery customizations**, then place a test checkout with a Sea Point
address and a cart over R700 — the free rate should appear.

## Tests

```sh
npm test
```

16 tests covering the distance maths, the classification precedence
(deny > allow > distance > unknown), the specific 8060 and Hermanus regressions,
and that untouched rates stay untouched.
