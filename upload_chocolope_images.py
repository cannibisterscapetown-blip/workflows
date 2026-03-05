#!/usr/bin/env python3
"""
Upload Chocolope Product Images
Created on Feb 09, 2026.
"""

from shopify_api import upload_product_image, get_product
import os

PRODUCT_ID = "9029351997652"  # Chocolope - Cannibisters Limited Collection
IMAGE_FILES = [
    "Chocolope .png",
    "CHOCOLOPE.jpg"
]

def main():
    print("🚀 Uploading Chocolope Product Images...")
    print("=" * 60)
    
    # Verify product exists
    print(f"📦 Checking product ID: {PRODUCT_ID}...")
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"   ❌ Product not found!")
        return
    
    print(f"   ✅ Found: {product['title']}")
    
    success_count = 0
    for image_file in IMAGE_FILES:
        print(f"\n   📸 Image: {image_file}")
        
        if not os.path.exists(image_file):
            print(f"      ❌ Image file not found")
            continue
            
        print(f"      Uploading...")
        if upload_product_image(PRODUCT_ID, image_file):
            print(f"      ✅ Uploaded successfully")
            success_count += 1
        else:
            print(f"      ❌ Upload failed")

    print("\n" + "=" * 60)
    print(f"🎉 Finished! Uploaded {success_count}/{len(IMAGE_FILES)} images.")

if __name__ == "__main__":
    main()
