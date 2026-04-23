#!/usr/bin/env python3
"""
Durban Poison Back-in-Stock — Klaviyo Email Campaign Creator
Creates the HTML template and campaign via Klaviyo API using curl (DNS workaround).
"""

import subprocess
import json
import sys

KLAVIYO_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
SHOP_URL = "cannibisters.com"

HEADERS = [
    "-H", f"Authorization: Klaviyo-API-Key {KLAVIYO_KEY}",
    "-H", "revision: 2024-10-15",
    "-H", "Content-Type: application/json",
    "-H", "Accept: application/json",
]

def klaviyo_get(path):
    result = subprocess.run(
        ["curl", "-s", f"https://a.klaviyo.com{path}"] + HEADERS,
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def klaviyo_post(path, payload):
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", f"https://a.klaviyo.com{path}"] + HEADERS +
        ["-d", json.dumps(payload)],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def klaviyo_patch(path, payload):
    result = subprocess.run(
        ["curl", "-s", "-X", "PATCH", f"https://a.klaviyo.com{path}"] + HEADERS +
        ["-d", json.dumps(payload)],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


# ── Product data pulled from Shopify ──────────────────────────────────────────

DURBAN = {
    "title": "Premium Durban Poison",
    "price": "R240",
    "handle": "durban-poison-living-soil",
    "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Durban_poison_budshot_1.png?v=1776669088",
}

NEW_ARRIVALS = [
    {
        "title": "Red Velvet Gary",
        "price": "R200",
        "handle": "red-velvet",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/20240726_131713.jpg?v=1722267168",
    },
    {
        "title": "Colt 45",
        "price": "R200",
        "handle": "colt-45",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Colt_45.png?v=1772799342",
    },
    {
        "title": "Elvis",
        "price": "R200",
        "handle": "elvis-90-10-sativa",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/elvis.jpg?v=1740402820",
    },
]

FAN_FAVOURITES = [
    {
        "title": "Premium Lion's Bread",
        "price": "R240",
        "handle": "lions-bread",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Lions_bread_183fdfd4-f2f0-4582-94bb-72b688e47d89.jpg?v=1752828397",
    },
    {
        "title": "Jessica Rabbit",
        "price": "R200",
        "handle": "jessica-rabbit",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Jessica_Rabbit_Cannibister_Discover_with_Leigh_Photography_03.03.26_2_of_5.jpg?v=1772611089",
    },
    {
        "title": "Acapulco Gold",
        "price": "R200",
        "handle": "acapulco-gold",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Acapulco_gold.jpg?v=1740402820",
    },
]

HASH = [
    {
        "title": "Afghan Mazar Sharif Hash",
        "price": "R450",
        "handle": "afghan-mazar-sharif-hash",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/HashRosin.png?v=1763716214",
    },
    {
        "title": "Bubble Hash — Bruce Banner",
        "price": "R450",
        "handle": "bubble-hash-bruce-banner",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/products/BruceBannerHash.png?v=1669130132",
    },
    {
        "title": "Light Bringer Hash Rosin",
        "price": "R1240",
        "handle": "light-bringer-hash-rosin",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Light_bringer.jpg?v=1760619918",
    },
]

MEMBERSHIP = [
    {
        "title": "30 Day Membership",
        "price": "R100",
        "handle": "cannibisters-the-herbal-apothecary-30-day-membership",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/30day_membership.png?v=1711745615",
    },
    {
        "title": "3 Month Membership",
        "price": "R300",
        "handle": "cannibisters-the-herbal-apothecary-3-month-membership",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/3month_membership.png?v=1711745656",
    },
    {
        "title": "12 Month Membership",
        "price": "R1000",
        "handle": "cannibisters-the-herbal-apothecary-12-month-membership",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/12month_membership.png?v=1711745687",
    },
]


# ── HTML email builder ─────────────────────────────────────────────────────────

def product_card(product, shop_url):
    url = f"https://{shop_url}/products/{product['handle']}"
    return f"""
<td class="kl-product-cell-stack" style="width:33.33%;padding:8px;vertical-align:top;" valign="top">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:#ffffff;border-radius:8px;overflow:hidden;">
    <tr>
      <td style="padding:0;">
        <a href="{url}" style="display:block;text-decoration:none;">
          <img src="{product['img']}" alt="{product['title']}"
               style="display:block;width:100%;height:180px;object-fit:cover;border-radius:8px 8px 0 0;" />
        </a>
      </td>
    </tr>
    <tr>
      <td style="padding:12px;">
        <p style="margin:0 0 4px 0;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#1a1a1a;line-height:1.3;">{product['title']}</p>
        <p style="margin:0 0 10px 0;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#ff9501;font-weight:700;">{product['price']}</p>
        <a href="{url}"
           style="display:inline-block;background:#1a1a1a;color:#ffffff;font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;text-decoration:none;padding:7px 14px;border-radius:4px;letter-spacing:0.5px;">
          SHOP NOW
        </a>
      </td>
    </tr>
  </table>
</td>"""


def section_header(title, subtitle=""):
    sub_html = f'<p style="margin:6px 0 0 0;font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#666666;">{subtitle}</p>' if subtitle else ""
    return f"""
<tr>
  <td style="padding:32px 24px 16px 24px;text-align:center;background:#fff8ee;">
    <h2 style="margin:0;font-family:Helvetica,Arial,sans-serif;font-size:22px;font-weight:900;color:#1a1a1a;letter-spacing:2px;text-transform:uppercase;">{title}</h2>
    {sub_html}
    <div style="width:40px;height:3px;background:#ff9501;margin:12px auto 0;"></div>
  </td>
</tr>"""


def product_row(products, shop_url):
    cards = "".join(product_card(p, shop_url) for p in products)
    return f"""
<tr>
  <td style="padding:0 16px 24px 16px;background:#fff8ee;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
      <tr>
        {cards}
      </tr>
    </table>
  </td>
</tr>"""


def membership_cards(memberships, shop):
    cards = []
    for m in memberships:
        cards.append(f"""
          <td class="kl-product-cell-stack" style="width:33.33%;padding:8px;vertical-align:top;" valign="top">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:#2a2a2a;border-radius:8px;overflow:hidden;">
              <tr>
                <td style="padding:0;">
                  <a href="https://{shop}/products/{m['handle']}" style="display:block;text-decoration:none;">
                    <img src="{m['img']}" alt="{m['title']}"
                         style="display:block;width:100%;height:150px;object-fit:cover;border-radius:8px 8px 0 0;" />
                  </a>
                </td>
              </tr>
              <tr>
                <td style="padding:12px;">
                  <p style="margin:0 0 4px 0;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#ffffff;line-height:1.3;">{m['title']}</p>
                  <p style="margin:0 0 10px 0;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#ff9501;font-weight:700;">{m['price']}</p>
                  <a href="https://{shop}/products/{m['handle']}"
                     style="display:inline-block;background:#ff9501;color:#000000;font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;text-decoration:none;padding:7px 14px;border-radius:4px;letter-spacing:0.5px;">
                    JOIN NOW
                  </a>
                </td>
              </tr>
            </table>
          </td>""")
    return "".join(cards)


def effect_pills():
    effects = ["Pure Sativa", "Energetic", "Creative", "Uplifting", "Stress Relief", "Anise &amp; Pine", "Landrace Heritage"]
    pills = []
    for e in effects:
        pills.append(
            f'<span style="display:inline-block;background:#1a2e1a;color:#d4a017;font-family:Helvetica,Arial,sans-serif;'
            f'font-size:11px;font-weight:700;padding:5px 12px;border-radius:20px;margin:3px 3px 3px 0;'
            f'border:1px solid #d4a01740;">{e}</span>'
        )
    return "".join(pills)


def build_email_html():
    shop = SHOP_URL

    return f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Durban Poison — Back in Stock | Cannibisters</title>
<style>
  body {{ margin:0;padding:0;background:#f0ece4;-webkit-text-size-adjust:100%; }}
  table,td {{ border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0; }}
  img {{ border:0;line-height:100%;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic; }}
  p {{ display:block;margin:13px 0; }}
  a {{ color:#ff9501; }}
  @media only screen and (max-width:480px) {{
    .kl-product-cell-stack {{ display:block !important;width:100% !important;padding:8px 0 !important; }}
    .hero-title {{ font-size:28px !important;line-height:1.2 !important; }}
    .hero-sub {{ font-size:14px !important; }}
    .mobile-pad {{ padding-left:16px !important;padding-right:16px !important; }}
    .desktop-hide {{ display:none !important; }}
  }}
</style>
</head>
<body>
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:#f0ece4;font-family:Helvetica,Arial,sans-serif;">
<tr>
<td align="center" style="padding:20px 10px;">

<!-- ══ EMAIL WRAPPER ══════════════════════════════════════════════════ -->
<table border="0" cellpadding="0" cellspacing="0" width="600" style="max-width:600px;width:100%;">

  <!-- ── HEADER / LOGO ─────────────────────────────────────────────── -->
  <tr>
    <td style="background:#1a1a1a;padding:20px 24px;text-align:center;border-radius:12px 12px 0 0;">
      <a href="https://{shop}" style="text-decoration:none;">
        <span style="font-family:Helvetica,Arial,sans-serif;font-size:22px;font-weight:900;color:#ffffff;letter-spacing:3px;text-transform:uppercase;">CANNIBISTERS</span>
        <span style="display:block;font-family:Helvetica,Arial,sans-serif;font-size:10px;font-weight:400;color:#ff9501;letter-spacing:4px;margin-top:2px;text-transform:uppercase;">The Herbal Apothecary</span>
      </a>
    </td>
  </tr>

  <!-- ── HERO — DURBAN POISON ──────────────────────────────────────── -->
  <tr>
    <td style="background:#0d1a0d;padding:0;position:relative;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td style="padding:0;">
            <img src="{DURBAN['img']}"
                 alt="Durban Poison — Premium South African Sativa"
                 style="display:block;width:100%;max-height:420px;object-fit:cover;" width="600"/>
          </td>
        </tr>
        <tr>
          <td style="background:linear-gradient(to bottom,rgba(13,26,13,0),#0d1a0d);padding:0 32px 36px 32px;text-align:center;" class="mobile-pad">
            <!-- Limited badge -->
            <div style="display:inline-block;background:#b8860b;color:#ffffff;font-family:Helvetica,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 14px;border-radius:20px;margin-bottom:16px;">
              ⚡ LIMITED STOCK — BACK IN STOCK
            </div>
            <h1 class="hero-title" style="margin:0 0 8px 0;font-family:Helvetica,Arial,sans-serif;font-size:42px;font-weight:900;color:#ffffff;line-height:1.1;letter-spacing:1px;">
              Durban Poison
            </h1>
            <p class="hero-sub" style="margin:0 0 6px 0;font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#d4a017;font-weight:700;letter-spacing:2px;text-transform:uppercase;">
              South Africa's Finest Landrace Sativa
            </p>
            <p style="margin:0;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#aaaaaa;letter-spacing:1px;">
              Pure Sativa · Indoor · {DURBAN['price']} per gram
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── COPY SECTION ───────────────────────────────────────────────── -->
  <tr>
    <td style="background:#0d1a0d;padding:0 40px 40px 40px;" class="mobile-pad">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td style="border-top:1px solid #d4a01740;padding-top:28px;">
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.8;color:#e0e0e0;margin:0 0 16px 0;">
              Durban Poison is not just a strain — it's a <strong style="color:#d4a017;">living piece of South African heritage</strong>. One of the oldest surviving cannabis landraces on earth, it was cultivated in the hills outside Durban long before the modern seed industry existed, shaped by the soil, sun and culture of our continent over hundreds of years.
            </p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.8;color:#e0e0e0;margin:0 0 16px 0;">
              Where most modern strains are engineered hybrids, Durban Poison is something rarer: <em>a pure expression</em>. No crossing, no tampering — just a proud, unadulterated sativa that delivers the kind of clean, soaring energy you simply cannot manufacture. Expect a sharp, anise-sweet aroma, electric cerebral clarity, and a creativity boost that's earned this strain a global cult following.
            </p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.8;color:#e0e0e0;margin:0 0 24px 0;">
              We don't always have it. When we do, it moves fast. <strong style="color:#ff9501;">This is your window — don't sleep on it.</strong>
            </p>
            <!-- Effect pills -->
            <p style="margin:0 0 8px 0;font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#888888;letter-spacing:1px;text-transform:uppercase;">Effects &amp; Profile</p>
            <div style="margin-bottom:28px;">
              {effect_pills()}
            </div>
            <!-- CTA -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td align="center">
                  <a href="https://{shop}/products/{DURBAN['handle']}"
                     style="display:inline-block;background:#d4a017;color:#0d1a0d;font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:900;text-decoration:none;padding:15px 40px;border-radius:6px;letter-spacing:1.5px;text-transform:uppercase;">
                    Shop Durban Poison — {DURBAN['price']}
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── DIVIDER ────────────────────────────────────────────────────── -->
  <tr>
    <td style="background:#d4a017;height:4px;font-size:0;line-height:0;">&nbsp;</td>
  </tr>

  <!-- ══ NEW ARRIVALS ══════════════════════════════════════════════════ -->
  {section_header("New Arrivals", "Fresh to the Apothecary")}
  {product_row(NEW_ARRIVALS, shop)}
  <tr>
    <td style="background:#fff8ee;padding:0 24px 32px 24px;text-align:center;">
      <a href="https://{shop}/collections/all?sort_by=created-descending"
         style="display:inline-block;background:transparent;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:10px 28px;border:2px solid #1a1a1a;border-radius:4px;letter-spacing:1px;text-transform:uppercase;">
        View All New Arrivals →
      </a>
    </td>
  </tr>

  <!-- ── DIVIDER ────────────────────────────────────────────────────── -->
  <tr>
    <td style="background:#e8e0d0;height:2px;font-size:0;line-height:0;">&nbsp;</td>
  </tr>

  <!-- ══ FAN FAVOURITES ════════════════════════════════════════════════ -->
  {section_header("Fan Favourites", "The strains our community keeps coming back for")}
  {product_row(FAN_FAVOURITES, shop)}
  <tr>
    <td style="background:#fff8ee;padding:0 24px 32px 24px;text-align:center;">
      <a href="https://{shop}/collections/premium-bud"
         style="display:inline-block;background:transparent;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:10px 28px;border:2px solid #1a1a1a;border-radius:4px;letter-spacing:1px;text-transform:uppercase;">
        Browse Fan Favourites →
      </a>
    </td>
  </tr>

  <!-- ── DIVIDER ────────────────────────────────────────────────────── -->
  <tr>
    <td style="background:#e8e0d0;height:2px;font-size:0;line-height:0;">&nbsp;</td>
  </tr>

  <!-- ══ HASH ══════════════════════════════════════════════════════════ -->
  {section_header("Hash", "Concentrated. Crafted. Coveted.")}
  {product_row(HASH, shop)}
  <tr>
    <td style="background:#fff8ee;padding:0 24px 32px 24px;text-align:center;">
      <a href="https://{shop}/collections/extracts-and-concentrates"
         style="display:inline-block;background:transparent;color:#1a1a1a;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:10px 28px;border:2px solid #1a1a1a;border-radius:4px;letter-spacing:1px;text-transform:uppercase;">
        Explore Hash &amp; Concentrates →
      </a>
    </td>
  </tr>

  <!-- ── DIVIDER ────────────────────────────────────────────────────── -->
  <tr>
    <td style="background:#e8e0d0;height:2px;font-size:0;line-height:0;">&nbsp;</td>
  </tr>

  <!-- ══ MEMBERSHIP ════════════════════════════════════════════════════ -->
  <tr>
    <td style="background:#1a1a1a;padding:32px 24px 16px 24px;text-align:center;">
      <h2 style="margin:0;font-family:Helvetica,Arial,sans-serif;font-size:22px;font-weight:900;color:#ffffff;letter-spacing:2px;text-transform:uppercase;">Membership</h2>
      <p style="margin:6px 0 0 0;font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#aaaaaa;">Join the Apothecary. Get exclusive access, member pricing &amp; more.</p>
      <div style="width:40px;height:3px;background:#ff9501;margin:12px auto 0;"></div>
    </td>
  </tr>
  <tr>
    <td style="background:#1a1a1a;padding:0 16px 8px 16px;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          {membership_cards(MEMBERSHIP, shop)}
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="background:#1a1a1a;padding:8px 24px 32px 24px;text-align:center;">
      <a href="https://{shop}/collections/membership"
         style="display:inline-block;background:transparent;color:#ffffff;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;text-decoration:none;padding:10px 28px;border:2px solid #ff9501;border-radius:4px;letter-spacing:1px;text-transform:uppercase;">
        View All Memberships →
      </a>
    </td>
  </tr>

  <!-- ── FOOTER ─────────────────────────────────────────────────────── -->
  <tr>
    <td style="background:#111111;padding:28px 32px;text-align:center;border-radius:0 0 12px 12px;" class="mobile-pad">
      <p style="margin:0 0 8px 0;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#ffffff;font-weight:700;letter-spacing:2px;text-transform:uppercase;">
        Cannibisters — The Herbal Apothecary
      </p>
      <p style="margin:0 0 8px 0;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;">
        65 Regent Rd, Sea Point, Cape Town · high@cannibisters.com · 066 344 3012
      </p>
      <p style="margin:0 0 16px 0;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;">
        <a href="https://{shop}" style="color:#ff9501;text-decoration:none;">cannibisters.com</a>
      </p>
      <p style="margin:0;font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#555555;line-height:1.6;">
        You are receiving this email because you subscribed to updates from Cannibisters.<br/>
        <a href="{{{{ unsubscribe_url }}}}" style="color:#555555;text-decoration:underline;">Unsubscribe</a> ·
        <a href="{{{{ view_in_browser_url }}}}" style="color:#555555;text-decoration:underline;">View in browser</a>
      </p>
    </td>
  </tr>

</table>
<!-- ══ END EMAIL WRAPPER ══════════════════════════════════════════════ -->

</td>
</tr>
</table>
</body>
</html>"""


def main():
    print("=" * 60)
    print("Cannibisters — Durban Poison Campaign Creator")
    print("=" * 60)

    # 1. Build HTML
    print("\n[1] Building email HTML...")
    html = build_email_html()
    print(f"    HTML generated: {len(html):,} characters")

    # Save local copy
    with open("/home/user/workflows/durban_poison_email.html", "w") as f:
        f.write(html)
    print("    Saved to: durban_poison_email.html")

    # 2. Create Klaviyo template
    print("\n[2] Creating Klaviyo template...")
    template_payload = {
        "data": {
            "type": "template",
            "attributes": {
                "name": "Durban Poison — Back in Stock (Apr 2026)",
                "editor_type": "CODE",
                "html": html,
                "text": (
                    "DURBAN POISON IS BACK\n\n"
                    "One of the oldest cannabis landraces on earth — a proudly South African pure sativa — "
                    "is back in limited stock at Cannibisters.\n\n"
                    f"Shop now: https://{SHOP_URL}/products/{DURBAN['handle']}\n\n"
                    "— The Cannibisters Team"
                ),
            }
        }
    }
    template_resp = klaviyo_post("/api/templates/", template_payload)

    if "errors" in template_resp:
        print(f"    ERROR: {template_resp['errors']}")
        return None, None

    template_id = template_resp.get("data", {}).get("id")
    if not template_id:
        print(f"    ERROR: No template ID in response: {template_resp}")
        return None, None

    print(f"    Template created: {template_id}")

    # 3. Create campaign
    print("\n[3] Creating Klaviyo campaign...")
    campaign_payload = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": "Durban Poison — Back in Stock (Apr 2026)",
                "audiences": {
                    "included": ["S9bF86", "REpHsC"],
                    "excluded": []
                },
                "send_options": {
                    "use_smart_sending": True,
                    "ignore_unsubscribes": False
                },
                "tracking_options": {
                    "add_tracking_params": True,
                    "custom_tracking_params": [
                        {"type": "static", "value": "klaviyo", "name": "utm_source"},
                        {"type": "static", "value": "email", "name": "utm_medium"},
                        {"type": "static", "value": "durban-poison-restock", "name": "utm_campaign"},
                    ],
                    "is_tracking_clicks": True,
                    "is_tracking_opens": True
                },
                "send_strategy": {
                    "method": "static",
                    "options_static": {
                        "datetime": "2026-04-24T09:00:00+02:00",
                        "is_local": True,
                        "send_past_recipients_immediately": True
                    }
                },
                "campaign-messages": {
                    "data": [
                        {
                            "type": "campaign-message",
                            "attributes": {
                                "channel": "email",
                                "label": "Durban Poison — Back in Stock",
                                "content": {
                                    "subject": "🌿 She's Back. Durban Poison — Limited Stock Available Now",
                                    "preview_text": "One of Africa's oldest landraces returns to the Apothecary. Don't miss it.",
                                    "from_email": "high@cannibisters.com",
                                    "reply_to_email": "high@cannibisters.com",
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
    campaign_resp = klaviyo_post("/api/campaigns/", campaign_payload)

    if "errors" in campaign_resp:
        print(f"    ERROR: {campaign_resp['errors']}")
        return template_id, None

    campaign_id = campaign_resp.get("data", {}).get("id")
    if not campaign_id:
        print(f"    ERROR: No campaign ID: {campaign_resp}")
        return template_id, None

    print(f"    Campaign created: {campaign_id}")

    # 4. Get campaign message ID (auto-created)
    print("\n[4] Fetching campaign message...")
    msg_resp = klaviyo_get(f"/api/campaigns/{campaign_id}/campaign-messages/")
    messages = msg_resp.get("data", [])

    if not messages:
        print(f"    ERROR: No messages found: {msg_resp}")
        return template_id, campaign_id

    msg_id = messages[0]["id"]
    print(f"    Message ID: {msg_id}")

    # 5. Update message with correct subject and sender details
    print("\n[5] Updating campaign message with email content...")
    message_payload = {
        "data": {
            "type": "campaign-message",
            "id": msg_id,
            "attributes": {
                "content": {
                    "subject": "🌿 She's Back. Durban Poison — Limited Stock Available Now",
                    "preview_text": "One of Africa's oldest landraces returns to the Apothecary. Don't miss it.",
                    "from_email": "high@cannibisters.com",
                    "from_label": "Cannibisters",
                    "reply_to_email": "high@cannibisters.com",
                }
            }
        }
    }
    msg_update = klaviyo_patch(f"/api/campaign-messages/{msg_id}/", message_payload)
    if "errors" in msg_update:
        print(f"    ERROR: {msg_update['errors']}")
    else:
        print("    Message content updated (subject, from, preview text)")

    # 6. Assign template to campaign message via campaign-message-assign-template action
    print("\n[6] Assigning HTML template to campaign message...")
    assign_result = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"https://a.klaviyo.com/api/campaign-message-assign-template/"] +
        HEADERS +
        ["-d", json.dumps({
            "data": {
                "type": "campaign-message",
                "id": msg_id,
                "relationships": {
                    "template": {"data": {"type": "template", "id": template_id}}
                }
            }
        })],
        capture_output=True, text=True
    )
    try:
        assign_resp = json.loads(assign_result.stdout)
        if "errors" in assign_resp:
            print(f"    ERROR: {assign_resp['errors']}")
        else:
            linked_template = assign_resp.get("data", {}).get("relationships", {}).get("template", {}).get("data", {}).get("id", "unknown")
            print(f"    Template linked as: {linked_template}")
    except Exception:
        print(f"    Response: {assign_result.stdout[:200]}")

    print("\n" + "=" * 60)
    print("CAMPAIGN CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"  Template ID:  {template_id}")
    print(f"  Campaign ID:  {campaign_id}")
    print(f"  Message ID:   {msg_id}")
    print(f"  Scheduled:    24 Apr 2026 @ 09:00 SAST")
    print(f"  Audiences:    Engaged Subscribers + Active Members")
    print(f"  Subject:      🌿 She's Back. Durban Poison — Limited Stock Available Now")
    print()
    print("  Review in Klaviyo:")
    print(f"  https://www.klaviyo.com/campaigns/{campaign_id}/scheduled")
    print("=" * 60)

    return template_id, campaign_id


if __name__ == "__main__":
    main()
