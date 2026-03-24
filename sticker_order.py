#!/usr/bin/env python3
"""
Sticker Order Calculator
Calculates monthly sticker requirements based on Shopify sales,
compares against current stock, and posts the order report to #stickers-inventory.

Run manually:  python3 sticker_order.py
Run for specific month:  python3 sticker_order.py --month 2026-02
"""

import json
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# Load .env file if present (simple key=value parser, no dependencies)
_env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# ─── Config ───────────────────────────────────────────────────────────────────

SHOPIFY_TOKEN = os.environ["SHOPIFY_TOKEN"]
SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE", "cannibisters.myshopify.com")
SLACK_TOKEN   = os.environ["SLACK_TOKEN"]
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "C0AJAL63PNK")  # default: #cannibot-chat (staging)

STOCK_FILE = os.path.join(os.path.dirname(__file__), "sticker_stock.json")

# ─── Shopify product title → sticker name ─────────────────────────────────────
# Each key is the exact Shopify product title; value is the sticker label.

PRODUCT_TO_STICKER = {
    # THC Oils
    "Gastronomical Rosin Drops":                                  "Gastronomical Drops (6mg/drop 5ml)",
    "THC Distillate Oil (1200mg) Medical Grade":                  "Medical Grade (1200mg 5ml)",
    "Near Death Drops Full Strength Tincture Oil 5ml - 2400mg":   "Death Drops (2400mg 5ml)",
    "Death Drops Double-strength Tincture Oil 5ml - 4800mg":      "Double Death Drops (4800mg 5ml)",
    "THC Tincture Oil - 650 mg":                                  "Hybrid Oil (650mg 10ml)",
    "CBD Tincture Oil - 650 mg":                                  "Hybrid Oil (650mg 10ml)",
    "Full Strength Tincture Oil 10ml - 1200mg":                   "Hybrid Oil (1200mg 10ml)",
    "Up Oil Sativa (1200mg)":                                     "Sativa Up Oil (1200mg 10ml)",
    "Near Death Drops Full Strength Tincture Oil 10ml - 2400mg":  "Near Death Drops (2400mg 10ml)",
    "Death Drops  Double-strength Tincture Oil 10ml - 4800mg":    "Double Death Drops (4800mg 10ml)",

    # Edibles
    "Gummy Bears - THC":   "THC Gummies (20mg 10 pack)",
    "Small THC Chocolate": "THC Chocolate (20mg 10 pack)",
    "Gummy Bears - CBD":   "CBD Gummies (20mg 10 pack)",
    "THC Lollipop":        "THC Lollipop (50mg)",
    "Gummies 100mg":       "THC Gummies (100mg 5 pack)",
    "Gummies 200mg":       "THC Gummies (200mg 5 pack)",

    # Accessories
    "Lighter - small":        "Lighter Sticker",
    "Cannibisters Lighter":   "Lighter Sticker",
    "Joint Holder":           "Joint Holder Sticker",
    "Joint holder - Pop-up":  "Joint Holder Sticker",
    "Rolling Tray - Black":   "Rolling Tray Sticker",
    "Cone Jar":               "Cone Jar Sticker",

    # Super Joints — 1 label per unit sold, classified by Sativa / Indica / Hybrid
    "Super Joint - Sativa":              "Super Joints Label - Sativa",
    "Super Joint Sativa Moroccan Rosin": "Super Joints Label - Sativa",
    "Super Joint - Indica":              "Super Joints Label - Indica",
}

# Product types that use a Container Sticker (1 per unique strain line item per order)
FLOWER_TYPES = {"Flower", "Flowers", "flower"}

# Stickers driven by order count rather than product sales
PER_ONLINE_ORDER_STICKERS = [
    "Package Seal Sticker",
    "Thank you Card",
    "Thank you for visiting",
    "Roadmap",
]

