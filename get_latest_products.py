import shopify_api
import requests
import json

def get_latest():
    all_p = []
    for status in ['active', 'draft']:
        url = f"{shopify_api.BASE_URL}/products.json?limit=250&status={status}"
        while url:
            print(f"Fetching {status}: {url}")
            resp = requests.get(url, headers=shopify_api.HEADERS)
            data = resp.json()
            products = data.get('products', [])
            print(f"Found {len(products)} products")
            all_p.extend(products)
            link = resp.headers.get('Link')
            url = None
            if link and 'rel="next"' in link:
                url = link.split(';')[0].strip('< >')
    
    all_p.sort(key=lambda x: x['created_at'], reverse=True)
    for p in all_p[:20]:
        print(f"{p['id']}: {p['title']} [{p['status']}] ({p['created_at']})")

if __name__ == "__main__":
    get_latest()
