#!/usr/bin/env python3
import shopify_api
import os

print("=== Debugging Shopify Connection ===")

# Test connection
print("Testing connection...")
if shopify_api.test_connection():
    print("Connection Successful!")
else:
    print("Connection Failed!")

print("\n=== Listing 1 Product ===")
try:
    products = shopify_api.list_products(limit=1, status='active')
    if products:
        print(f"Found product: {products[0]['title']} (ID: {products[0]['id']})")
    else:
        print("No products found (even with limit=1, status='active')")
except Exception as e:
    print(f"Error listing products: {e}")
