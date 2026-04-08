#!/usr/bin/env python3
"""
Update Cannibisters Pre Rolled Backwoods email template:
1. Fix R550 copy: "indoor cultivars" -> "rolled with 2 grams of our most premium flower"
2. Upload banner image if available
"""

import requests
import json
import sys

KLAVIYO_API_KEY = "pk_2b57d9dd3402b67a041cb42568247ac52b"
TEMPLATE_ID = "SEkym7"

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json",
    "revision": "2024-10-15",
}

def get_template():
    url = f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/"
    resp = requests.get(url, headers=HEADERS)
    print(f"GET template status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Error: {resp.text}")
        return None
    return resp.json()

def update_template(html: str, text: str = None):
    url = f"https://a.klaviyo.com/api/templates/{TEMPLATE_ID}/"
    payload = {
        "data": {
            "type": "template",
            "id": TEMPLATE_ID,
            "attributes": {
                "html": html,
            }
        }
    }
    if text:
        payload["data"]["attributes"]["text"] = text
    resp = requests.patch(url, headers=HEADERS, json=payload)
    print(f"PATCH template status: {resp.status_code}")
    if resp.status_code not in (200, 204):
        print(f"Error: {resp.text[:1000]}")
        return False
    return True

def main():
    print("Fetching template...")
    data = get_template()
    if not data:
        sys.exit(1)

    attrs = data["data"]["attributes"]
    html = attrs.get("html", "")
    text = attrs.get("text", "")

    print(f"Template name: {attrs.get('name')}")
    print(f"HTML length: {len(html)}")

    # Show context around the phrase we want to change
    idx = html.lower().find("indoor cultivar")
    if idx == -1:
        print("\nPhrase 'indoor cultivars' NOT found in template HTML.")
        print("Searching for nearby phrases...")
        for phrase in ["premium", "indoor", "cultivar", "r550", "550"]:
            i = html.lower().find(phrase)
            if i != -1:
                print(f"  Found '{phrase}' at index {i}: ...{html[max(0,i-60):i+80]}...")
    else:
        print(f"\nFound 'indoor cultivar' at index {idx}:")
        print(f"  Context: ...{html[max(0,idx-80):idx+120]}...")

    # Save original for inspection
    with open("/home/user/workflows/backwoods_template_original.html", "w") as f:
        f.write(html)
    print("\nOriginal HTML saved to backwoods_template_original.html")

    # Apply copy fix
    old_phrase = "indoor cultivars"
    new_phrase = "rolled with 2 grams of our most premium flower"

    if old_phrase in html:
        updated_html = html.replace(old_phrase, new_phrase)
        print(f"\nReplaced '{old_phrase}' with '{new_phrase}'")
        count = html.count(old_phrase)
        print(f"Replacements made: {count}")
    else:
        # Try case-insensitive match
        import re
        pattern = re.compile(re.escape(old_phrase), re.IGNORECASE)
        matches = pattern.findall(html)
        if matches:
            updated_html = pattern.sub(new_phrase, html)
            print(f"\nReplaced {len(matches)} case-insensitive match(es)")
        else:
            print(f"\nPhrase not found. Saving HTML for manual inspection.")
            updated_html = None

    if updated_html and updated_html != html:
        with open("/home/user/workflows/backwoods_template_updated.html", "w") as f:
            f.write(updated_html)
        print("Updated HTML saved to backwoods_template_updated.html")
        print("\nPushing update to Klaviyo...")
        success = update_template(updated_html)
        if success:
            print("Template updated successfully!")
        else:
            print("Update failed.")
    else:
        print("No changes applied.")

if __name__ == "__main__":
    main()
