# Cannibisters Members App — Research Handoff

Status: discovery complete in the cloud session (3 Sep 2026). Build to continue **locally**, where the Obsidian vault is available. Nothing has been built yet; this file is the full record of what was verified against the live store, the live theme and the repo, plus the proposed architecture. Treat every "verified" item as fact and every "assumption" item as something to confirm from Obsidian before building.

---

## 1. What the app must do (from the brief)

1. Club entry via a member QR code, "the same way the site currently does".
2. Online ordering with the same member logins as the website (no re-registration).
3. Loyalty dashboard: see points, redeem points.
4. Club Moments: members upload photos from the shop / smoke sessions, tag the strain or product (product selection auto-fills indica / sativa / hybrid), other members engage.
5. Cannisino section: interact and play the Cannisino games.
6. Night Owl: after midnight the app flips to dark mode and "the night owl takes over" with an eye-catching animation.
7. App-only specials to incentivise ordering through the app.
8. Home for the Concierge feature launched 31 Aug 2026.
9. Premium, brand-true, straightforward navigation, subtle upsell nudges / CTAs.
10. iOS + Android, web version first is acceptable for design and planning.
11. Orchestration: Fable 5.1 designs and orchestrates; cheaper models do grunt work.

---

## 2. Verified store facts (Shopify Admin API, 3 Sep 2026)

| Item | Value |
|---|---|
| Store | `cannibisters.myshopify.com`, primary domain `cannibisters.com` |
| Name | Cannibisters - The Herbal Apothecary |
| Plan / currency / tz | Advanced · ZAR · CAT (SAST, UTC+2) |
| Customer accounts | **CLASSIC** (email + password). `loginRequiredAtCheckout: true` |
| Address | 65 Regent Rd, Sea Point, Cape Town. Open daily (press: 09:00–23:30) |
| Phone / WhatsApp | +27 87 537 8000 · WhatsApp +27 66 344 3012 (`wa.me/27663443012`) |
| Instagram | @cannibisterscapetown |
| Free delivery | Over R700 within 25 km. Same-day Cape Town before daily cut-off; nationwide courier |
| Members | ~23,000 (press) |

### Membership products (collection `membership`, id 407649943764)
| Product | Variant id | Price |
|---|---|---|
| One day membership (24h) — "Day Pass" | 45926468649172 | R20 |
| 30 day membership | 43324946415828 | R100 |
| 3 month membership | 44119600398548 | R300 |
| 6 month membership | 44119603577044 | R550 |
| 12 month membership | 44119604887764 | R1000 |

Checkout is gated: `snippets/membership-gate-modal.liquid` blocks checkout without an active membership and offers a one-click R20 day pass. Locksmith is installed for content gating. Applications are collected by **Helium Customer Fields** (registration form id `2qt9G8`: age question, terms, ID upload, referral code `referral_code__who_invited`) and reviewed by hand within ~24h. `/pages/invite` gives a referred friend a free day pass (localStorage `cb_invite`, `?ref=CODE`).

### Login model for the app (verified against Shopify docs)
Classic accounts ⇒ Storefront API `customerAccessTokenCreate(input:{email,password})` returns a customer access token (expires, renew with `customerAccessTokenRenew`). Attach it to the cart with `cartBuyerIdentityUpdate` so `checkoutUrl` opens already signed in. This is exactly "same logins as the website". Registration/applications should deep-link to `https://cannibisters.com/account/register` (Customer Fields form) inside an in-app browser rather than re-implementing KYC.

Needed credentials (none created yet): a Storefront API token from a Headless channel (read products/collections/customers, write carts), an Admin API custom-app token (read customers + metafields, read discounts, write discount codes for app-only specials), and the BON Loyalty API bearer token.

