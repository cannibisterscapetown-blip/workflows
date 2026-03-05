import sys
import shopify_api
import traceback

print("Script start", flush=True)
try:
    print("Listing products...", flush=True)
    products = shopify_api.list_products(limit=5, status='active')
    print(f"Products found: {len(products)}", flush=True)
    for p in products:
        if 'joint' in p.get('title', '').lower():
            print(f"JOINT: {p['title']} ({p['id']})", flush=True)
except Exception:
    traceback.print_exc()
print("Script end", flush=True)
