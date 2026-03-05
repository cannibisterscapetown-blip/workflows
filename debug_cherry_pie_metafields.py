
import json
import shopify_api
import requests
from shopify_api import BASE_URL, HEADERS

SOURCE_PRODUCT_ID = "7973893505236"  # Cherry Pie
TARGET_PRODUCT_ID = "8374576021716" # Cherry Pie Joint

def check_raw(product_id, label="Product"):
    print(f"Fetching raw metafields for {label} ({product_id})...")
    url = f'{BASE_URL}/products/{product_id}/metafields.json'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        metafields = response.json()['metafields']
        print(f"Found {len(metafields)} metafields.")
        for mf in metafields:
            if mf['namespace'] == 'my_fields':
                print(f" - {mf['key']}: {mf['value']} (Type: {mf['type']})")
        return metafields
    else:
        print(f"Failed to fetch: {response.text}")
        return []

def main():
    source_mfs = check_raw(SOURCE_PRODUCT_ID, "Source (Cherry Pie)")
    print("-" * 20)
    target_mfs = check_raw(TARGET_PRODUCT_ID, "Target (Joint)")

if __name__ == "__main__":
    main()
