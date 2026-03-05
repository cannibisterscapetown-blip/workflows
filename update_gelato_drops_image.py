#!/usr/bin/env python3
"""
Update Gelato Drops image
"""

import os
from shopify_api import delete_all_product_images, upload_product_image

product_id = "9008376086740"
# This is the path provided in the context
image_path = "/Users/norton/.gemini/antigravity/brain/cd734594-ef45-4702-bdad-4a230f68967c/uploaded_image_1765526719511.png"

print(f"🚀 Updating image for Gelato Drops (ID: {product_id})...")
print("="*80)

if os.path.exists(image_path):
    print(f"📸 Image found at: {image_path}")
    
    # 1. Delete old images
    if delete_all_product_images(product_id):
        # 2. Upload new image
        if upload_product_image(product_id, image_path):
            print(f"   ✨ Successfully refreshed image for product {product_id}")
        else:
            print(f"   ❌ Failed to upload new image for product {product_id}")
    else:
        print(f"   ❌ Failed to delete old images for product {product_id}")
else:
    print(f"❌ Image file not found at: {image_path}")

print("\n" + "="*80)
print("🏁 Update process finished!")
