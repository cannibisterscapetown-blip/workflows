#!/usr/bin/env python3
import shopify_api
import requests

# Re-implementing list_products with pagination here because shopify_api.list_products doesn't have it
def get_all_products():
    all_products = []
    url = f'{shopify_api.BASE_URL}/products.json'
    params = {'limit': 250, 'status': 'any'}
    
    print("Paginated search started...")
    page = 1
    while url:
        print(f"  Fetching page {page}...")
        try:
            response = requests.get(url, headers=shopify_api.HEADERS, params=params)
            response.raise_for_status()
            batch = response.json().get('products', [])
            all_products.extend(batch)
            
            # Pagination
            link_header = response.headers.get('Link')
            url = None
            params = {} # Clear params for next link as the link has them
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0].strip('< >')
            page += 1
        except Exception as e:
            print(f"Error: {e}")
            break
            
    print(f"Total products fetched: {len(all_products)}")
    return all_products

products = get_all_products()
targets = ["High Club", "Skittlez", "Permanent", "Sun of Peach"]

print("\n=== Matches ===")
for p in products:
    title = p.get('title', '')
    if any(t.lower() in title.lower() for t in targets):
        print(f"Title: {title}")
        print(f"ID: {p['id']}")
        print(f"Status: {p['status']}")
        print(f"Created: {p.get('created_at')}")
        print("-" * 20)
