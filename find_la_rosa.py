#!/usr/bin/env python3
import shopify_api

def find_la_rosa():
    print("🔍 Searching for 'LA Rosa'...")
    # Search all statuses
    products = shopify_api.search_products("LA Rosa", status='any')
    
    if products:
        print(f"Found {len(products)} matches:")
        for p in products:
            print(f"ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print(f"Created: {p['created_at']}")
            print(f"Tags: {p.get('tags')}")
            print("-" * 30)
    else:
        print("❌ No products found with title 'LA Rosa'")
        print("\nSearching in recent products...")
        # Fallback: check recent products
        recent = shopify_api.list_products(limit=250, status='active')
        drafts = shopify_api.list_products(limit=250, status='draft')
        all_products = recent + drafts
        all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        print("Top 5 most recent:")
        for p in all_products[:5]:
            print(f"ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print(f"Created: {p['created_at']}")
            print("-" * 30)

if __name__ == "__main__":
    find_la_rosa()
