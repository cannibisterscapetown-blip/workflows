#!/usr/bin/env python3
import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"
OLD_BANNER = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Gemini_Generated_Image_6tloi16tloi16tlo.png?v=1775639363"
NEW_BANNER = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Gemini_Generated_Image_slmk0qslmk0qslmk.png?v=1775639565"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

resp = requests.get(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS)
resp.raise_for_status()
html = resp.json()["data"]["attributes"]["html"]

if OLD_BANNER in html:
    html = html.replace(OLD_BANNER, NEW_BANNER)
    print("Banner URL swapped.")
else:
    print("Old URL not found — replacing any banner img src directly...")
    import re
    html, n = re.subn(r'(src=")([^"]+Gemini_Generated_Image[^"]+)(")', rf'\g<1>{NEW_BANNER}\3', html)
    print(f"  Replaced {n} occurrence(s).")

payload = {"data": {"type": "template", "id": TEMPLATE_ID, "attributes": {"html": html}}}
resp = requests.patch(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS, json=payload)
resp.raise_for_status()
print(f"Template updated. Status: {resp.status_code}")
