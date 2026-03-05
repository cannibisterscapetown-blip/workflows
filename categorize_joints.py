import shopify_api
import requests
import json

def categorize():
    cats = {'Normal Joints': [], 'Moonsticks': [], 'Super Joints': []}
    for status in ['active', 'draft']:
        url = f"{shopify_api.BASE_URL}/products.json?limit=250&status={status}"
        while url:
            resp = requests.get(url, headers=shopify_api.HEADERS)
            data = resp.json()
            products = data.get('products', [])
            for p in products:
                title = p['title'].lower()
                if 'moonstick' in title:
                    cats['Moonsticks'].append({"id": p['id'], "title": p['title']})
                elif 'super joint' in title:
                    cats['Super Joints'].append({"id": p['id'], "title": p['title']})
                elif 'joint' in title:
                    cats['Normal Joints'].append({"id": p['id'], "title": p['title']})
            
            link = resp.headers.get('Link')
            url = None
            if link and 'rel="next"' in link:
                url = link.split(';')[0].strip('< >')
    
    with open('joint_categories.json', 'w') as f:
        json.dump(cats, f, indent=2)
    print(f"Categorized {sum(len(v) for v in cats.values())} products.")

if __name__ == "__main__":
    categorize()
