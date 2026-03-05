#!/usr/bin/env python3
"""
Upload Blue Caviar Product Image
Created on Feb 09, 2026.
"""

from shopify_api import upload_product_image, get_product
import os

# From previous output, Blue Caviar ID is 9049869353172
PRODUCT_ID = "9049869353172"
IMAGE_FILE = "Blue Caviar - Cannibister_Discover_with_Leigh_Photography-2.jpg"

def main():
    print("🚀 Uploading Blue Caviar Product Image...")
    print("=" * 60)
    
    # Verify product exists
    print(f"📦 Checking product ID: {PRODUCT_ID}...")
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"   ❌ Product not found!")
        return
    
    print(f"   ✅ Found: {product['title']}")
    
    # Check if image exists
    if not os.path.exists(IMAGE_FILE):
        print(f"   ❌ Image file not found: {IMAGE_FILE}")
        return
    
    print(f"   📸 Uploading image: {IMAGE_FILE}...")
    if upload_product_image(PRODUCT_ID, IMAGE_FILE):
        print("   ✅ Image uploaded successfully!")
    else:
        print("   ❌ Image upload failed")

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
