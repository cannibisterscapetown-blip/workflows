#!/usr/bin/env python3
import shopify_api

def find_chocolope():
    print("🔍 Searching for 'Chocolope'...")
    products = shopify_api.search_products("Chocolope", status='any')
    
    if products:
        print(f"Found {len(products)} matches:")
        for p in products:
            print(f"ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print("-" * 30)
    else:
        print("❌ No products found")
        print("\nTrying broader search...")
        # Try listing recent products
        recent = shopify_api.list_products(limit=50, status='active')
        for p in recent:
            if 'chocolope' in p['title'].lower():
                print(f"ID: {p['id']}")
                print(f"Title: {p['title']}")
                print(f"Status: {p['status']}")
                print("-" * 30)

if __name__ == "__main__":
    find_chocolope()
