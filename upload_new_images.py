#!/usr/bin/env python3
"""
Upload new product images to Shopify
"""

import os

from shopify_api import upload_product_image, search_products as api_search_products

# List of image files to process
image_files = [
    "Black patronus .png",
    "Bluricorn.png",
    "Chocolope .png",
    "Frosted pearls.png",
    "Gelato Jeleousy .png",
    "Orange sherbet.png",
    "Peach Jam.png",
    "Superberry crush.png"
]

base_dir = "/Users/norton/Desktop/Cannibisters Agent"

def get_product_id_by_name(name):
    """Search for a product by name and return its ID"""
    products = api_search_products(name)
    if products:
        # Sort by similarity or exact match if possible, but for now take the first one
        # Ideally we'd filter for exact matches
        for p in products:
            if p['title'].lower() == name.lower():
                return p['id']
            # Handle "Peachy Jam" vs "Peach Jam"
            if name.lower() == "peach jam" and p['title'].lower() == "peachy jam":
                return p['id']
            
        return products[0]['id']
    return None

print("🚀 Starting image upload process...")
print("="*80)

for image_file in image_files:
    image_path = os.path.join(base_dir, image_file)
    
    # Clean up filename to get product name
    # Remove extension
    name = os.path.splitext(image_file)[0]
    # Remove trailing spaces
    name = name.strip()
    
    print(f"\n📸 Processing image: {image_file}")
    print(f"   Searching for product: '{name}'")
    
    product_id = get_product_id_by_name(name)
    
    if product_id:
        print(f"   ✅ Found product ID: {product_id}")
        if upload_product_image(str(product_id), image_path):
             print(f"   ✅ Uploaded {image_file}")
        else:
             print(f"   ❌ Failed to upload {image_file}")
    else:
        print(f"   ❌ Product not found for '{name}'")
        # Try fuzzy match manually for specific cases if needed
        if name.lower() == "peach jam":
             print("   Trying 'Peachy Jam'...")
             product_id = get_product_id_by_name("Peachy Jam")
             if product_id:
                 print(f"   ✅ Found product ID: {product_id}")
                 upload_product_image(str(product_id), image_path)

print("\n" + "="*80)
print("🏁 Image upload process finished!")
