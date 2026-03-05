#!/usr/bin/env python3
import json
import requests
from shopify_api import list_products

def load_schedule(path):
    with open(path, 'r') as f:
        return json.load(f)

def map_products():
    schedule = load_schedule('advent_calendar_schedule.json')
    mapping = {}
    
    unique_names = sorted(list(set(item['product'] for item in schedule)))
    print(f"🔍 Found {len(unique_names)} unique products in schedule.")
    
    print("📦 Fetching all products from store (by status)...")
    all_products = []
    
    # Combined statuses since 'any' is failing
    for status in ['active', 'draft', 'archived']:
        print(f"   Fetching {status} products...")
        from shopify_api import BASE_URL, HEADERS
        url = f'{BASE_URL}/products.json'
        params = {'limit': 250, 'status': status}
        
        status_count = 0
        while url:
            try:
                response = requests.get(url, headers=HEADERS, params=params)
                response.raise_for_status()
                batch = response.json().get('products', [])
                all_products.extend(batch)
                status_count += len(batch)
                
                link_header = response.headers.get('Link')
                if link_header and 'rel="next"' in link_header:
                    links = link_header.split(',')
                    url = None
                    for link in links:
                        if 'rel="next"' in link:
                            url = link.split(';')[0].strip('< >')
                    params = {}
                else:
                    url = None
            except Exception as e:
                print(f"      ❌ Error fetching {status}: {e}")
                url = None
        print(f"      Found {status_count} products.")
            
    print(f"✅ Retrieved {len(all_products)} products total.")
    
    for name in unique_names:
        print(f"   Matching: {name}...", end=" ", flush=True)
        # Try exact match
        match = next((p for p in all_products if p['title'].lower() == name.lower()), None)
        
        # Try partial match (name in title)
        if not match:
            matches = [p for p in all_products if name.lower() in p['title'].lower()]
            if matches:
                # Pick the one that most closely matches or just the first
                match = matches[0]
                print(f" (Partial match: {match['title']})", end="")
            else:
                # Try even broader: parts of name in title
                parts = name.split()
                if len(parts) >= 2:
                    potential = parts[0] + " " + parts[1]
                    matches = [p for p in all_products if potential.lower() in p['title'].lower()]
                    if matches:
                        match = matches[0]
                        print(f" (Broad match: {match['title']})", end="")

        if match:
            mapping[name] = {
                'id': match['id'],
                'title': match['title']
            }
            print(" ✅")
        else:
            print(" ❌ NOT FOUND")

    with open('advent_product_mapping.json', 'w') as f:
        json.dump(mapping, f, indent=4)
    
    print(f"\n✅ Mapping saved to advent_product_mapping.json")
    print(f"Mapped {len(mapping)}/{len(unique_names)} products.")

if __name__ == '__main__':
    map_products()
