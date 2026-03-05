import shopify_api
import requests
import json

def find_targets():
    print("Fetching ALL products (active & draft)...")
    
    # We need to check both active and draft.
    # Shopify API defaults to published_status=published (active) if not specified? 
    # Or status=active.
    # To be safe, let's fetch status=active and status=draft separately or no status filter?
    # status=any is likely what we want if supported, or just loop both.
    
    statuses = ['active', 'draft']
    targets = ["Violet", "Blood", "Chocolope"]
    
    found = {}
    
    for status in statuses:
        url = f"{shopify_api.BASE_URL}/products.json?limit=250&status={status}"
        while url:
            print(f"Fetching ({status}): {url}")
            resp = requests.get(url, headers=shopify_api.HEADERS)
            if resp.status_code != 200:
                print(f"Error: {resp.status_code} {resp.text}")
                break
                
            data = resp.json()
            products = data.get('products', [])
            
            for p in products:
                title = p.get('title', '')
                pid = str(p['id'])
                for t in targets:
                    if t.lower() in title.lower():
                        print(f"FOUND: {pid} - {title} [{status}]")
                        
            link = resp.headers.get('Link')
            url = None
            if link and 'rel="next"' in link:
                url = link.split(';')[0].strip('< >')

if __name__ == "__main__":
    find_targets()
