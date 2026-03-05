import shopify_api
import requests
import json

def find_products():
    targets = [
        "ABG", "Moonstick", "Mints", "Sherbet", "Sherbert", "CBD", "THC", "Distillate", "Drops", "Chimera"
    ]
    
    found = []
    
    for status in ['active', 'draft']:
        url = f"{shopify_api.BASE_URL}/products.json?limit=250&status={status}"
        while url:
            resp = requests.get(url, headers=shopify_api.HEADERS)
            data = resp.json()
            products = data.get('products', [])
            
            for p in products:
                title = p['title'].lower()
                if any(t.lower() in title for t in targets):
                    found.append({"id": p['id'], "title": p['title'], "status": p['status']})
            
            link = resp.headers.get('Link')
            url = None
            if link and 'rel="next"' in link:
                url = link.split(';')[0].strip('< >')
                
    for f in found:
        print(f"{f['id']}: {f['title']} [{f['status']}]")

if __name__ == "__main__":
    find_products()
