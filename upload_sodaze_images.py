#!/usr/bin/env python3
"""
Upload Sodaze Product Images
Created on Feb 09, 2026.
"""

from shopify_api import upload_product_image
import os

# Product ID to Image File mapping
PRODUCT_IMAGES = {
    "9068414009556": "Blueberry lemonade sodaze.webp",  # Blueberry Lemonade
    "9068414107860": "Cherry pop sodaze.webp",          # Lemon Meringue (using Cherry pop)
    "9068414173396": "Orange creamaxz.jpg"              # Orange Creme
}

def main():
    print("🚀 Uploading Sodaze Product Images...")
    print("=" * 60)
    
    success_count = 0
    for product_id, image_file in PRODUCT_IMAGES.items():
        print(f"\n📦 Product ID: {product_id}")
        print(f"   Image: {image_file}")
        
        if not os.path.exists(image_file):
            print(f"   ❌ Image file not found: {image_file}")
            continue
            
        print(f"   📸 Uploading...")
        if upload_product_image(product_id, image_file):
            print("   ✅ Image uploaded successfully")
            success_count += 1
        else:
            print("   ❌ Image upload failed")
        
        print("-" * 40)

    print("\n" + "=" * 60)
    print(f"🎉 Finished! Uploaded {success_count}/{len(PRODUCT_IMAGES)} images.")

if __name__ == "__main__":
    main()
