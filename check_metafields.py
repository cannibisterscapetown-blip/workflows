#!/usr/bin/env python3
"""
Check metafields for Peachy Jam and Gelato Drops
"""

import requests
import json
from shopify_api import BASE_URL, HEADERS

# Product IDs
peachy_jam_id = "9008376774868"
gelato_drops_id = "9008376086740"

products = {
    "Peachy Jam": peachy_jam_id,
    "Gelato Drops": gelato_drops_id
}

for name, product_id in products.items():
    print(f"\n{'='*80}")
    print(f"📦 {name} (ID: {product_id})")
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
                print(f"[{namespace}]")
                for mf in fields:
                    value_preview = str(mf['value'])[:60]
                    if len(str(mf['value'])) > 60:
                        value_preview += "..."
                    print(f"  {mf['key']}: {value_preview}")
                    print(f"    Type: {mf['type']}")
                    print(f"    ID: {mf['id']}")
                print()
        else:
            print("⚠️  No metafields found!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
