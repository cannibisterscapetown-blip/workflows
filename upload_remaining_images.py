#!/usr/bin/env python3
"""
Upload remaining product images to Shopify
"""

import os
from shopify_api import upload_product_image

# Map image filenames to correct product IDs based on list_products output
# Found "Orange Sherbert" (9008378970324) vs "Orange sherbet.png"
# Need to find IDs for:
# - Bluricorn
# - Frosted pearls
# - Gelato Jeleousy

product_map = {
    # Exact text matches from list_products (or fuzzy matches)
    "Orange sherbet.png": "9008378970324", # "Orange Sherbert"
}

# Image files we still need to process
remaining_images = [
    "Bluricorn.png",
    "Frosted pearls.png",
    "Gelato Jeleousy .png",
]

base_dir = "/Users/norton/Desktop/Cannibisters Agent"

print("🚀 Starting upload for remaining images...")
print("="*80)

# Process the known match first
for image_file, product_id in product_map.items():
    image_path = os.path.join(base_dir, image_file)
    print(f"\n📸 Processing image: {image_file}")
    if upload_product_image(product_id, image_path):
        print(f"   ✅ Uploaded {image_file} to product {product_id}")
    else:
        print(f"   ❌ Failed to upload {image_file}")

# Try to find the others - maybe they are drafts?
print("\n🔍 Searching for remaining products (including drafts)...")
from shopify_api import list_products

# Get ALL products including drafts
all_products = list_products(limit=250, status='any')
print(f"   Fetched {len(all_products)} products total")

for image_file in remaining_images:
    name = os.path.splitext(image_file)[0].strip().lower()
    print(f"\n📸 Searching for: '{name}'")
    
    found = False
    for p in all_products:
        p_title = p['title'].lower()
        if name in p_title or p_title in name:
            print(f"   ✅ Found match: '{p['title']}' (ID: {p['id']})")
            image_path = os.path.join(base_dir, image_file)
            if upload_product_image(str(p['id']), image_path):
                print(f"   ✅ Uploaded {image_file}")
            found = True
            break
    
    if not found:
        print(f"   ❌ No match found for '{name}'")

print("\n" + "="*80)
print("🏁 Remaining uploads process finished!")
