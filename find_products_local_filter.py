#!/usr/bin/env python3
import shopify_api

print("=== Listing recent products and filtering locally ===\n")

# Get 100 products
products = shopify_api.list_products(limit=100, status='any')

targets = ["High Club", "Skittlez", "Permanent", "Lemon", "Sun"]

found = []

if products:
    print(f"Scanned {len(products)} products.\n")
    for p in products:
        title = p.get('title', '')
        # Check if any target keyword is in the title
        if any(t.lower() in title.lower() for t in targets):
            found.append(p)
            print(f"MATCH FOUND:")
            print(f"  Title: {title}")
            print(f"  ID: {p['id']}")
            print(f"  Status: {p['status']}")
            print(f"  Created: {p.get('created_at')}")
            print("-" * 20)

    if not found:
        print("No matches found in the last 100 products.")
else:
    print("No products returned from API.")
