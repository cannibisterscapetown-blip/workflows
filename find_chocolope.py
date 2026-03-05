#!/usr/bin/env python3
import shopify_api

def find_chocolope():
    print("🔍 Searching for 'Chocolope'...")
    # Search all statuses
    products = shopify_api.search_products("Chocolope", status='any')
    
    if products:
        print(f"Found {len(products)} matches:")
        for p in products:
            print(f"ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print(f"Created: {p['created_at']}")
            print("-" * 30)
    else:
        print("❌ No products found with title 'Chocolope'")

if __name__ == "__main__":
    find_chocolope()
