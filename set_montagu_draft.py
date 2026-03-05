#!/usr/bin/env python3
"""
Set Montagu Snacks to Draft.
"""

from shopify_api import BASE_URL, HEADERS
import requests
import json

PRODUCTS = [
    "9045387477204", # Mango Fruit Flakes
    "9045387542740", # Raspberry & Beetroot
    "9045387575508"  # Mixed Tree Nuts
]

def set_to_draft(product_id):
    print(f"📦 Setting product {product_id} to DRAFT...")
    
    payload = {
        "product": {
            "id": product_id,
            "status": "draft"
        }
    }
    
    try:
        response = requests.put(f"{BASE_URL}/products/{product_id}.json", headers=HEADERS, json=payload)
        response.raise_for_status()
        print(f"      ✅ Status updated to DRAFT")
             
    except Exception as e:
        print(f"      ❌ Error: {e}")
        if hasattr(e, 'response') and e.response:
             print(f"      Response: {e.response.text}")

def main():
    print("🚀 Updating Montagu Snacks Status...")
    print("=" * 60)
    
    for pid in PRODUCTS:
        set_to_draft(pid)

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
