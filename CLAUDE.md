# Cannibisters — Workflows Repo Context

## What This Repo Is

This repo contains automated workflows for **Cannibisters Cape Town**, a cannabis brand based in Cape Town, South Africa. The primary active workflow is the **monthly sticker order calculator**.

---

## Sticker Order System

### Overview
Every month, stickers and labels need to be ordered based on how many of each product were sold on Shopify. The system:
1. Pulls last month's Shopify orders via the API
2. Maps each product sold to a sticker type
3. Compares usage against current stock (`sticker_stock.json`)
4. Calculates how many of each sticker to order
5. Posts the report to the **#stickers-inventory** Slack channel

### Key Files
| File | Purpose |
|------|---------|
| `sticker_order.py` | Main script — run this monthly |
| `sticker_stock.json` | Current on-hand sticker counts (update after each physical count) |
| `sticker_config.json` | Legacy config (superseded by hardcoded mappings in `sticker_order.py`) |
| `sticker_inventory.json` | Legacy leftover tracker (superseded by `sticker_stock.json`) |
| `.env` | Secrets: `SHOPIFY_TOKEN`, `SLACK_TOKEN`, `SHOPIFY_STORE`, `SLACK_CHANNEL` |

### How to Run
```bash
python3 sticker_order.py                  # uses last calendar month
python3 sticker_order.py --month 2026-02  # specify a month
```

### Sticker Categories Tracked
- **THC Oils** — 9 product variants (tinctures, drops)
- **Edibles** — gummies, chocolates, lollipops
- **Packaging** — Container Sticker (1 per unique flower strain per order), Package Seal
- **Flyers** — Thank you Card, Thank you for visiting, Roadmap (1 per online order)
- **Accessories** — Lighter, Joint Holder, Rolling Tray, Cone Jar stickers
- **Pre Roll Labels** — Sativa / Indica / Hybrid (dynamically classified from Shopify product tags/titles)
- **LTD Edition Labels** — Sativa / Indica / Hybrid
- **Moonstick Labels** — Sativa / Indica / Hybrid
- **Living Soil Labels** — Sativa / Indica / Hybrid
- **Super Joints Labels** — Sativa / Indica / Hybrid

### Joint Label Classification (Dynamic)
Joint products are **not** manually mapped. At runtime, `sticker_order.py`:
1. Fetches all Shopify products with type `joint`/`joints`
2. Classifies each by **brand** (Pre Roll / LTD / Moonstick / Living Soil / Super Joints) using title keywords
3. Classifies each by **strain** (Sativa / Indica / Hybrid) using product tags, then title keywords
4. Builds a `{product_id: sticker_name}` map used during order counting

This auto-classifies ~68 joint products without manual maintenance.

---

## Current State of `sticker_stock.json` (as of March 2026)

### Joint Labels — populated from invoice (March 2026)
| Label | Sativa | Indica | Hybrid |
|-------|--------|--------|--------|
| Pre Roll Label | 2400 | 1500 | 1500 |
| Living Soil Label | 2400 | 1500 | 1500 |
| LTD Label | 2400 | 1500 | 1500 |
| Super Joints Label | 200 | 100 | — |
| Moonstick Label | 600 | 600 | 600 |

### All Other Stickers — **PENDING end-of-March physical count**
All other sticker types (oils, edibles, packaging, accessories, flyers) are currently set to `0` as placeholders. These will be updated once the manual stock count is completed at the end of March 2026.

**When the user provides counts:** update `sticker_stock.json` with the real numbers, commit, and push to `claude/optimize-sticker-ordering-S51no`.

---

## Slack Integration
- Report posts to **#stickers-inventory** channel
- Default channel ID: `C0AJAL63PNK` (can be overridden via `SLACK_CHANNEL` env var)
- The report shows: Sold (last month) | Stock (on-hand) | Order (qty to purchase)
- LOW stock flag triggers when stock < 25% of monthly usage

---

## Development Branch
Active branch: `claude/optimize-sticker-ordering-S51no`

---

## Other Workflows in `.agent/workflows/`
- `boost_instagram_post.md` — Instagram post boosting
- `optimize_meta_campaigns.md` — Meta ad campaign optimisation
- `cleanup-new-strains.md` — Shopify new strain cleanup
- `shopify-product-update.md` — Shopify product update workflow
- `advent_calendar_update.md` — Advent calendar updates
