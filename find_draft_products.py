#!/usr/bin/env python3
"""
List all DRAFT products to find Apex and Mango Tango.
"""

from shopify_api import BASE_URL, HEADERS
import requests
import json

def get_draft_products():
    print("🔍 Fetching DRAFT products...")
    
    # Filter by status=draft
    url = f"{BASE_URL}/products.json?status=draft&limit=250"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        products = response.json().get('products', [])
        
        print(f"✅ Found {len(products)} draft products:")
        print("-" * 60)
        for p in products:
            print(f"ID: {p['id']} | Title: {p['title']}")
            
    except Exception as e:
        print(f"❌ Error fetching products: {e}")

if __name__ == "__main__":
    get_draft_products()
