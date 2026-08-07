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
  "countryCode": "ZA",
  "provinceCode": "WC",
  "metroZips": ["8001", "8005", "..."],
  "allowZips": [],
  "denyZips": []
}
```

`metroZips` is the fallback used when checkout supplies no coordinates, which
is the common case. **It is a starting set, not a surveyed one** — worth
reviewing against where you actually deliver. Adding a missing postcode to
`allowZips` takes effect immediately without a redeploy, so a gap costs a
config edit rather than a release.

Verify `originLatitude` / `originLongitude` against the 65 Regent Rd location in
admin before relying on them. A few hundred metres of drift doesn't matter at a
25km threshold, but a wrong suburb would.

## Deploying

Requires Partner credentials, which aren't available from a Claude Code session,
so this has to run on an authenticated machine.

The extension directory here is hand-written rather than produced by
`shopify app generate extension`, so it lacks two things the CLI's JavaScript
build path expects: a `codegen` block in the extension's `package.json`, and a
`schema.graphql` fetched from Shopify. Both are needed before the wasm build
will run.

Fetch the schema (this is the step that needs auth):

```sh
cd delivery-radius-gate/extensions/radius-gate
shopify app function schema
shopify app function typegen
```

Then from `delivery-radius-gate`:

```sh
npm install
npm test          # expect 16 pass / 0 fail
shopify app deploy
```

If typegen still fails, the fastest fix is to let the CLI scaffold a known-good
extension and move the logic into it — the scaffold brings the correct
`package.json`, codegen config and schema:

```sh
shopify app generate extension   # pick "delivery option transform", JavaScript
```

Then copy `src/index.js`, `src/run.graphql` and `src/run.test.js` from this
extension into the generated one, and keep its `package.json` and
`shopify.extension.toml`. The logic in `index.js` has no dependency on how the
extension was scaffolded.

Two things that are easy to get wrong and cost a deploy cycle each:

- **The entry point must be `src/index.js`.** The CLI looks only there to decide
  a function is JavaScript. Any other filename (`src/run.js`, say) makes it fall
  through to a path that demands an explicit build command and fails with
  "doesn't have a build command or it's empty".
- **`@shopify/shopify_function` must be a dependency** of the function
  directory, at `~2.0.0`.

For CI instead of a local machine, create an **app automation token** (dev
dashboard → the app → Settings → App automation token) and set
`SHOPIFY_CLI_PARTNERS_TOKEN`.

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
