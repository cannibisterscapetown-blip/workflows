import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
STORE_NAME = os.getenv('SHOPIFY_STORE_NAME')
BASE_URL = f'https://{STORE_NAME}.myshopify.com/admin/api/2024-01'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def list_all_products(status='active'):
    products = []
    url = f'{BASE_URL}/products.json'
    params = {'limit': 250, 'status': status}
    
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        products.extend(response.json()['products'])
        
        # Paging via 'Link' header
        link = response.headers.get('Link')
        if link and 'rel="next"' in link:
            url = link.split(';')[0].strip('<>')
            params = {} # Params are already in the next URL
        else:
            url = None
    return products

target_strains = [
    "Sour Diesel D",
    "Sour Diesel MS1",
    "White Widow",
    "SUPERCHEESE"
]

def find_missing():
    found = {}
    
    for status in ['active', 'draft', 'archived']:
        print(f"Checking {status} products...")
        products = list_all_products(status)
        for p in products:
            p_title = p['title'].lower()
            for target in target_strains:
                if target.lower() in p_title:
                    found[target] = p['id']
                    print(f"Found {target} ({status}): {p['id']}")
    
    return found

if __name__ == "__main__":
    results = find_missing()
    print("\n--- Missing Found ---")
    for strain in target_strains:
        status = results.get(strain, "NOT FOUND")
        print(f"{strain}: {status}")
