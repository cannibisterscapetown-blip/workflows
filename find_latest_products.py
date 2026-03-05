#!/usr/bin/env python3
import shopify_api
from datetime import datetime

print("=== Fetching latest products ===\n")

# Get 50 products
products = shopify_api.list_products(limit=50, status='any')

if products:
    print(f"Fetched {len(products)} products. Sorting by created_at...")
    # Sort by created_at desc
    # Handle missing created_at just in case
    products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    print("\n--- TOP 10 NEWEST PRODUCTS ---")
    for p in products[:10]:
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
    print("No products returned.")
