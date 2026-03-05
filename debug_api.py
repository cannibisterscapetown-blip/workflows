import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('SHOPIFY_ACCESS_TOKEN')
url = os.getenv('SHOPIFY_STORE_URL')
pid = "9072669163732"

print(f"DEBUG: Token starts with {token[:5]}", flush=True)
headers = {'X-Shopify-Access-Token': token, 'Content-Type': 'application/json'}
response = requests.get(f'https://{url}/admin/api/2024-01/products/{pid}.json', headers=headers)

if response.status_code == 200:
    data = response.json().get('product', {})
    print(f"TITLE: {data.get('title')}", flush=True)
    print(f"STATUS: {data.get('status')}", flush=True)
    print(f"DESC: {data.get('body_html')}", flush=True)
else:
    print(f"ERROR {response.status_code}: {response.text}", flush=True)
