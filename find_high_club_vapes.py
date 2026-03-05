#!/usr/bin/env python3
import shopify_api

print("=== Searching for 'The High Club' products via API ===\n")

# Search active and draft
products = shopify_api.search_products("The High Club", status='any')

if products:
    for p in products:
        print(f"  Title: {p['title']}")
        print(f"  ID: {p['id']}")
        print(f"  Status: {p['status']}")
        print(f"  Created: {p.get('created_at', 'Unknown')}")
        print()
else:
    print(f"  No matches found for 'The High Club'\n")
