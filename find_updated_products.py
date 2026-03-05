#!/usr/bin/env python3
import shopify_api
from operator import itemgetter

print("=== Fetching recently UPDATED products ===\n")

all_products = []

for status in ['active', 'draft', 'archived']:
    print(f"Fetching {status} products (limit 50)...")
    # We can't sort by updated_at in the API easily (it supports order=updated_at+desc but let's just fetch and sort locally)
    # Actually API supports order param.
    # But let's stick to list_products from shopify_api which just takes limit/status.
    # We'll fetch 50 of each and sort locally.
    prods = shopify_api.list_products(limit=50, status=status) or []
    print(f"  Found {len(prods)} {status} products.")
    all_products.extend(prods)

if all_products:
    print(f"Total products fetched: {len(all_products)}")
    # Sort by updated_at desc
    all_products.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    
    print("\n--- TOP 20 MOST RECENTLY UPDATED ---")
    for p in all_products[:20]:
        title = p.get('title', 'No Title')
        pid = p.get('id', 'No ID')
        updated = p.get('updated_at', 'No Date')
        status = p.get('status', 'Unknown')
        print(f"Title: {title}")
        print(f"ID: {pid}")
        print(f"Updated: {updated}")
        print(f"Status: {status}")
        print("-" * 30)
else:
    print("No products found.")
