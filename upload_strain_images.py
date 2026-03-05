#!/usr/bin/env python3
"""
Upload images for Violet Cake, Blood Bath, and Chocolope.
"""

from shopify_api import upload_product_image
import os
import sys

# Mapping: Product ID -> Image Filename
# Violet Cake: 8403086835924
# Blood Bath: 8403070910676
# Chocolope: 8876246728916 (Draft strain)

UPLOADS = {
    "8403086835924": "violet cake.png",
    "8403070910676": "blood bath.png",
    "8876246728916": "CHOCOLOPE.jpg"
}

def main():
    print("🚀 Uploading Strain Images...")
    print("=" * 60)

    for pid, filename in UPLOADS.items():
        if not os.path.exists(filename):
            print(f"❌ Image not found: {filename}")
            continue

        print(f"\n📸 Uploading {filename} to Product {pid}...")
        
        if upload_product_image(pid, filename):
             print(f"   ✅ Image uploaded successfully")
        else:
             print(f"   ❌ Failed to upload image")

    print("\n" + "=" * 60)
    print("🎉 All image uploads finished!")

if __name__ == "__main__":
    main()
