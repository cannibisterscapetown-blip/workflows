import shopify_api
import requests
import json

def dump_all():
    print("Dumping ALL products to all_products.txt...")
    
    statuses = ['active', 'draft', 'archived']
    with open('all_products.txt', 'w') as f:
        for status in statuses:
            url = f"{shopify_api.BASE_URL}/products.json?limit=250&status={status}"
            while url:
                print(f"Fetching ({status})...")
                resp = requests.get(url, headers=shopify_api.HEADERS)
                if resp.status_code != 200:
                    print(f"Error: {resp.status_code}")
                    break
                    
                data = resp.json()
                products = data.get('products', [])
                
                for p in products:
                    line = f"{p['id']} | {p['title']} | {status}\n"
                    f.write(line)
                            
                link = resp.headers.get('Link')
                url = None
                if link and 'rel="next"' in link:
                    url = link.split(';')[0].strip('< >')

if __name__ == "__main__":
    dump_all()