# Display order for the report
REPORT_CATEGORIES = {
    "THC OILS": [
        "Gastronomical Drops (6mg/drop 5ml)",
        "Medical Grade (1200mg 5ml)",
        "Death Drops (2400mg 5ml)",
        "Double Death Drops (4800mg 5ml)",
        "Hybrid Oil (650mg 10ml)",
        "Hybrid Oil (1200mg 10ml)",
        "Sativa Up Oil (1200mg 10ml)",
        "Near Death Drops (2400mg 10ml)",
        "Double Death Drops (4800mg 10ml)",
    ],
    "EDIBLES": [
        "THC Gummies (20mg 10 pack)",
        "THC Chocolate (20mg 10 pack)",
        "CBD Gummies (20mg 10 pack)",
        "THC Lollipop (50mg)",
        "THC Gummies (100mg 5 pack)",
        "THC Gummies (200mg 5 pack)",
    ],
    "PACKAGING": [
        "Container Sticker",
        "Package Seal Sticker",
    ],
    "FLYERS": [
        "Thank you Card",
        "Thank you for visiting",
        "Roadmap",
    ],
    "ACCESSORIES": [
        "Lighter Sticker",
        "Joint Holder Sticker",
        "Rolling Tray Sticker",
        "Cone Jar Sticker",
    ],
    "SUPER JOINTS": [
        "Super Joints Label - Sativa",
        "Super Joints Label - Indica",
        "Super Joints Label - Hybrid",
    ],
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def shopify_get(path, params=None):
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-01/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN})
    with urllib.request.urlopen(req) as resp:
        link = resp.headers.get("Link", "")
        data = json.loads(resp.read())
    return data, link


def next_page_url(link_header):
    if 'rel="next"' not in link_header:
        return None
    m = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
    return m.group(1) if m else None


def slack_post(text):
    payload = json.dumps({"channel": SLACK_CHANNEL, "text": text}).encode()
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=payload,
        headers={
            "Authorization": f"Bearer {SLACK_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def load_stock():
    if os.path.exists(STOCK_FILE):
        with open(STOCK_FILE) as f:
            return json.load(f)
    return {}


def save_stock(stock):
    with open(STOCK_FILE, "w") as f:
        json.dump(stock, f, indent=2)

# ─── Core logic ───────────────────────────────────────────────────────────────

def get_flower_product_ids():
    """Return a set of Shopify product IDs whose type is Flower/Flowers/flower."""
    ids = set()
    for ptype in FLOWER_TYPES:
        url = None
        params = {"product_type": ptype, "limit": 250, "fields": "id"}
        while True:
            if url:
                req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN})
                with urllib.request.urlopen(req) as resp:
                    link = resp.headers.get("Link", "")
                    data = json.loads(resp.read())
            else:
                data, link = shopify_get("products.json", params)
            for p in data.get("products", []):
                ids.add(p["id"])
            url = next_page_url(link)
            if not url:
                break
    return ids


def get_orders(start: datetime, end: datetime):
    """Fetch all orders created in [start, end)."""
    orders = []
    params = {
        "status": "any",
        "limit": 250,
        "created_at_min": start.isoformat(),
        "created_at_max": end.isoformat(),
        "fields": "id,source_name,line_items",
    }
    url = None
    while True:
        if url:
            req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN})
            with urllib.request.urlopen(req) as resp:
                link = resp.headers.get("Link", "")
                data = json.loads(resp.read())
        else:
            data, link = shopify_get("orders.json", params)
        orders.extend(data.get("orders", []))
        url = next_page_url(link)
        if not url:
            break
    return orders


