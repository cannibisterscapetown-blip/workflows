#!/usr/bin/env python3
"""
Upload Chocolate Product Images
Created on Feb 09, 2026.
"""

from shopify_api import upload_product_image, get_product, search_products
import os

IMAGE_FILES = [
    "Chocolope .png",
    "CHOCOLOPE.jpg"
]

def main():
    print("🚀 Finding and Uploading Chocolate Product Images...")
    print("=" * 60)
    
    # Search for Chocolate product
    print("🔍 Searching for 'Chocolate' product...")
    products = search_products("Chocolate", status='any')
    
    if not products:
        print("❌ No products found with 'Chocolate' in title")
        return
    
    # Show all matches
    print(f"\nFound {len(products)} matches:")
    for i, p in enumerate(products):
        print(f"{i+1}. {p['title']} (ID: {p['id']}, Status: {p['status']})")
    
    # Use the first match (or let user specify)
    product = products[0]
    product_id = str(product['id'])
    
    print(f"\n📦 Using: {product['title']} (ID: {product_id})")
    
    success_count = 0
    for image_file in IMAGE_FILES:
        print(f"\n   📸 Image: {image_file}")
        
        if not os.path.exists(image_file):
            print(f"      ❌ Image file not found")
            continue
            
        print(f"      Uploading...")
        if upload_product_image(product_id, image_file):
            print(f"      ✅ Uploaded successfully")
            success_count += 1
        else:
            print(f"      ❌ Upload failed")

    print("\n" + "=" * 60)
    print(f"🎉 Finished! Uploaded {success_count}/{len(IMAGE_FILES)} images.")

if __name__ == "__main__":
    main()
