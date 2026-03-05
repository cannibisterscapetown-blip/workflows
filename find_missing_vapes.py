#!/usr/bin/env python3
import shopify_api
import requests

def get_all_drafts():
    url = f'{shopify_api.BASE_URL}/products.json'
    params = {'limit': 250, 'status': 'draft'}
    
    print("Paginated DRAFT search started...")
    found_count = 0
    page = 1
    
    targets = ["skittlez", "sun of peach"]
    
    while url:
        print(f"  Scanning page {page}...")
        try:
            response = requests.get(url, headers=shopify_api.HEADERS, params=params)
            response.raise_for_status()
            batch = response.json().get('products', [])
            
            for p in batch:
                title = p.get('title', '').lower()
                if any(t in title for t in targets):
                    print(f"MATCH FOUND:")
                    print(f"  Title: {p['title']}")
                    print(f"  ID: {p['id']}")
                    print(f"  Status: {p['status']}")
                    print(f"  Created: {p.get('created_at')}")
                    print(f"  Updated: {p.get('updated_at')}")
                    print("-" * 20)
                    found_count += 1
            
            # Pagination
            link_header = response.headers.get('Link')
            url = None
            params = {}
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0].strip('< >')
            page += 1
            
        except Exception as e:
            print(f"Error: {e}")
            break
            
    print(f"Search complete. Found {found_count} matches.")

if __name__ == "__main__":
    get_all_drafts()