def calculate_usage(orders, flower_product_ids):
    """
    Returns a dict of {sticker_name: count} for the given orders.

    Rules:
    - THC Oils / Edibles / Accessories: 1 sticker per unit sold (qty × 1)
    - Container Sticker: 1 per unique flower strain per order (qty ignored)
    - Package Seal Sticker + Flyers: 1 per online order
    """
    usage = {}

    def add(sticker, n=1):
        usage[sticker] = usage.get(sticker, 0) + n

    for order in orders:
        is_online = order.get("source_name") != "pos"

        if is_online:
            for sticker in PER_ONLINE_ORDER_STICKERS:
                add(sticker)

        # Track unique flower product titles in this order for container stickers
        flower_titles_in_order = set()

        for item in order.get("line_items", []):
            title      = item.get("title", "")
            product_id = item.get("product_id")
            qty        = item.get("quantity", 1)

            # Container sticker — flower only, 1 per unique strain regardless of qty
            if product_id in flower_product_ids:
                flower_titles_in_order.add(title)

            # Product-specific stickers
            sticker = PRODUCT_TO_STICKER.get(title)
            if sticker:
                add(sticker, qty)

        add("Container Sticker", len(flower_titles_in_order))

    return usage


def month_range(year: int, month: int):
    """Return (start, end) datetime for the given month."""
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    return start, end


# ─── Report formatting ────────────────────────────────────────────────────────

def build_report(month_label: str, usage: dict, stock: dict) -> str:
    col_w = 36
    sold_header = f"Sold ({month_label})"
    lines = [
        f":package: *Sticker Order Report — {month_label}*",
        f"_'Sold' = units sold in {month_label} · 'Stock' = current on-hand count · 'Order' = qty to purchase_\n",
        "```",
        f"{'Sticker':<{col_w}} {sold_header:>16}  {'Stock':>5}  {'Order':>5}",
        f"{'─' * col_w} {'─'*16}  {'─'*5}  {'─'*5}",
    ]

    grand_total_order = 0

    for category, stickers in REPORT_CATEGORIES.items():
        cat_lines = []
        for s in stickers:
            used    = usage.get(s, 0)
            in_stock = stock.get(s, 0)
            to_order = max(0, used - in_stock)
            grand_total_order += to_order
            # Only show rows with activity
            if used > 0 or in_stock > 0:
                flag = "  <-- LOW" if in_stock > 0 and in_stock < used * 0.25 else ""
                cat_lines.append(
                    f"  {s:<{col_w - 2}} {used:>16}  {in_stock:>5}  {to_order:>5}{flag}"
                )

        if cat_lines:
            lines.append(f"\n  {category}")
            lines.extend(cat_lines)

    lines += [
        f"\n{'─' * (col_w + 32)}",
        f"  {'TOTAL TO ORDER':<{col_w - 2}} {'':>16}  {'':>5}  {grand_total_order:>5}",
        "```",
        "\n_To update stock counts after your physical count, post the counts in #cannibot-chat and ask me to update them._",
    ]

    return "\n".join(lines)


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    # Parse optional --month YYYY-MM argument
    year  = None
    month = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--month" and i + 1 < len(sys.argv[1:]):
            y, m = sys.argv[i + 2].split("-")
            year, month = int(y), int(m)

    now = datetime.now(timezone.utc)
    if year is None:
        # Default: last calendar month
        month = now.month - 1 if now.month > 1 else 12
        year  = now.year if now.month > 1 else now.year - 1

    start, end = month_range(year, month)
    month_label = start.strftime("%B %Y")

    print(f"Calculating sticker usage for {month_label}...")

    print("  Fetching flower product IDs...")
    flower_ids = get_flower_product_ids()
    print(f"  Found {len(flower_ids)} flower products")

    print("  Fetching orders...")
    orders = get_orders(start, end)
    online = sum(1 for o in orders if o.get("source_name") != "pos")
    print(f"  Found {len(orders)} orders ({online} online, {len(orders) - online} in-store)")

    print("  Calculating usage...")
    usage = calculate_usage(orders, flower_ids)

    stock = load_stock()

    report = build_report(month_label, usage, stock)
    print("\n" + report)

    print("\nPosting to Slack #stickers-inventory...")
    result = slack_post(report)
    if result.get("ok"):
        print("Done!")
    else:
        print(f"Slack error: {result.get('error')}")


if __name__ == "__main__":
    main()
