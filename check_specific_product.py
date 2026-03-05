import shopify_api
import json

pid = "9072669163732"
p = shopify_api.get_product(pid)
if p:
    print(f"ID: {p['id']}")
    print(f"Title: {p['title']}")
    print(f"Status: {p['status']}")
    print(f"Tags: {p.get('tags')}")
    print(f"Body: {p.get('body_html')}")
    print(f"Images: {len(p.get('images', []))}")
    # print(json.dumps(p.get('metafields', []), indent=2))
else:
    print(f"Product {pid} not found.")
