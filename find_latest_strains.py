#!/usr/bin/env python3
"""
Find the 5 most recently created products to identify new strains.
"""

from shopify_api import BASE_URL, HEADERS
import requests
import json
from datetime import datetime

def get_latest_products():
    print("🔍 Fetching latest products...")
    
    # We can't easily sort by created_at desc in one call without iterating?
    # Actually, default order is by title.
    # We can fetch a list and sort manually, or use 'created_at_min' if we knew the time.
    # Let's fetch the last created products by using no params (fetch 250) or just fetch all and sort.
    # Actually, products endpoint doesn't support generic 'sort_by' created_at via REST easily without specific params?
    # Filter for products created today (Jan 22, 2026)
    url = f"{BASE_URL}/products.json?limit=50&created_at_min=2026-01-22T00:00:00"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        products = response.json().get('products', [])
        
        print(f"✅ Found {len(products)} products created today:")
        print("-" * 60)
        for p in products:
            created_at = p.get('created_at', 'Unknown')
            status = p.get('status', 'unknown')
            print(f"ID: {p['id']} | Status: {status} | Created: {created_at}")
            print(f"Title: {p['title']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error fetching products: {e}")

if __name__ == "__main__":
    get_latest_products()