### Product data model
- Product types: Flower, joints, extracts/concentrates, vapes, edibles, accessories. Flower ≈ R200 default variant.
- Type is a **tag**: `Indica`, `Sativa`, `Hybrid` (also `Indica-Dominant`, `Balanced`). Effects and flavours are tags too (`Relaxed`, `Euphoric`, `Sweet`, `Gas`…). Collections `indica`/`sativa`/`hybrid` are tag-rule smart collections. This is what Club Moments uses to auto-fill the type from a selected product.
- Metafields (namespace `my_fields`): `lineage` (list), `profile` (e.g. "70/30 Indica-Dominant Hybrid"), `flavours`, `effects` (list), `breeder` (list), `flowering_time` (list), `height`, `stretch_percentage`, `average_thc_levels`, `used_for`. Older duplicates under `custom.*`.
- Key collections: `specials` (manual), `new-strains`, `premium-bud` (Flower), `sativa`, `indica`, `hybrid`, `greendoor` (Organic Living Soil), `lucky-packets`, `strain-of-the-week` (Flower Of The Week), `joints`, `cannibisters-limited-collection-1`, `extracts-and-concentrates`, `vapes`, `edibles`, `accessories`, plus effect collections (`relax`, `sleep`, `happy`, `focus`, `energetic`, `euphoric`, `giggles`, `social`, `libido`, `pain`, `stress`, `anxiety`, `appetite`, `tingly`, `uplifting`, `creative`).
- Customer metafields that matter: `klaviyo.bon_point`, `klaviyo.bon_vip_tier`, `klaviyo.bon_member_status`, `klaviyo.bon_referral_url`, `klaviyo.bon_birthday`, `klaviyo.bon_point_expired_at`, `klaviyo.LoyaltyPoints`, `klaviyo.club_application`. A `member_number` metaobject definition exists (field `member`, integer).
- Discount patterns in use: per-customer one-use codes `CB-ONLINE100-XXXX` (R100 off online order, min R200) and `CB-POS200/500-XXXX` (in-store vouchers). App-only specials can follow the same pattern (Admin API `discountCodeBasicCreate`, customer-restricted, one use).

---

## 3. The redesign theme (verified from the live MAIN theme)

Theme: Minion 2.6.0, named **"Copy of Redesign PREVIEW"** (gid 165952946388), heavily customised with `cb-*` sections and CDN bundles (`cb-home`, `cb-product`, `cb-nightowl`, `cb-loyalty-page`). Header is light/clean with a dark charcoal nav and the gold leaf emblem; body chapters, footer, login, loyalty, product and collection pages are **dark luxe**.

### Design tokens (copy exactly)
```
--cbg-dark:      #05060c   page background (dark luxe)
--cbg-card:      #11131a   cards           (alt #0b0c12, #0f1118 inputs)
--cbg-gold:      #D4A843   primary gold    (older sections use #D4A017)
--cbg-gold-lt:   #E8C96A   gold highlight / hover
--cbg-ink:       #F4ECE0   cream text      (login uses #F5EFE2)
--cbg-muted:     #b9b09c   secondary text  (#8f8877 tertiary)
--cbg-orange:    #FE9E01   "Canni Orange" primary CTA (hover #FF9501), black text on it
--cbg-line:      rgba(212,168,67,.22–.35)  gold hairlines / borders
--cbp-bone:      #F8F4EA   light surfaces (day mode)
--cbp-ink:       #0A0A0A   "Apothecary Black"
--cbp-body:      #D9D2C4 · --cbp-mute: #8E8677
tier badges:     silver #E7EAEF→#A7ACB6 · gold #E8C96A→#B98B2E · platinum #F5F5F4→#C7C6C3 · diamond #E1F4F8→#9BC9D6
```
Typography: **Bebas Neue** (display, uppercase, tight leading .92, letterspacing .012em), **DM Sans** (body 400/500/700), **Playfair Display italic** (serif accent), **Caveat 700** (handwritten accent on collection heroes). Theme default body font is Figtree (legacy Minion pages only). Eyebrows: DM Sans 700, .7rem, uppercase, letterspacing .32em, gold. Radius 10–16px on cards and inputs, 999px pills for CTAs on Cannisino. Cards: 1px gold hairline border, `0 24px 60px rgba(0,0,0,.45)` shadow. Motion: `cubic-bezier(.16,1,.3,1)` fade-up 0.5s, `cubic-bezier(.2,.7,.2,1)` general ease. Gold leaf emblem watermark at 4% opacity behind auth screens. Film-grain and radial "night ground" on hero surfaces.

Brand assets in repo: `Canni Logo.png` (gold ornate leaf, serif CANNIBISTERS, HERBAL APOTHECARY). Theme asset `assets/cb-leaf-emblem-gold.png`; CDN `night-owl-gold-360.png`, `night-owl-2.mp4` + poster.

### Homepage chapters (day mode order)
September Specials → Lucky Packets → Night Owl promo → Loyalty + Cannisino intro → In-house doctor (Dr Andre Sorger: Medicinal Cannabis Consultation R650, Chinese Medicine R900, booked via Meety on product pages) → Strain of the Week (ch4) → Membership pricing (ch6) → Cannisino chapter → "Enjoy It Elegantly" closer (ch7) → Delivery (Cape Town same-day / Nationwide / In-store). Nav: Home, Shop, About us, Consultations, Contact, Gallery, Blog, Loyalty Program, Cannisino.

