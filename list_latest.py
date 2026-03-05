import shopify_api
import sys

print("🚀 Script starting", flush=True)
try:
    products = shopify_api.list_products(limit=15, status='any')
    print(f"✅ Fetched {len(products)} products", flush=True)
    for p in products:
        print(f"ID: {p['id']} | TITLE: {p['title']} | STATUS: {p['status']}", flush=True)
        if str(p['id']) == "9072669163732":
            print("🎯 TARGET MATCH FOUND!", flush=True)
except Exception as e:
    print(f"❌ ERROR: {e}", file=sys.stderr, flush=True)
