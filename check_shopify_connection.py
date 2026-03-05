#!/usr/bin/env python3
import shopify_api
import os

print("=== Diagnostics ===\n")
print(f"Store URL env var present: {bool(os.getenv('SHOPIFY_STORE_URL'))}")
print(f"Access Token env var present: {bool(os.getenv('SHOPIFY_ACCESS_TOKEN'))}")

print("\n=== Testing Connection ===")
shopify_api.test_connection()

print("\n=== Listing ANY 5 Products ===")
try:
    products = shopify_api.list_products(limit=5, status='any')
    print(f"Count: {len(products)}")
    for p in products:
        print(f" - {p['title']} ({p['id']}) [{p['status']}]")
except Exception as e:
    print(f"Error listing products: {e}")
