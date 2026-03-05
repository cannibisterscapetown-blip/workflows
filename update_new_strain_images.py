#!/usr/bin/env python3
"""
Update images for new strains from 'new_strain_pics' folder
"""

import os
import sys
from shopify_api import delete_all_product_images, upload_product_image

# Mapping of Strain names to Product IDs and their corresponding unzipped image filenames
products_to_update = [
    {
        "name": "Sticky Rice",
        "id": "9016555864276",
        "image": "new_strain_pics/Sticky rice .jpg"
    },
    {
        "name": "Lit Pineapple",
        "id": "9016556454100",
        "image": "new_strain_pics/Lit pinapple.jpg"
    },
    {
        "name": "Highlighter",
        "id": "9016555995348",
        "image": "new_strain_pics/High lighter.jpg"
    },
    {
        "name": "Blue Dream",
        "id": "7611810676948",
        "image": "new_strain_pics/Blue dream.jpg"
    },
    {
        "name": "Black Cat",
        "id": "9019110293716",
        "image": "new_strain_pics/Black cat.jpg"
    },
    {
        "name": "Watermelon Punch",
        "id": "7958185410772",
        "image": "new_strain_pics/watermelon punch .jpg"
    }
]

def main():
    base_dir = "/Users/norton/Desktop/Cannibisters Agent"
    
    print("🚀 Starting image update for new strains...")
    print("=" * 80)
    
    success_count = 0
    fail_count = 0
    
    for item in products_to_update:
        name = item["name"]
        product_id = item["id"]
        image_rel_path = item["image"]
        image_path = os.path.join(base_dir, image_rel_path)
        
        print(f"\n📦 Processing {name} (ID: {product_id})")
        
        if not os.path.exists(image_path):
            print(f"   ❌ Image file not found: {image_rel_path}")
            fail_count += 1
            continue
            
        print(f"   📸 Found image: {image_rel_path}")
        
        # 1. Delete old images
        print(f"   🗑️ Clearing existing images...")
        if delete_all_product_images(product_id):
            # 2. Upload new image
            print(f"   📤 Uploading new image...")
            if upload_product_image(product_id, image_path):
                print(f"   ✨ Successfully updated image for {name}")
                success_count += 1
            else:
                print(f"   ❌ Failed to upload new image for {name}")
                fail_count += 1
        else:
            print(f"   ❌ Failed to delete old images for {name}")
            fail_count += 1
            
    print("\n" + "=" * 80)
    print(f"🏁 Update process finished!")
    print(f"✅ Successes: {success_count}")
    print(f"❌ Failures: {fail_count}")
    
    if fail_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
