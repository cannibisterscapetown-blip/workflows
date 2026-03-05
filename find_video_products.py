import shopify_api
import requests
import json

def find_products():
    targets = [
        "CBD",
        "Mints",
        "Sherbet Rosin",
        "1200mg",
        "600mg",
        "Platinum Chimera",
        "Distillate"
    ]
    
    found = {}
    
    for status in ['active', 'draft']:
        url = f"{shopify_api.BASE_URL}/products.json?limit=250&status={status}"
        while url:
            resp = requests.get(url, headers=shopify_api.HEADERS)
            data = resp.json()
            products = data.get('products', [])
            
            for p in products:
                title = p['title'].lower()
                for t in targets:
                    query = t.lower()
                    # Basic match
                    if query in title or (query == "joint 01" and "joint" in title):
                         if t not in found:
                             found[t] = []
                         found[t].append({"id": p['id'], "title": p['title']})
            
            link = resp.headers.get('Link')
            url = None
            if link and 'rel="next"' in link:
                url = link.split(';')[0].strip('< >')
                
    print(json.dumps(found, indent=2))

if __name__ == "__main__":
    find_products()
