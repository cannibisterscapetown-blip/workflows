#!/usr/bin/env python3
import shopify_api

print("=== Searching for target products via API ===\n")

targets = [
    'Indoor Flower Rosin - Girl Scout Cookies',
    'Canni Ltd Edition Joint - Supercheese',
    'Canni Ltd Edition Joint - Elvis',
    'Canni Ltd Edition Joint - Sour Diesel',
    'Girl Scout Cookies', # Fallback
    'Supercheese', # Fallback
    'Elvis', # Fallback
    'Sour Diesel' # Fallback
]

found_ids = {}

for target in targets:
    print(f"--- Searching for: '{target}' ---")
    # Search active and draft
    products = shopify_api.search_products(target, status='any')
    
    if products:
        for p in products:
            print(f"  Title: {p['title']}")
            print(f"  ID: {p['id']}")
            print(f"  Status: {p['status']}")
            print(f"  Created: {p.get('created_at', 'Unknown')}")
            found_ids[p['title']] = p['id']
            print()
    else:
        print(f"  No matches found for '{target}'\n")

print("\n=== Summary of Found IDs ===")
for title, pid in found_ids.items():
    print(f"{title}: {pid}")
