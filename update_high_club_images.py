#!/usr/bin/env python3
"""
Update Images for 2 "The High Club" Vapes on Shopify.
Created on Feb 05, 2026.
"""

from shopify_api import upload_product_image, delete_all_product_images, get_product
import os
import time

# Product Image Configuration
# Using exact filenames from directory listing
PRODUCTS = {
    "9062481985748": { # Skittlez / Lemon Berry Fire
        "title": "The High Club: Skittlez / Lemon Berry Fire",
        "images": [
            "high club lemon skittelz .jpg",
            "high cclub lemon skittelz front.jpg",
            "high club lemon skittelz side .jpg"
        ]
    },
    "9062480642260": { # Permanent Marker / Sun of Peach
        "title": "The High Club: Permanent Marker / Sun of Peach",
        "images": [
            "high club permenant marker.jpg",
            "high club permenant marker front.jpg",
            "high club permemnant marker side.jpg"
        ]
    }
}

BASE_PATH = "/Users/norton/Desktop/Cannibisters Agent"

def main():
    print("🚀 Updating High Club Vape Images (Feb 05)...")
    print("=" * 60)

    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing Images for {data['title']} (ID: {pid})...")
        
        # 1. Delete existing images
        print("   🗑️  Cleaning up old images...")
        if delete_all_product_images(pid):
            print("   ✅ Old images deleted")
        else:
            print("   ⚠️  Failed to delete old images (or none existed)")
            
        # 2. Upload new images
        print("   📸 Uploading new images...")
        success_count = 0
        for img_name in data['images']:
            full_path = os.path.join(BASE_PATH, img_name)
            if not os.path.exists(full_path):
                print(f"      ❌ File not found: {img_name}")
                continue
                
            if upload_product_image(pid, full_path):
                print(f"      ✅ Uploaded {img_name}")
                success_count += 1
                # Small delay to ensure order or just polite API usage
                time.sleep(1) 
            else:
                print(f"      ❌ Failed to upload {img_name}")
        
        print(f"   ✅ {success_count}/{len(data['images'])} images uploaded")

    print("\n" + "=" * 60)
    print("🎉 All image updates finished!")

if __name__ == "__main__":
    main()
