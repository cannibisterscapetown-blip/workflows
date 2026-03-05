#!/usr/bin/env python3
"""
Upload image to new joint products.
"""

from shopify_api import upload_product_image
import os
import sys

# Product IDs
PRODUCTS = {
    "9039335981268": "Canni Papa Smurf Joint",
    "9039335817428": "Canni Chocolope Joint",
    "9039335522516": "Canni Astro Grape Joint",
    "9039335129300": "Canni Ltd Joint"
}

IMAGE_PATH = "cannibisters_joint_tube.jpg"

def main():
    print("🚀 Uploading images to new joints...")
    print("=" * 60)

    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Image not found: {IMAGE_PATH}")
        sys.exit(1)

    for pid, title in PRODUCTS.items():
        print(f"\n📸 Processing {title} (ID: {pid})...")
        
        if upload_product_image(pid, IMAGE_PATH):
             print(f"   ✅ Image uploaded successfully")
        else:
             print(f"   ❌ Failed to upload image")

    print("\n" + "=" * 60)
    print("🎉 All image uploads finished!")

if __name__ == "__main__":
    main()
