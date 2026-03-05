#!/usr/bin/env python3
"""
Create Montagu Snack Products.
"""

from shopify_api import BASE_URL, HEADERS, upload_product_image
import requests
import json
import os

PRODUCTS = [
    {
        "title": "Montagu Mango Fruit Flakes",
        "image_file": "Mango Fruit Flakes - Montagu.png"
    },
    {
        "title": "Montagu Raspberry & Beetroot Fruit Cubes",
        "image_file": "Rasberry & Betroot Fruit Cubes - Montagu.png"
    },
    {
        "title": "Montagu Mixed Tree Nuts",
        "image_file": "Mixed Tree Nuts - Montagu.png"
    }
]

PRICE = "45.00"
VENDOR = "Montagu"
PRODUCT_TYPE = "Snacks"
TAGS = "Snacks, Montagu, Munchies"

def create_product(product_data):
    title = product_data['title']
    image_file = product_data['image_file']
    
    print(f"🚀 Creating Product: {title}...")
    
    payload = {
        "product": {
            "title": title,
            "body_html": "",
            "vendor": VENDOR,
            "product_type": PRODUCT_TYPE,
            "tags": TAGS,
            "status": "active",
            "published": True,
            "variants": [
                {
                    "price": PRICE,
                    "inventory_management": "shopify",
                    "inventory_policy": "continue",
                    "requires_shipping": True,
                    "taxable": True
                }
            ]
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products.json", headers=HEADERS, json=payload)
        response.raise_for_status()
        new_product = response.json()['product']
        product_id = str(new_product['id'])
        print(f"   ✅ Created (ID: {product_id})")
        
        # Upload Image
        if os.path.exists(image_file):
            print(f"   📸 Uploading image: {image_file}...")
            if upload_product_image(product_id, image_file):
                print("      ✅ Image uploaded")
            else:
                print("      ❌ Image upload failed")
        else:
             print(f"   ⚠️ Image file not found: {image_file}")
             
    except Exception as e:
        print(f"   ❌ Error creating product: {e}")
        if hasattr(e, 'response') and e.response:
             print(f"   Response: {e.response.text}")


def main():
    print("🚀 Starting Montagu Product Creation...")
    print("=" * 60)
    
    for p in PRODUCTS:
        create_product(p)
        print("-" * 40)

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
