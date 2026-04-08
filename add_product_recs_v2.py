#!/usr/bin/env python3
"""
Add static fallback products to the CUSTOMERS_RECENT_PRODUCTS section.
If a recipient has no feed data (new customer / no history), they'll see
the 3 curated products instead of empty cells.
"""

import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"
HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

FALLBACK_PRODUCTS = [
    {
        "name": "Sinister Minister",
        "price": "R 175",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/SinisterMinister.png?v=1774612750",
        "url": "https://cannibisters.com/products/sinister-minister",
    },
    {
        "name": "High Mac",
        "price": "R 190",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/HighMac.png?v=1774612771",
        "url": "https://cannibisters.com/products/high-mac",
    },
    {
        "name": "Lemon Cherry Gelato",
        "price": "R 200",
        "img": "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Lemon_Cherry_Gelato_Cannibisters_Discover_with_Leigh_Photography_12.03_1.jpg?v=1773388867",
        "url": "https://cannibisters.com/products/lemon-cherry-gelato",
    },
]

def static_cell(p):
    return f"""<td align="center" class="kl-product-cell-stack" style="padding:10px;vertical-align:top;width:33%;">
<table align="center" border="0" cellpadding="0" cellspacing="0" style="table-layout:fixed;height:100%;" width="100%">
<tbody>
<tr>
  <td align="center">
    <a href="{p['url']}" style="color:#ff9501;text-decoration:none;">
      <img alt="{p['name']}" src="{p['img']}" width="150"
           style="display:block;width:150px;height:150px;max-width:150px;border-radius:8px;margin:0 auto;object-fit:cover;"/>
    </a>
  </td>
</tr>
<tr>
  <td align="center" style="padding-top:8px;">
    <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:700;color:#060606;margin:0 0 3px 0;line-height:1.3;">{p['name']}</p>
    <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#666666;margin:0 0 12px 0;">{p['price']}</p>
  </td>
</tr>
<tr>
  <td align="center">
    <table border="0" cellpadding="0" cellspacing="0" style="margin:0 auto;">
      <tr>
        <td align="center" bgcolor="#ff9501" style="border-radius:6px;">
          <a href="{p['url']}" style="display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#000000;text-decoration:none;padding:10px 20px;">Shop now</a>
        </td>
      </tr>
    </table>
  </td>
</tr>
</tbody>
</table>
</td>"""

def dynamic_cell(index):
    feed = "CUSTOMERS_RECENT_PRODUCTS"
    return (
        f"""{{% if feeds.{feed}|index:{index} %}}"""
        f"""{{% with item=feeds.{feed}|index:{index} %}}"""
        f"""{{% with Title=item.title|safe Price=item.price|default:"" %}}"""
        f"""<td align="center" class="kl-product-cell-stack" style="padding:10px;vertical-align:top;width:33%;">
<table align="center" border="0" cellpadding="0" cellspacing="0" style="table-layout:fixed;height:100%;" width="100%">
<tbody>
<tr>
  <td align="center">
    <a href="{{{{ item.url }}}}" style="color:#ff9501;text-decoration:none;">
      <img alt="Image of {{{{ Title }}}}" src="{{{{ item.image_full_url }}}}" width="150"
           style="display:block;width:150px;height:150px;max-width:150px;border-radius:8px;margin:0 auto;object-fit:cover;"/>
    </a>
  </td>
</tr>
<tr>
  <td align="center" style="padding-top:8px;">
    <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:700;color:#060606;margin:0 0 3px 0;line-height:1.3;">{{{{ Title }}}}</p>
    <p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#666666;margin:0 0 12px 0;">{{{{ Price }}}}</p>
  </td>
</tr>
<tr>
  <td align="center">
    <table border="0" cellpadding="0" cellspacing="0" style="margin:0 auto;">
      <tr>
        <td align="center" bgcolor="#ff9501" style="border-radius:6px;">
          <a href="{{{{ item.url }}}}" style="display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:#000000;text-decoration:none;padding:10px 20px;">Shop now</a>
        </td>
      </tr>
    </table>
  </td>
</tr>
</tbody>
</table>
</td>"""
        f"""{{% endwith %}}{{% endwith %}}{{% endif %}}"""
    )

# Build the new product section with fallback logic:
# If the feed has ANY data → show personalised products
# Else → show static curated picks
dynamic_cells = "\n".join(dynamic_cell(i) for i in range(3))
static_cells = "\n".join(static_cell(p) for p in FALLBACK_PRODUCTS)

NEW_ONLINE_SECTION = f"""  <!-- ── ONLINE SHOP SECTION ── -->
  <tr>
    <td align="center" class="mob-pad" style="padding:32px 40px 10px;background-color:#ffffff;">
      {{% if feeds.CUSTOMERS_RECENT_PRODUCTS|index:0 %}}
      <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 6px 0;">Based on your recent activity 🛒</h2>
      {{% else %}}
      <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 6px 0;">Popular right now 🛒</h2>
      {{% endif %}}
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#666666;margin:0;">Order premium flower from the comfort of home.</p>
    </td>
  </tr>
  <!-- Dynamic: show personalised recent products if available -->
  {{% if feeds.CUSTOMERS_RECENT_PRODUCTS|index:0 %}}
  <tr>
    <td class="mob-pad" style="padding:16px 30px 36px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          {dynamic_cells}
        </tr>
      </table>
    </td>
  </tr>
  {{% else %}}
  <!-- Fallback: curated picks for new / inactive customers -->
  <tr>
    <td class="mob-pad" style="padding:16px 30px 36px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          {static_cells}
        </tr>
      </table>
    </td>
  </tr>
  {{% endif %}}"""

# Fetch current template
resp = requests.get(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS)
resp.raise_for_status()
html = resp.json()["data"]["attributes"]["html"]

start = html.find("<!-- ── ONLINE SHOP SECTION ──")
end   = html.find("<!-- ── SHOP ALL CTA ──")

if start == -1 or end == -1:
    print("ERROR: section markers not found")
    exit(1)

new_html = html[:start] + NEW_ONLINE_SECTION + "\n\n  " + html[end:]
print(f"Rebuilt product section with fallback ({len(new_html):,} chars)")

with open("/home/user/workflows/backwoods_template_v5.html", "w") as f:
    f.write(new_html)

payload = {"data": {"type": "template", "id": TEMPLATE_ID, "attributes": {"html": new_html}}}
resp = requests.patch(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS, json=payload)
if resp.status_code in (200, 204):
    print(f"✓ Template updated (HTTP {resp.status_code})")
else:
    print(f"✗ {resp.status_code}: {resp.text[:400]}")
