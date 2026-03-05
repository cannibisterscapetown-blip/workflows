#!/usr/bin/env python3
import shopify_api

def find_blue_caviar():
    print("🔍 Searching for 'Blue Caviar'...")
    products = shopify_api.search_products("Blue Caviar", status='any')
    
    if products:
        print(f"Found {len(products)} matches:")
        for p in products:
            print(f"ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print("-" * 30)
    else:
        print("❌ No products found")

if __name__ == "__main__":
    find_blue_caviar()