---

## 4. Brand voice (from "Cannibisters Klaviyo Brand Voice Guidelines.pdf" + repo style guides)
- Modern, elevated, warm; "premium hospitality meets Cape Town cool"; a second home for members.
- Calm, minimalist, confident, upmarket. Short intentional lines. **No exclamation marks.** UK / South African English (flavours, colour, recognise).
- Say **member**, never customer. Use: members-only, private, curated, premium, drop, arrival, exclusive, "your Club", discreet, responsible, community, crafted, flavours, strains.
- Avoid stoner slang (blaze, lit, dank), medical claims, "guaranteed", pushy sales phrasing, direct consumption encouragement.
- Sign-off: "The Cannibisters Team". Emojis minimal (🌿 ✨ at most).
- Palette direction: clean black, gold and cream; ample spacing; premium photography; subtle elegant animation.
- Live copy to reuse: "Members-Only Cannabis Club & Herbal Apothecary in Sea Point, Cape Town", "Share and exchange cannabis products legally and responsibly", "WELCOME BACK.", "Not a member yet? Apply to join.", "New arrivals, member specials and the quiet drops".

---

## 5. Loyalty (verified)
Two layers:
1. **BON Loyalty** (Shopify app, points live in `klaviyo.bon_point`). GraphQL API docs: https://bonloyalty.com/api-doc/index.html — endpoint `graph[-dev].bonloyalty.com/graphql`, header `Authorization: Bearer <token from BON dashboard>`. Query `customer(shopify_id)` → `points, points_earned, point_histories, rewards, reward_detail, customer_tier, referral_code, referral_link, point_expired_at`. Mutations include `createRedeem`, `createDiscount`, `Customer.adjustPoint`, `Order`, `tier`.
2. **Custom loyalty backend** already built for the site: `https://cannibisters-loyalty.vercel.app` with `/api/loyalty/me`, `/api/loyalty/redeem`, `/api/loyalty/subscribe`; sessions minted through the Shopify **app proxy** `POST /apps/cannisino/loyalty-session` (also `/apps/loyalty/session`). Source lives outside this repo (`cannibisters-loyalty/storefront/...`, see comments in `assets/cb-loyalty-page.js`). The app should reuse this backend, adding an auth path that accepts a Storefront customer access token instead of the Liquid `{{ customer }}` gate.

Programme rules (from the live loyalty bundle, effective 1 Sep 2026): earn `BASE_RATE_PTS_PER_RAND` × tier multiplier; tiers Silver (0, 1.0×, 0% off) → Gold (10,000, 1.2×, 10% off) → Platinum (20,000, 1.4×, 20% off) → Diamond (1.7×); tiers on a rolling 180-day spend window; points expire after 12 months (oldest spent first); `REDEEM_RATE` points = R1; complete profile +100, birthday month +1,000, referral +2,500 (friend gets 1,500); reaching Gold/Platinum banks a Wheel of Fortune spin (Gold ≈45% win, Platinum ≈55%). Prize copy: 15% off, free pre-roll, 10,000 pts (Gold); 20% off, Moonstick, 15,000 pts (Platinum). Repo `wheel_of_fortune/` has spend tiers Silver R1500+ / Gold R2500+ / Platinum R3500+ with full prize lists — useful for the in-app wheel.

---

## 6. Cannisino (verified)
Page `/pages/cannisino` posts `POST /apps/cannisino/session` (same-origin, needs logged-in customer) → `{token}` → iframe `https://cannisino.vercel.app/casino?embed_token=<token>`. Games: Predictions (weekly markets, odds lock on bet, settle daily), Claw Machine, Mines, Wheel of Fortune. Rules: 21+ members, free-to-play, "Play Wallet" separate from loyalty balance, min stake 500 pts, winnings settle to loyalty balance with 24h cooldown and R500 lifetime cap. Homepage CTA style: Canni Orange pill "Log in to play". The app can embed the same URL in a WebView once it can mint the session token with a Storefront customer token (backend change in the cannisino app), or link out until then.

---

## 7. Night Owl (verified)
Website already has a Night Owl takeover on the homepage: active **midnight–7am SAST**, 15% off online orders, exit button "Day mode ☀", rails "Popular Tonight" and "Just Landed", video hero. Copy: "After Dark · Midnight–7am", "Night Owl. The city's asleep — the apothecary isn't. Take your time with the menu; the quiet hours are yours.", "15% off everything · midnight–7am", "Shop the night →", "Members only · Order tonight, first delivery slot tomorrow", "Late nights deserve quiet delivery." The app version must be its own animation (owl emblem, gold eyes, feathers/stars) and should apply the discount automatically (automatic discount scheduled nightly, or a code applied to the cart).

