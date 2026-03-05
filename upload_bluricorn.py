#!/usr/bin/env python3
"""
Clean up old images and upload Bluricorn image
"""

import os
from shopify_api import delete_all_product_images, upload_product_image, get_product

product_id = "7973895733460"
image_file = "Bluricorn.png"
base_dir = "/Users/norton/Desktop/Cannibisters Agent"
image_path = os.path.join(base_dir, image_file)

print("🚀 Starting Bluricorn image upload...")
print("="*80)

# Verify product first
product = get_product(product_id)
if product:
    print(f"📦 Found product: {product['title']} (ID: {product_id})")
    
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
    print(f"❌ Product {product_id} not found!")

print("\n" + "="*80)
print("🏁 Bluricorn upload finished!")
