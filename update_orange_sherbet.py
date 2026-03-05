#!/usr/bin/env python3
"""
Update Orange Sherbet metafields
"""

import requests
from shopify_api import BASE_URL, HEADERS

def create_or_update_list_metafield(product_id: str, namespace: str, key: str, value: str) -> bool:
    """Create or update a LIST metafield"""
    try:
        metafields_response = requests.get(
            f'{BASE_URL}/products/{product_id}/metafields.json',
            headers=HEADERS,
            params={'namespace': namespace, 'key': key}
        )
        metafields_response.raise_for_status()
        existing_metafields = metafields_response.json()['metafields']
        
        data = {
            'metafield': {
                'namespace': namespace,
                'key': key,
                'value': f'["{value}"]',
                'type': 'list.single_line_text_field'
            }
        }
        
        if existing_metafields:
            metafield_id = existing_metafields[0]['id']
            response = requests.put(
                f'{BASE_URL}/metafields/{metafield_id}.json',
                headers=HEADERS,
                json=data
            )
        else:
            response = requests.post(
                f'{BASE_URL}/products/{product_id}/metafields.json',
                headers=HEADERS,
                json=data
            )
        
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

def create_or_update_single_metafield(product_id: str, namespace: str, key: str, value: str) -> bool:
    """Create or update a SINGLE metafield"""
    try:
        metafields_response = requests.get(
            f'{BASE_URL}/products/{product_id}/metafields.json',
            headers=HEADERS,
            params={'namespace': namespace, 'key': key}
        )
        metafields_response.raise_for_status()
        existing_metafields = metafields_response.json()['metafields']
        
        data = {
            'metafield': {
                'namespace': namespace,
                'key': key,
                'value': value,
                'type': 'single_line_text_field'
            }
        }
        
        if existing_metafields:
            metafield_id = existing_metafields[0]['id']
            response = requests.put(
                f'{BASE_URL}/metafields/{metafield_id}.json',
                headers=HEADERS,
                json=data
            )
        else:
            response = requests.post(
                f'{BASE_URL}/products/{product_id}/metafields.json',
                headers=HEADERS,
                json=data
            )
        
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

product_id = "9008378970324"

# List type metafields
list_fields = {
    "lineage": "Orange Cream x Purple Urkle x Cherry Pie (sweet citrus indica blend)",
    "flowering_time": "9–10 weeks",
    "effects": "Relaxed • Euphoric • Happy • Calm • Uplifted",
    "breeder": "Barney's Farm (premium genetics)",
}

# Single type metafields
single_fields = {
    "profile": "80/20 Indica-Dominant Hybrid",
    "height": "Medium",
    "stretch_percentage": "±30%",
    "average_thc_levels": "22–24%",
    "flavours": "Sweet orange candy, fresh citrus, creamy tangerine, earthy pine",
    "used_for": "Evening relaxation, stress relief, pain management, anxiety relief",
}

print("🚀 Updating Orange Sherbet metafields...")
print(f"   Product ID: {product_id}\n")

success_count = 0
fail_count = 0

# Update list fields
for key, value in list_fields.items():
    print(f"   {key}...", end=" ")
    if create_or_update_list_metafield(product_id, "my_fields", key, value):
        print("✅")
        success_count += 1
    else:
        print("❌")
        fail_count += 1

# Update single fields
for key, value in single_fields.items():
    print(f"   {key}...", end=" ")
    if create_or_update_single_metafield(product_id, "my_fields", key, value):
        print("✅")
        success_count += 1
    else:
        print("❌")
        fail_count += 1

print(f"\n📊 Results:")
print(f"   ✅ Successful: {success_count}")
print(f"   ❌ Failed: {fail_count}")

if fail_count == 0:
    print(f"\n🎉 All metafields updated successfully!")
    print(f"   View product: https://admin.shopify.com/store/cannibisters/products/{product_id}")
