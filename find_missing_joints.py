import shopify_api
import requests
import json

def find_them():
    all_p = []
    print("Fetching ALL draft products...")
    url = f"{shopify_api.BASE_URL}/products.json?limit=250&status=draft"
    while url:
        print(f"Fetching: {url}")
        resp = requests.get(url, headers=shopify_api.HEADERS)
        data = resp.json()
        products = data.get('products', [])
        all_p.extend(products)
        link = resp.headers.get('Link')
        url = None
        if link and 'rel="next"' in link:
            url = link.split(';')[0].strip('< >')
    
    print(f"Total drafts found: {len(all_p)}")
    
    targets = ["Papa", "Chocolope", "Astro", "Ltd"]
    for p in all_p:
        title = p.get('title', '')
        # Check against targets
        for t in targets:
            if t.lower() in title.lower():
                print(f"FOUND: {p['id']} - {title}")

if __name__ == "__main__":
    find_them()
