#!/usr/bin/env python3
import shopify_api

print("=== Searching for Specific High Club Vapes ===\n")

queries = ["Skittlez", "Permanent Marker"]

for q in queries:
    print(f"--- Searching for '{q}' ---")
    products = shopify_api.search_products(q, status='any')
    if products:
        for p in products:
            print(f"  Title: {p['title']}")
            print(f"  ID: {p['id']}")
            print(f"  Status: {p['status']}")
            print(f"  Tags: {p.get('tags', '')}")
            print()
    else:
        print(f"  No matches found for '{q}'\n")
