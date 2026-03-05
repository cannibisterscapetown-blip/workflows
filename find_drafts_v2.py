#!/usr/bin/env python3
import shopify_api

print("=== Listing DRAFT products (Case-Insensitive) ===\n")

# Get drafts
products = shopify_api.list_products(limit=250, status='draft')

keywords = ["high club", "skittlez", "permanent", "lemon", "sun", "vape"]

if products:
    print(f"Found {len(products)} draft products.\n")
    for p in products:
        title = p.get('title', '').lower()
        if any(k in title for k in keywords):
            print(f"MATCH FOUND:")
            print(f"  Title: {p['title']}")
            print(f"  ID: {p['id']}")
            print(f"  Status: {p['status']}")
            print(f"  Created: {p.get('created_at')}")
            print("-" * 20)
else:
    print("No draft products returned.")
