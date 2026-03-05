#!/usr/bin/env python3
"""
Clean up old images and re-upload new ones for remaining manually matched products
"""

import os
from shopify_api import delete_all_product_images, upload_product_image

# Map image files to product IDs based on user input and lookup
# 8598292037844: Gelato Jealousy -> Matches "Gelato Jeleousy .png"
# 8899422945492: Frosted Peaks -> Matches "Frosted pearls.png"
# "Bluricorn.png" is still unmatched

image_map = {
    "Gelato Jeleousy .png": "8598292037844",
    "Frosted pearls.png": "8899422945492",
}

base_dir = "/Users/norton/Desktop/Cannibisters Agent"

print("🚀 Starting image cleanup and upload for manually matched products...")
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
print("🏁 Finished processing provided IDs!")
