#!/usr/bin/env python3
"""
Final template update:
1. Fix R550 sentence (grammar issue from prior replacement)
2. Insert banner image between header and hero
"""

import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"
BANNER_URL = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Gemini_Generated_Image_6tloi16tloi16tlo.png?v=1775639363"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

def get_template():
    url = f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["data"]["attributes"]["html"]

def update_template(html: str):
    url = f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/"
    payload = {
        "data": {
            "type": "template",
            "id": TEMPLATE_ID,
            "attributes": {"html": html}
        }
    }
    resp = requests.patch(url, headers=HEADERS, json=payload)
    if resp.status_code not in (200, 204):
        print(f"Error {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
    return resp.json()

# --- Fetch current template ---
print("Fetching current template HTML...")
html = get_template()
print(f"  Length: {len(html)} chars")

# --- Fix 1: R550 copy — clean the garbled sentence ---
old_r550 = (
    "Rolled exclusively with our finest top-shelf rolled with 2 grams of our most premium flower."
)
new_r550 = (
    "Rolled with 2 grams of our most premium flower."
)

if old_r550 in html:
    html = html.replace(old_r550, new_r550)
    print("  R550 sentence fixed.")
else:
    print("  WARNING: expected R550 phrase not found — check template manually.")

# --- Fix 2: Insert banner image between HEADER and HERO ---
BANNER_ROW = f"""<!-- ═══ BANNER ═══ -->
<tr>
<td style="padding:0; line-height:0; font-size:0;">
<img alt="Pre Rolled Backwoods — Cannibisters" src="{BANNER_URL}" style="display:block; width:100%; max-width:600px; height:auto; border:0;" width="600"/>
</td>
</tr>"""

# Insertion point: right before <!-- ═══ HERO ═══ -->
marker = "<!-- ═══ HERO ═══ -->"
if marker in html:
    html = html.replace(marker, BANNER_ROW + "\n" + marker)
    print("  Banner image inserted before hero section.")
else:
    print("  WARNING: hero marker not found — banner not inserted.")

# --- Save locally ---
with open("/home/user/workflows/backwoods_template_final.html", "w") as f:
    f.write(html)
print("  Saved to backwoods_template_final.html")

# --- Push to Klaviyo ---
print("\nPushing to Klaviyo...")
result = update_template(html)
print(f"  Template updated. Name: {result['data']['attributes']['name']}")
print("  Done.")
