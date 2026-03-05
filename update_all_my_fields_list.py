#!/usr/bin/env python3
"""
Update all three products with my_fields namespace metafields using LIST type
"""

from shopify_api import create_or_update_metafield
import requests
from shopify_api import BASE_URL, HEADERS

def create_or_update_list_metafield(product_id: str, namespace: str, key: str, value: str) -> bool:
    """
    Create or update a LIST metafield (list.single_line_text_field type)
    """
    try:
        # Check if metafield exists
        metafields_response = requests.get(
            f'{BASE_URL}/products/{product_id}/metafields.json',
            headers=HEADERS,
            params={'namespace': namespace, 'key': key}
        )
        metafields_response.raise_for_status()
        existing_metafields = metafields_response.json()['metafields']
        
        # For list type, wrap value in JSON array
        data = {
            'metafield': {
                'namespace': namespace,
                'key': key,
                'value': f'["{value}"]',  # Wrap in array
                'type': 'list.single_line_text_field'
            }
        }
        
        if existing_metafields:
            # Update existing metafield
            metafield_id = existing_metafields[0]['id']
            response = requests.put(
                f'{BASE_URL}/metafields/{metafield_id}.json',
                headers=HEADERS,
                json=data
            )
        else:
            # Create new metafield
            response = requests.post(
                f'{BASE_URL}/products/{product_id}/metafields.json',
                headers=HEADERS,
                json=data
            )
        
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return False

# Products to update
products = {
    "Gelato Drops": {
        "id": "9008376086740",
        "list_fields": {
            "lineage": "Sunset Sherbet x Thin Mint Girl Scout Cookies (legendary dessert hybrid from Cookie Fam)",
            "flowering_time": "8–9 weeks",
            "effects": "Euphoric • Relaxed • Creative • Happy • Balanced body-mind buzz",
            "breeder": "Cookie Fam Genetics x Sherbinskis (San Francisco origins)",
        }
    },
    "Peachy Jam": {
        "id": "9008376774868",
        "list_fields": {
            "lineage": "Traffic Jam x Peach Crescendo (peachy-sweet hybrid; balanced genetics)",
            "flowering_time": "8–9 weeks",
            "effects": "Euphoric • Relaxed • Uplifted • Happy • Balanced mind-body harmony",
            "breeder": "Genetic Avenue (Traffic Jam x Peach Crescendo cross)",
        }
    },
    "Black Patronus": {
        "id": "9008376185044",
        "list_fields": {
            "lineage": "Rainbow Sherbet #11 (RS-11) x Falcon 9 (Exotic Genetix creation)",
            "flowering_time": "8–9 weeks",
            "effects": "Relaxed • Euphoric • Focused • Uplifted • Creative",
            "breeder": "Exotic Genetix (Washington-based breeder)",
        }
    }
}

print("🚀 Updating all products with my_fields namespace metafields (LIST type)...")
print("="*80)

for product_name, data in products.items():
    product_id = data["id"]
    list_fields = data["list_fields"]
    
    print(f"\n📦 {product_name} (ID: {product_id})")
    print("-"*80)
    
    success_count = 0
    fail_count = 0
    
    for key, value in list_fields.items():
        print(f"   {key}...", end=" ")
        if create_or_update_list_metafield(product_id, "my_fields", key, value):
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1
    
    print(f"\n   ✅ Successful: {success_count} | ❌ Failed: {fail_count}")

print(f"\n{'='*80}")
print("🎉 All products updated!")
print(f"{'='*80}")
