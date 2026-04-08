#!/usr/bin/env python3
"""
Final rebuild of Backwoods template:
- Real Cannibisters brand style (white bg, #ff9501 orange, Helvetica)
- Friendly "Hi Member," tone
- Banner image at top
- Two Backwoods product cards (in-store only, create desire)
- 3-product online shop grid (drive online traffic)
- Scarcity note + CTA
- Correct footer
"""

import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"
BANNER_URL = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Gemini_Generated_Image_slmk0qslmk0qslmk.png?v=1775639565"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

# Online products to feature (from April Specials reference)
FEATURED_PRODUCTS = [
    {
        "name": "Sinister Minister",
        "price": "R 175",
        "type": "Flower",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/SinisterMinister.png?v=1774612750",
        "url": "https://cannibisters.com/products/sinister-minister",
    },
    {
        "name": "High Mac",
        "price": "R 190",
        "type": "Flower",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/HighMac.png?v=1774612771",
        "url": "https://cannibisters.com/products/high-mac",
    },
    {
        "name": "Lemon Cherry Gelato",
        "price": "R 200",
        "type": "Flower",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Lemon_Cherry_Gelato_Cannibisters_Discover_with_Leigh_Photography_12.03_1.jpg?v=1773388867",
        "url": "https://cannibisters.com/products/lemon-cherry-gelato",
    },
]

def product_cell(p):
    """Render a single product card cell (for 3-column grid)."""
    return f"""<td align="center" class="kl-product-cell-stack" style="padding:10px;vertical-align:top;width:33%;" width="33%">
  <a href="{p['url']}"><img src="{p['img']}" alt="{p['name']}" width="150" style="display:block;width:150px;height:150px;max-width:150px;border-radius:8px;margin:0 auto;object-fit:cover;"/></a>
  <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:700;color:#060606;margin:10px 0 3px 0;line-height:1.3;">{p['name']}</p>
  <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#666666;margin:0 0 12px 0;">{p['price']}</p>
  <table border="0" cellpadding="0" cellspacing="0" style="margin:0 auto;">
    <tr>
      <td align="center" bgcolor="#ff9501" style="border-radius:6px;">
        <a href="{p['url']}" style="display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#000000;text-decoration:none;padding:10px 20px;">Shop now</a>
      </td>
    </tr>
  </table>
</td>"""

product_cells = "\n".join(product_cell(p) for p in FEATURED_PRODUCTS)

HTML = f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Pre Rolled Backwoods — Daily Drop | Cannibisters</title>
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings>
  <o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
