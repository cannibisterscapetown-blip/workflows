#!/usr/bin/env python3
"""
Create Sodaze Soda Products.
Created on Feb 09, 2026.
"""

from shopify_api import BASE_URL, HEADERS
import requests
import json

PRODUCTS = [
    {
        "title": "Sodaze Blueberry Lemonade Soda",
        "description": "Refreshing Blueberry Lemonade infused soda. <br><br><strong>30mg THC</strong><br><br>• 250ml<br>• Made with real fruit<br>• Preservative free<br>• No artificial colourants<br><br>A delicious and refreshing way to enjoy cannabis.",
        "tags": "Edibles, Sodaze, Soda, Blueberry, Lemonade, 30mg, Drinks"
    },
    {
        "title": "Sodaze Lemon Meringue Soda",
        "description": "Sweet and tangy Lemon Meringue infused soda. <br><br><strong>30mg THC</strong><br><br>• 250ml<br>• Made with real fruit<br>• Preservative free<br>• No artificial colourants<br><br>A delicious and refreshing way to enjoy cannabis.",
        "tags": "Edibles, Sodaze, Soda, Lemon, Meringue, 30mg, Drinks"
    },
    {
        "title": "Sodaze Orange Creme Soda",
        "description": "Creamy Orange infused soda. <br><br><strong>30mg THC</strong><br><br>• 250ml<br>• Made with real fruit<br>• Preservative free<br>• No artificial colourants<br><br>A delicious and refreshing way to enjoy cannabis.",
        "tags": "Edibles, Sodaze, Soda, Orange, Creme, 30mg, Drinks"
    }
]

VENDOR = "Sodaze"
PRODUCT_TYPE = "Edibles"
PRICE = "0.00"  # User can set price later

def create_product(product_data):
    title = product_data['title']
    description = product_data['description']
    tags = product_data['tags']
    
    print(f"🚀 Creating Product: {title}...")
    
    payload = {
        "product": {
            "title": title,
            "body_html": description,
            "vendor": VENDOR,
            "product_type": PRODUCT_TYPE,
            "tags": tags,
            "status": "draft",  # Create as draft
            "published": False,
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
        print(f"   ✅ Created as DRAFT (ID: {product_id})")
        return product_id
        
    except Exception as e:
        print(f"   ❌ Error creating product: {e}")
        if hasattr(e, 'response') and e.response:
             print(f"   Response: {e.response.text}")
        return None


def main():
    print("🚀 Starting Sodaze Product Creation...")
    print("=" * 60)
    
    created_ids = []
    for p in PRODUCTS:
        product_id = create_product(p)
        if product_id:
            created_ids.append(product_id)
        print("-" * 40)

    print("\n" + "=" * 60)
    print(f"🎉 Finished! Created {len(created_ids)} products as DRAFTS.")
    print(f"Product IDs: {', '.join(created_ids)}")

if __name__ == "__main__":
    main()
