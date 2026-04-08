#!/usr/bin/env python3
import requests

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"
HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

resp = requests.get(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS)
resp.raise_for_status()
html = resp.json()["data"]["attributes"]["html"]

edits = [
    (
        "A smooth, flavour-forward Backwood rolled with our Orange Sherbet selection. Citrus-sweet, clean, and well-crafted — a solid everyday choice.",
        "A smooth, flavour-forward Backwood rolled with Orange Sherbet Flower. Citrus-sweet, clean, and well-crafted — a solid everyday choice."
    ),
    (
        "Rolled with 2 grams of our most premium flower. Each day brings a new featured strain from our rotation — including Alien Mints, Queen Sugar, Super Berry Crush and Karamel Cut Throat.",
        "Rolled with 2 grams of our most premium flower. Each day brings a featured strain from our rotation — including Alien Mints, Queen Sugar, Super Berry Crush, Karamel Cut Throat &amp; more."
    ),
    (
        "Available in-store only. We recommend visiting early — once today's batch is gone, it's gone.",
        "Available in-store only. We roll &amp; restock in the afternoons — once today's batch is gone, it's gone."
    ),
]

for old, new in edits:
    if old in html:
        html = html.replace(old, new)
        print(f"✓ Replaced: {old[:60]}...")
    else:
        print(f"✗ NOT FOUND: {old[:60]}...")

payload = {"data": {"type": "template", "id": TEMPLATE_ID, "attributes": {"html": html}}}
resp = requests.patch(f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/", headers=HEADERS, json=payload)
resp.raise_for_status()
print(f"\nTemplate updated (HTTP {resp.status_code})")
