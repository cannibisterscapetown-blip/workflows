#!/usr/bin/env python3
"""
Replace the static 3-product grid in the Backwoods template with
Klaviyo's CUSTOMERS_RECENT_PRODUCTS catalog feed (personalised per recipient).
Same HTML pattern used in the live Dynamic .com template (Vjb7AE).
Falls back gracefully — if a slot has no data the cell simply doesn't render.
"""

import requests, re

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

def product_cell(index: int) -> str:
    """One dynamic product cell using CUSTOMERS_RECENT_PRODUCTS feed."""
    feed = "CUSTOMERS_RECENT_PRODUCTS"
    return f"""<td align="center" class="kl-product-cell-stack" style="padding:10px;vertical-align:top;width:33%;">
{{% if feeds.{feed}|index:{index} %}}
{{% with item=feeds.{feed}|index:{index} %}}
{{% with Title=item.title|safe Price=item.price|default:"" %}}
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
{{% endwith %}}
{{% endwith %}}
{{% endif %}}
</td>"""

# Build the 3-cell row
dynamic_row = "\n".join(product_cell(i) for i in range(3))

# New online section to inject
ONLINE_SECTION = f"""  <!-- ── ONLINE SHOP SECTION ── -->
  <tr>
    <td align="center" class="mob-pad" style="padding:32px 40px 16px;background-color:#ffffff;">
      <h2 style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:700;color:#060606;margin:0 0 6px 0;">Based on your recent activity 🛒</h2>
      <p style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#666666;margin:0;">Order premium flower from the comfort of home.</p>
    </td>
  </tr>
  <tr>
    <td class="mob-pad" style="padding:16px 30px 36px;background-color:#ffffff;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          {dynamic_row}
        </tr>
      </table>
    </td>
  </tr>"""

# Fetch current template
resp = requests.get(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS)
resp.raise_for_status()
html = resp.json()["data"]["attributes"]["html"]
print(f"Fetched template ({len(html):,} chars)")

# Replace the existing online shop section (everything from <!-- ── ONLINE SHOP SECTION ──
# through the closing </tr> of the product grid) with our dynamic version
old_section_start = html.find("<!-- ── ONLINE SHOP SECTION ──")
old_section_end = html.find("<!-- ── SHOP ALL CTA ──")

if old_section_start == -1 or old_section_end == -1:
    print("ERROR: Could not find section markers — check template HTML")
    exit(1)

new_html = html[:old_section_start] + ONLINE_SECTION + "\n\n  " + html[old_section_end:]
print(f"Replaced static section with dynamic feed section ({len(new_html):,} chars)")

# Save locally
with open("/home/user/workflows/backwoods_template_v4.html", "w") as f:
    f.write(new_html)
print("Saved to backwoods_template_v4.html")

# Push to Klaviyo
payload = {"data": {"type": "template", "id": TEMPLATE_ID, "attributes": {"html": new_html}}}
resp = requests.patch(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS, json=payload)
if resp.status_code in (200, 204):
    print(f"✓ Template updated (HTTP {resp.status_code})")
else:
    print(f"✗ Error {resp.status_code}: {resp.text[:500]}")
