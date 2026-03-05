#!/usr/bin/env python3
"""
Create New Sodaze Products - Berry Haze & Cherry Pop
Created on Mar 02, 2026.
"""

from shopify_api import BASE_URL, HEADERS, create_or_update_metafield, upload_product_image
import requests
import os
import time

PRODUCTS = [
    {
        "title": "Sodaze Berry Haze Soda",
        "description": (
            "A vibrant and refreshing Berry Haze infused soda bursting with wild berry flavour. "
            "<br><br><strong>30mg THC</strong><br><br>"
            "• 250ml<br>"
            "• Made with real fruit<br>"
            "• Preservative free<br>"
            "• No artificial colourants<br><br>"
            "A delicious and refreshing way to enjoy cannabis."
        ),
        "tags": "Edibles, Sodaze, Soda, Berry, Haze, 30mg, Drinks",
        "image_file": None,  # No image available yet — can be added later
        "metafields": {
            "thc_content": "30mg",
            "volume": "250ml",
            "ingredients": "Real fruit, Natural flavours, Cannabis extract",
            "product_type": "Infused Beverage",
            "flavours": "Berry, Mixed Berry, Sweet, Fruity",
            "effects": "Relaxed • Happy • Euphoric",
            "used_for": "Relaxation, social enjoyment, stress relief",
            "preservative_free": "Yes",
            "artificial_colourants": "No"
        }
    },
    {
        "title": "Sodaze Cherry Pop Soda",
        "description": (
            "A bold and bubbly Cherry Pop infused soda with a sweet cherry burst in every sip. "
            "<br><br><strong>30mg THC</strong><br><br>"
            "• 250ml<br>"
            "• Made with real fruit<br>"
            "• Preservative free<br>"
            "• No artificial colourants<br><br>"
            "A delicious and refreshing way to enjoy cannabis."
        ),
        "tags": "Edibles, Sodaze, Soda, Cherry, 30mg, Drinks",
        "image_file": "Cherry pop sodaze.webp",
        "metafields": {
            "thc_content": "30mg",
            "volume": "250ml",
            "ingredients": "Real fruit, Natural flavours, Cannabis extract",
            "product_type": "Infused Beverage",
            "flavours": "Cherry, Sweet, Fruity",
            "effects": "Relaxed • Happy • Euphoric",
            "used_for": "Relaxation, social enjoyment, stress relief",
            "preservative_free": "Yes",
            "artificial_colourants": "No"
        }
    }
]

VENDOR = "Sodaze"
PRODUCT_TYPE = "Edibles"
PRICE = "0.00"  # Price to be set in Admin


def create_product(product_data):
    title = product_data["title"]
    print(f"\n🚀 Creating: {title}...")

    payload = {
        "product": {
            "title": title,
            "body_html": product_data["description"],
            "vendor": VENDOR,
            "product_type": PRODUCT_TYPE,
            "tags": product_data["tags"],
            "status": "draft",
            "published": False,
            "variants": [
                {
                    "price": PRICE,
                    "inventory_management": "shopify",
                    "inventory_policy": "continue",
                    "requires_shipping": True,
                    "taxable": True
                }
            ]
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/products.json", headers=HEADERS, json=payload)
        response.raise_for_status()
        new_product = response.json()["product"]
        product_id = str(new_product["id"])
        print(f"   ✅ Created as DRAFT — ID: {product_id}")
        return product_id
    except Exception as e:
        print(f"   ❌ Error creating product: {e}")
        if hasattr(e, "response") and e.response:
            print(f"   Response: {e.response.text}")
        return None


def add_metafields(product_id, metafields):
    print(f"   📋 Adding metafields...")
    success = 0
    for key, value in metafields.items():
        if create_or_update_metafield(product_id, "my_fields", key, value):
            success += 1
            print(f"      ✅ {key}")
        else:
            print(f"      ❌ {key}")
    print(f"   ✅ {success}/{len(metafields)} metafields set")


def upload_image(product_id, image_file):
    if not image_file:
        print("   ℹ️  No image file specified — skipping image upload")
        return
    if not os.path.exists(image_file):
        print(f"   ⚠️  Image not found: {image_file} — skipping upload")
        return
    print(f"   📸 Uploading image: {image_file}...")
    if upload_product_image(product_id, image_file):
        print("   ✅ Image uploaded successfully")
    else:
        print("   ❌ Image upload failed")


def main():
    print("🚀 Creating New Sodaze Products — Berry Haze & Cherry Pop")
    print("=" * 60)

    created = []
    for product in PRODUCTS:
        product_id = create_product(product)
        if product_id:
            time.sleep(0.5)
            add_metafields(product_id, product["metafields"])
            time.sleep(0.5)
            upload_image(product_id, product.get("image_file"))
            created.append((product["title"], product_id))
        print("-" * 40)

    print("\n" + "=" * 60)
    print(f"🎉 Done! Created {len(created)} products as DRAFTS:")
    for title, pid in created:
        print(f"   • {title} — ID: {pid}")
    print("\nNext steps:")
    print("  1. Set prices in Shopify Admin")
    print("  2. Add product images if missing")
    print("  3. Publish when ready")


if __name__ == "__main__":
    main()
