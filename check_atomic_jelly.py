#!/usr/bin/env python3
"""
Check metafields for Atomic Jelly (working example)
"""

import requests
import json
from shopify_api import BASE_URL, HEADERS

product_id = "8999728644308"

print(f"📦 Atomic Jelly (ID: {product_id})")
print(f"{'='*80}\n")

# Get metafields
response = requests.get(
    f'{BASE_URL}/products/{product_id}/metafields.json',
    headers=HEADERS
)

if response.status_code == 200:
    metafields = response.json()['metafields']
    
    if metafields:
        print(f"Found {len(metafields)} metafields:\n")
        
        # Group by namespace
        by_namespace = {}
        for mf in metafields:
            ns = mf['namespace']
            if ns not in by_namespace:
                by_namespace[ns] = []
            by_namespace[ns].append(mf)
        
        for namespace, fields in by_namespace.items():
            print(f"\n[{namespace}]")
            for mf in fields:
                print(f"  Key: {mf['key']}")
                print(f"  Value: {mf['value']}")
                print(f"  Type: {mf['type']}")
                print(f"  ID: {mf['id']}")
                print()
    else:
        print("⚠️  No metafields found!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
