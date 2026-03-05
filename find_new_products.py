import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv('/Users/norton/Desktop/Cannibisters Agent/.env')

SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
SHOPIFY_STORE_URL = os.getenv('SHOPIFY_STORE_URL')
API_VERSION = '2024-01'
BASE_URL = f'https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}'
HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

# Get all products sorted by created_at desc, both draft and active
response = requests.get(
    f'{BASE_URL}/products.json',
    headers=HEADERS,
    params={'limit': 20, 'status': 'any', 'order': 'created_at desc'}
)
response.raise_for_status()
products = response.json()['products']

print(f"📦 Most recently created products ({len(products)}):\n")
for p in products:
    created = p.get('created_at', 'Unknown')[:10]
    print(f"  ID: {p['id']}  |  Status: {p['status']}  |  Created: {created}  |  Title: {p['title']}")
