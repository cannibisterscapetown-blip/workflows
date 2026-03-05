#!/usr/bin/env python3
"""
Update Montagu Snacks: Add Descriptions & Add to Collection.
"""

from shopify_api import BASE_URL, HEADERS, update_product_description
import requests
import json

COLLECTION_ID = "413369499860" # Coffee-Beverages-Snacks

PRODUCTS = {
    "9045387477204": {
        "title": "Montagu Mango Fruit Flakes",
        "description": "Deliciously sweet and chewy mango fruit flakes, made from real fruit. A perfect healthy snack for on-the-go energy."
    },
    "9045387542740": {
        "title": "Montagu Raspberry & Beetroot Fruit Cubes",
        "description": "A unique blend of tangy raspberry and earthy beetroot in convenient, bite-sized cubes. Packed with flavor and natural goodness."
    },
    "9045387575508": {
        "title": "Montagu Mixed Tree Nuts",
        "description": "A premium selection of crunchy tree nuts. High in protein and healthy fats, making for a satisfying and nutritious snack."
    }
}

def add_to_collection(product_id):
    print(f"   📂 Adding to collection {COLLECTION_ID}...")
    
    # Check if already in collection? 
    # The API might just error or return existing. Better to just try add.
    
    payload = {
        "collect": {
            "product_id": product_id,
            "collection_id": COLLECTION_ID
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/collects.json", headers=HEADERS, json=payload)
        # 422 Unprocessable Entity means already exists usually
        if response.status_code == 201:
            print("      ✅ Added to collection")
        elif response.status_code == 422:
             print("      ⚠️  Already in collection (or other error)")
        else:
             print(f"      ❌ Failed to add: {response.status_code} {response.text}")
             
    except Exception as e:
        print(f"      ❌ Error: {e}")

def main():
    print("🚀 Updating Montagu Snacks...")
    print("=" * 60)
    
    for pid, data in PRODUCTS.items():
        print(f"📦 Processing {data['title']} (ID: {pid})...")
        
        # 1. Update Description
        print("   📝 Updating description...")
        if update_product_description(pid, data['description']):
            print("      ✅ Description updated")
        else:
            print("      ❌ Description update failed")
            
        # 2. Add to Collection
        add_to_collection(pid)
        print("-" * 40)

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
