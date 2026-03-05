#!/usr/bin/env python3
"""
Verify image counts for the updated products on Shopify
"""

from shopify_api import get_product

# Product IDs that were updated
product_ids = [
    "9016555864276", # Sticky Rice
    "9016556454100", # Lit Pineapple
    "9016555995348", # Highlighter
    "7611810676948", # Blue Dream
    "9019110293716", # Black Cat
    "7958185410772"  # Watermelon Punch
]

print("🔍 Verifying image updates...")
print("-" * 40)

for pid in product_ids:
    product = get_product(pid)
    if product:
        title = product['title']
        image_count = len(product.get('images', []))
        print(f"Product: {title:<20} | Images: {image_count}")
        if image_count == 1:
            print(f"   ✅ Correct")
        else:
            print(f"   ❌ Expected 1 image, found {image_count}")
    else:
        print(f"❌ Failed to fetch product info for ID: {pid}")

print("-" * 40)
