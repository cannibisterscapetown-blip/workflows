#!/usr/bin/env python3
import shopify_api
import requests
import time

def get_all_drafts():
    all_products = []
    # Make sure we use the correct URL from shopify_api
    url = f'{shopify_api.BASE_URL}/products.json'
    params = {'limit': 250, 'status': 'draft'}
    
    print("Paginated DRAFT search started...")
    page = 1
    while url:
        print(f"  Fetching page {page}...")
        try:
            response = requests.get(url, headers=shopify_api.HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            batch = data.get('products', [])
            all_products.extend(batch)
            print(f"    Got {len(batch)} products.")
            
            # Pagination
            link_header = response.headers.get('Link')
            url = None
            params = {} # Clear params for next link
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0].strip('< >')
            page += 1
            # Safety break
            if page > 20:
                print("Reached page 20, stopping.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
            
    print(f"Total drafts fetched: {len(all_products)}")
    return all_products

products = get_all_drafts()
keywords = ["high club", "skittlez", "permanent", "sun of peach", "lemon"]

print("\n=== Matches ===")
for p in products:
    title = p.get('title', '').lower()
    if any(k in title for k in keywords):
        print(f"Match: {p.get('title')}")
        print(f"ID: {p['id']}")
        print(f"Created: {p.get('created_at')}")
        print("-" * 20)
