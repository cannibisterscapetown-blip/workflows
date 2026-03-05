#!/usr/bin/env python3
"""
Update images for Ready Whip and Grapefruit from '4 dec buds' folder
"""

import os
from shopify_api import delete_all_product_images, upload_product_image

# Product IDs identified earlier
products = {
    "Ready Whip": {
        "id": "9004336185556",
        "image": "4 dec buds/Ready whip.jpeg"
    },
    "Grapefruit": {
        "id": "8782047051988",
        "image": "4 dec buds/Grape Fruit.jpeg"
    }
}

base_dir = "/Users/norton/Desktop/Cannibisters Agent"

print("🚀 Starting image update for Ready Whip and Grapefruit...")
print("="*80)

for name, data in products.items():
    product_id = data["id"]
    image_rel_path = data["image"]
    image_path = os.path.join(base_dir, image_rel_path)
    
    print(f"\n📦 Processing {name} (ID: {product_id})")
    
    if os.path.exists(image_path):
        print(f"   📸 Found image: {image_rel_path}")
        
        # 1. Delete old images
        if delete_all_product_images(product_id):
            # 2. Upload new image
            if upload_product_image(product_id, image_path):
                print(f"   ✨ Successfully refreshed image for {name}")
            else:
                print(f"   ❌ Failed to upload new image for {name}")
        else:
            print(f"   ❌ Failed to delete old images for {name}")
    else:
        print(f"   ❌ Image file not found: {image_rel_path}")

print("\n" + "="*80)
print("🏁 Update process finished!")
