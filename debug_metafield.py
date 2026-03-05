#!/usr/bin/env python3
"""
Debug metafield creation - get detailed error info
"""

import requests
import json
from shopify_api import BASE_URL, HEADERS

product_id = "9008376774868"  # Peachy Jam

# Try to create one metafield with detailed error handling
metafield_data = {
    "metafield": {
        "namespace": "my_fields",
        "key": "lineage",
        "value": "Traffic Jam x Peach Crescendo (peachy-sweet hybrid; balanced genetics)",
        "type": "single_line_text_field"
    }
}

print(f"🔍 Attempting to create my_fields.lineage metafield...")
print(f"Product ID: {product_id}\n")

response = requests.post(
    f'{BASE_URL}/products/{product_id}/metafields.json',
    headers=HEADERS,
    json=metafield_data
)

print(f"Status Code: {response.status_code}")
print(f"\nResponse Headers:")
for key, value in response.headers.items():
    if 'error' in key.lower() or 'message' in key.lower():
        print(f"  {key}: {value}")

print(f"\nResponse Body:")
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)
