#!/usr/bin/env python3
import shopify_api

print("=== Listing DRAFT products ===\n")

# Get drafts
products = shopify_api.list_products(limit=250, status='draft')

if products:
    print(f"Found {len(products)} draft products.\n")
    for p in products:
        title = p.get('title', '')
        if "High Club" in title or "Skittlez" in title or "Permanent" in title:
            print(f"MATCH FOUND:")
            print(f"  Title: {title}")
            print(f"  ID: {p['id']}")
            print(f"  Status: {p['status']}")
            print(f"  Created: {p.get('created_at')}")
            print("-" * 20)
else:
    print("No draft products returned.")
