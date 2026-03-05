#!/usr/bin/env python3
import shopify_api

ids = [9062480642260, 9062481985748]

print("=== Identifying The High Club Vapes ===\n")

for pid in ids:
    product = shopify_api.get_product(str(pid))
    if product:
        print(f"ID: {pid}")
        print(f"Title: {product['title']}")
        print(f"Status: {product['status']}")
        current_tags = product.get('tags', '')
        print(f"Current Tags: {current_tags}")
        print("-" * 30)
    else:
        print(f"ID: {pid} NOT FOUND")
