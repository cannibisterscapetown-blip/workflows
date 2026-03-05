#!/usr/bin/env python3
"""
Clean up old images and re-upload new ones for updated products
"""

import os
from shopify_api import delete_all_product_images, upload_product_image

# Map image files to product IDs
image_map = {
    # Confirmed matches
    "Black patronus .png": "9008376185044",      # Black Patronus
    "Chocolope .png": "8876246728916",           # Chocolope
    "Peach Jam.png": "9008376774868",            # Peachy Jam
    "Superberry crush.png": "8733300719828",     # Superberry crush
    "Orange sherbet.png": "9008378970324",       # Orange Sherbet
}

base_dir = "/Users/norton/Desktop/Cannibisters Agent"

print("🚀 Starting image cleanup and re-upload...")
print("="*80)

for image_file, product_id in image_map.items():
    image_path = os.path.join(base_dir, image_file)
    print(f"\n📦 Processing product: {product_id} ({image_file})")
    
    # 1. Delete old images
    if delete_all_product_images(product_id):
        # 2. Upload new image
        if upload_product_image(product_id, image_path):
            print(f"   ✨ Successfully refreshed image for product {product_id}")
        else:
            print(f"   ❌ Failed to upload new image for product {product_id}")
    else:
        print(f"   ❌ Failed to delete old images for product {product_id}")

print("\n" + "="*80)
print("🏁 Cleanup and re-upload finished!")
