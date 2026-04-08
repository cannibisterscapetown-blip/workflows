#!/usr/bin/env python3
import requests, re

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"
NEW_BANNER = "https://cdn.shopify.com/s/files/1/0631/7749/0644/files/Gemini_Generated_Image_3sv4in3sv4in3sv4.png?v=1775640042"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

resp = requests.get(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS)
resp.raise_for_status()
html = resp.json()["data"]["attributes"]["html"]

html, n = re.subn(r'(src=")([^"]*Gemini_Generated_Image[^"]*)(")', rf'\g<1>{NEW_BANNER}\3', html)
print(f"Replaced {n} banner URL(s).")

payload = {"data": {"type": "template", "id": TEMPLATE_ID, "attributes": {"html": html}}}
resp = requests.patch(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS, json=payload)
resp.raise_for_status()
print(f"Template updated. Status: {resp.status_code}")
