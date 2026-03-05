#!/usr/bin/env python3
"""
Upload image for Apple & Banana Gelato.
"""

from shopify_api import upload_product_image
import os
import sys

# Apple & Banana Gelato ID: 7889558110420
PRODUCT_ID = "7889558110420"
IMAGE = "apple_banana_gelato.png"

def main():
    print(f"🚀 Uploading image to Apple & Banana Gelato (ID: {PRODUCT_ID})...")
    print("=" * 60)

    if not os.path.exists(IMAGE):
        print(f"❌ Image not found: {IMAGE}")
        sys.exit(1)
            
    print(f"📸 Uploading {IMAGE}...")
    if upload_product_image(PRODUCT_ID, IMAGE):
            print(f"   ✅ Success")
    else:
            print(f"   ❌ Failed")

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
