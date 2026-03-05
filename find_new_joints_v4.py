import sys
import shopify_api
import traceback

print("Script start", flush=True)
try:
    print("Listing Active products...", flush=True)
    products = shopify_api.list_products(limit=10, status='active')
    print(f"Active Products found: {len(products)}", flush=True)
    for p in products:
        print(f"ACTIVE: {p['title']} ({p['id']})", flush=True)

    print("Listing Draft products...", flush=True)
    drafts = shopify_api.list_products(limit=10, status='draft')
    print(f"Draft Products found: {len(drafts)}", flush=True)
    for p in drafts:
        print(f"DRAFT: {p['title']} ({p['id']})", flush=True)

except Exception:
    traceback.print_exc()
print("Script end", flush=True)
