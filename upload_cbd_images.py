#!/usr/bin/env python3
"""
Upload images for Cannibisters Full Spectrum CBD Cream.
"""

from shopify_api import upload_product_image
import os
import sys

# CBD Cream ID: 9039396798676
PRODUCT_ID = "9039396798676"
IMAGES = ["cbd_cream_1.jpg", "cbd_cream_2.jpg"]

def main():
    print(f"🚀 Uploading images to CBD Cream (ID: {PRODUCT_ID})...")
    print("=" * 60)

    for img in IMAGES:
        if not os.path.exists(img):
            print(f"❌ Image not found: {img}")
            continue
            
        print(f"📸 Uploading {img}...")
        if upload_product_image(PRODUCT_ID, img):
             print(f"   ✅ Success")
        else:
             print(f"   ❌ Failed")

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