<style>
body,table,td,p,a,li{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}}
table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;line-height:100%;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;max-width:100%;height:auto;display:block;}}
body{{margin:0;padding:0;background-color:#f5f5f5;}}
p{{margin:0;padding:0;}}
a:link,a:visited,a:active{{color:#ff9501;}}
@media only screen and (max-width:620px){{
  .email-container{{width:100%!important;}}
  .mob-pad{{padding-left:16px!important;padding-right:16px!important;}}
  .kl-product-cell-stack{{display:block!important;width:100%!important;padding-left:0!important;padding-right:0!important;}}
  .hero-title{{font-size:26px!important;line-height:1.3!important;}}
}}
</style>
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f5f5f5;padding:30px 0;">
<tr><td align="center">

<!-- ═══ EMAIL CONTAINER ═══ -->
<table border="0" cellpadding="0" cellspacing="0" class="email-container" width="600" style="max-width:600px;background-color:#ffffff;">

  <!-- ── BANNER IMAGE ── -->
  <tr>
    <td style="padding:0;line-height:0;font-size:0;">
      <img src="{BANNER_URL}" alt="Pre Rolled Backwoods — Cannibisters" width="600" style="width:100%;max-width:600px;display:block;"/>
    </td>
  </tr>

  <!-- ── ORANGE HEADER BAR ── -->
  <tr>
    <td align="center" style="background-color:#ff9501;padding:10px 20px;">
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#000000;margin:0;">Cannibisters Herbal Apothecary &nbsp;·&nbsp; Members Only</p>
    </td>
  </tr>

  <!-- ── INTRO ── -->
  <tr>
    <td align="left" class="mob-pad" style="padding:36px 40px 24px;background-color:#ffffff;">
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#333333;margin:0 0 14px 0;">Hi Member,</p>
      <h1 class="hero-title" style="font-family:Helvetica,Arial,sans-serif;font-size:30px;font-weight:700;line-height:1.25;color:#060606;margin:0 0 16px 0;">
        Pre Rolled Backwoods<br/>are here. 🌿
      </h1>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.7;color:#555555;margin:0;">
        We hand-roll a fresh batch every morning — available in limited quantities, <strong>first come, first served</strong>. Two tiers to choose from today.
      </p>
      <table border="0" cellpadding="0" cellspacing="0" style="margin:22px 0 0;"><tr><td width="48" height="3" style="background-color:#ff9501;border-radius:2px;font-size:0;line-height:0;"> </td></tr></table>
    </td>
  </tr>

  <!-- ── PRODUCT CARD: R420 ── -->
  <tr>
    <td class="mob-pad" style="padding:8px 40px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#fff8ee;border-radius:10px;">
        <tr>
          <td style="padding:26px 28px 22px;">
            <table border="0" cellpadding="0" cellspacing="0" style="margin-bottom:12px;">
              <tr>
                <td style="background-color:#ff9501;border-radius:6px;padding:5px 14px;">
                  <span style="font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#000000;">R 420</span>
                </td>
              </tr>
            </table>
            <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 4px 0;">The Classic Backwood</h2>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#ff9501;margin:0 0 12px 0;">Orange Sherbet</p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:1.7;color:#555555;margin:0 0 16px 0;">
              A smooth, flavour-forward Backwood rolled with our Orange Sherbet selection. Citrus-sweet, clean, and well-crafted — a solid everyday choice.
            </p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0;letter-spacing:0.5px;">In-store only &nbsp;·&nbsp; Available daily while stocks last</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── PRODUCT CARD: R550 ── -->
  <tr>
    <td class="mob-pad" style="padding:16px 40px 28px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#fff8ee;border-radius:10px;border:2px solid #ff9501;">
        <tr>
          <td style="padding:26px 28px 22px;">
            <table border="0" cellpadding="0" cellspacing="0" style="margin-bottom:12px;">
              <tr>
                <td style="background-color:#ff9501;border-radius:6px;padding:5px 14px;">
                  <span style="font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#000000;">R 550 &nbsp;⭐ Top Shelf</span>
                </td>
              </tr>
            </table>
            <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 4px 0;">The Top Shelf Backwood</h2>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#ff9501;margin:0 0 12px 0;">Premium Indoor Selection</p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:1.7;color:#555555;margin:0 0 10px 0;">
              Rolled with 2 grams of our most premium flower. Each day brings a new featured strain from our rotation — including Alien Mints, Queen Sugar, Super Berry Crush and Karamel Cut Throat.
            </p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#ff9501;margin:0 0 16px 0;">Ask your budtender for today's strain 🌿</p>
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#060606;margin:0;letter-spacing:0.5px;">In-store only &nbsp;·&nbsp; Available daily while stocks last</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── SCARCITY BOX ── -->
  <tr>
    <td class="mob-pad" style="padding:0 40px 36px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-left:4px solid #ff9501;background-color:#fff8ee;border-radius:4px;">
        <tr>
          <td style="padding:14px 18px;">
            <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.7;color:#555555;margin:0;">
              <strong style="color:#060606;">Limited quantities. Rolled fresh daily.</strong><br/>
              Available in-store only. We recommend visiting early — once today's batch is gone, it's gone.
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── VISIT US CTA ── -->
  <tr>
    <td align="center" class="mob-pad" style="padding:0 40px 48px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" bgcolor="#ff9501" style="border-radius:8px;">
            <a href="https://www.cannibisters.com" style="display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:15px;font-weight:700;color:#000000;text-decoration:none;padding:15px 44px;">Visit Us In-Store</a>
          </td>
        </tr>
      </table>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#999999;margin:14px 0 0 0;">65 Regent Road, Sea Point, Cape Town &nbsp;·&nbsp; Members only</p>
    </td>
  </tr>

  <!-- ── DIVIDER ── -->
  <tr>
    <td style="padding:0 40px;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><td height="1" style="background-color:#eeeeee;font-size:0;line-height:0;"> </td></tr></table>
    </td>
  </tr>

  <!-- ── ONLINE SHOP SECTION ── -->
  <tr>
    <td align="center" class="mob-pad" style="padding:32px 40px 16px;background-color:#ffffff;">
      <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 6px 0;">Also available online 🛒</h2>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#666666;margin:0;">Order premium flower from the comfort of home.</p>
    </td>
  </tr>
  <tr>
    <td class="mob-pad" style="padding:16px 30px 36px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          {product_cells}
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── SHOP ALL CTA ── -->
  <tr>
    <td align="center" style="padding:0 40px 48px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" bgcolor="#060606" style="border-radius:8px;">
            <a href="https://www.cannibisters.com/collections/all" style="display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:700;color:#ffffff;text-decoration:none;padding:14px 40px;">Shop All Products</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── FOOTER ── -->
  <tr>
    <td align="center" class="mob-pad" style="background-color:#f5f5f5;border-top:1px solid #eeeeee;padding:30px 40px;">
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#333333;margin:0 0 4px 0;">Cannibisters - The Herbal Apothecary</p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;margin:0 0 4px 0;">65 Regent Rd, Sea Point, Cape Town, Western Cape, 8001, South Africa</p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;margin:0 0 4px 0;">087 537 8000 &nbsp;·&nbsp; <a href="mailto:high@cannibisters.com" style="color:#ff9501;text-decoration:none;">high@cannibisters.com</a></p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#888888;margin:0 0 20px 0;"><a href="http://www.cannibisters.com" style="color:#ff9501;text-decoration:none;">www.cannibisters.com</a></p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#aaaaaa;margin:0 0 10px 0;">
        {{% unsubscribe 'Unsubscribe' %}}
      </p>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:10px;color:#cccccc;line-height:1.6;margin:0;">This communication is intended for Cannibisters Club members only.<br/>Private, responsible and members-only. For adults 18+.</p>
    </td>
  </tr>

</table>
<!-- END EMAIL CONTAINER -->

</td></tr>
</table>
</body>
</html>"""

# Save locally
with open("/home/user/workflows/backwoods_template_v3.html", "w") as f:
    f.write(HTML)
print(f"Saved locally ({len(HTML):,} chars)")

# Push to Klaviyo
payload = {
    "data": {
        "type": "template",
        "id": TEMPLATE_ID,
        "attributes": {"html": HTML}
    }
}
resp = requests.patch(
    f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/",
    headers=HEADERS,
    json=payload
)
if resp.status_code in (200, 204):
    print(f"✓ Template updated (HTTP {resp.status_code})")
else:
    print(f"✗ Error {resp.status_code}: {resp.text[:500]}")
