#!/usr/bin/env python3
import shopify_api
from datetime import datetime

def find_latest_product():
    print("🔍 Fetching latest products...")
    # Get active and draft to be safe
    products = shopify_api.list_products(limit=10, status='active')
    drafts = shopify_api.list_products(limit=10, status='draft')
    
    all_products = products + drafts
    
    # Sort by created_at descending
    all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    print(f"\nFound {len(all_products)} recent products. Top 5:")
    for p in all_products[:5]:
        print(f"ID: {p['id']}")
        print(f"Title: {p['title']}")
        print(f"Status: {p['status']}")
        print(f"Created: {p['created_at']}")
        print(f"Tags: {p.get('tags')}")
        print("-" * 30)

if __name__ == "__main__":
    find_latest_product()
