#!/usr/bin/env python3
import shopify_api

keywords = ["2ml", "Disposable", "Vape", "High Club", "Gelato", "Wedding"]

print("=== Searching for keywords ===\n")

for kw in keywords:
    print(f"--- Searching for '{kw}' ---")
    products = shopify_api.search_products(kw, status='any')
    if products:
        # Sort by ID (proxy for creation time roughly) to show newest first
        products.sort(key=lambda x: x.get('id', 0), reverse=True)
        for p in products[:3]:
            print(f"  Title: {p['title']}")
            print(f"  ID: {p['id']}")
            print(f"  Status: {p['status']}")
            print(f"  Created: {p.get('created_at')}")
            print()
    else:
        print(f"  No matches for '{kw}'\n")
