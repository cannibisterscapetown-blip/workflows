#!/usr/bin/env python3
import shopify_api
from operator import itemgetter

print("=== Fetching latest products (Active & Draft) ===\n")

# Get actives
print("Fetching active products...")
actives = shopify_api.list_products(limit=50, status='active') or []
print(f"  Found {len(actives)} active.")

# Get drafts
print("Fetching draft products...")
drafts = shopify_api.list_products(limit=50, status='draft') or []
print(f"  Found {len(drafts)} drafts.")

# Combine
all_products = actives + drafts

if all_products:
    print(f"Total products fetched: {len(all_products)}")
    # Sort by created_at desc
    # some might lack created_at, handle that
    all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    print("\n--- TOP 20 NEWEST PRODUCTS ---")
    for p in all_products[:20]:
        title = p.get('title', 'No Title')
        pid = p.get('id', 'No ID')
        created = p.get('created_at', 'No Date')
        status = p.get('status', 'Unknown')
        print(f"Title: {title}")
        print(f"ID: {pid}")
        print(f"Created: {created}")
        print(f"Status: {status}")
        print("-" * 30)
else:
    print("No products found.")
