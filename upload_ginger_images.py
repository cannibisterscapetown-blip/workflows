#!/usr/bin/env python3
"""
Upload images for Ginger Shot - INFUSED 24mg.
"""

from shopify_api import upload_product_image
import os
import sys

# Ginger Shot - INFUSED 24mg ID: 9036277481684
PRODUCT_ID = "9036277481684"
IMAGES = ["ginger_shot_1.jpg", "ginger_shot_2.jpg"]

def main():
    print(f"🚀 Uploading images to Ginger Shot (ID: {PRODUCT_ID})...")
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