---

## 8. QR club entry — NOT found on cannibisters.com (needs Obsidian)
No QR generation exists in the Shopify theme, pages or loyalty bundle. **`cannibisters.co.za` is a separate Bubble.io app** ("Cannibisters HOME", has a `/login` page, uses Lottie). That is almost certainly where the member QR / door check-in lives today. Confirm from Obsidian: what the QR encodes (member number? Shopify customer id? signed token?), what the door scanner expects, and whether membership validity is checked at scan time. The app should reproduce the same payload so the existing scanner keeps working; recommended payload is a short-lived signed token containing member number + expiry, rendered as a QR with a live countdown.

## 9. Concierge — NOT found anywhere public (needs Obsidian)
Nothing on the site, theme, blog, Slack, Gmail or web mentions a concierge. The Consultations page and one blog post were edited on 31 Aug (launch day) but contain no concierge copy. Read the Obsidian notes on the concierge launch before designing this tab. Working assumption if nothing turns up: "Canni Concierge" = WhatsApp-backed personal service (strain recommendations, pre-orders for collection, table/seat reservation, consultation booking, delivery slot help) presented as a chat-style screen in the app.

---

## 10. Proposed architecture (decided, adjust locally if Obsidian changes anything)
- **Monorepo** `cannibisters-app/` (pnpm workspaces): `apps/mobile` (Vite + React + TypeScript PWA, mobile-first app shell, wrapped with **Capacitor** for iOS and Android: camera, haptics, push, biometrics, safe areas), `apps/api` (Node BFF, Hono), `packages/ui` (design tokens + components), `packages/shopify` (typed Storefront/Admin clients), `docs/`.
- Why Capacitor over Expo: one web codebase satisfies "web version first", ships to both stores, and the existing Cannisino/loyalty web bundles embed cleanly.
- **Auth**: Storefront `customerAccessTokenCreate`; token stored in secure storage; BFF exchanges it for a short app session and resolves the Shopify customer id for BON / loyalty / Cannisino calls.
- **Ordering**: Storefront cart API + `checkoutUrl` opened in an in-app browser with buyer identity attached; membership gate mirrored in-app (offer day pass); Night Owl discount auto-applied in window.
- **Loyalty**: BFF → existing loyalty backend (`/api/loyalty/me`, `/redeem`) with BON as source of truth.
- **Club Moments**: BFF-owned Postgres + object storage; post = image, caption, product ref (Shopify product id), strain type auto-derived from tags, likes/comments/reports; moderation queue; 18+ and privacy consent copy in brand voice.
- **Cannisino**: WebView of `cannisino.vercel.app/casino?embed_token=` minted via BFF.
- **App-only specials**: BFF config + Admin API customer-restricted one-use codes; surfaced on Home and Cart with subtle nudges.
- **Night Owl**: client clock in Africa/Johannesburg + server flag; theme flips to dark, owl animation (SVG/Lottie), "Popular Tonight" rail, 15% messaging.
- **Concierge**: define after Obsidian; slot is the fourth tab.
- Tabs: Home · Shop · Entry (QR, centre, gold) · Moments · More (Loyalty, Cannisino, Concierge, Orders, Profile). Alternative: Home · Shop · QR · Cannisino · Concierge with Moments in Home feed. Decide locally.
- **Orchestration**: Fable writes design system, IA, screen specs and reviews; Sonnet/Haiku agents scaffold, implement screens from specs, write mocks and tests; Fable runs adversarial review before merge.

## 11. Repo context
- This repo is a Shopify ops toolbox (Python scripts, product metafield updates, marketing reports). `shopify_api.py` reads a token from `.env`. `index.html` is an unrelated OffGrid AI landing page. `wheel_of_fortune/` is a working dark-theme wheel (Outfit font, neon green, confetti) to restyle for Cannisino.
- Branch for this work: `claude/cannibisters-mobile-app-7hmeho`.

## 12. Open questions for the local session (answer from Obsidian first)
1. What exactly does the current member QR encode and which system scans it (Bubble app, POS, tablet)?
2. What is the Concierge feature: channel, scope, staff workflow, pricing, copy?
3. Is `cannibisters-loyalty.vercel.app` / `cannisino.vercel.app` source available locally (to add token-based auth for the app)?
4. Which tab layout and which app name (e.g. "Cannibisters", "Canni Club")?
5. Any existing brand assets for the owl (Night Owl) and app icon?
