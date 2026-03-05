import sys
import shopify_api
import traceback

print("Script start", flush=True)
try:
    print("Listing Active products...", flush=True)
    products = shopify_api.list_products(limit=30, status='active')
    print("Listing Draft products...", flush=True)
    drafts = shopify_api.list_products(limit=30, status='draft')

    all_products = products + drafts
    all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    print(f"\nScanning {len(all_products)} recent products for 'Joint' or 'Moonstick'...", flush=True)

    count = 0
    for p in all_products:
        title = p.get('title', '').lower()
        if 'joint' in title or 'moonstick' in title:
            count += 1
            print(f"\n🎯 MATCH FOUND [{count}]")
            print(f"ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print(f"Created: {p['created_at']}")
            print(f"Description (HTML): {p.get('body_html', '')}")
            print(f"Tags: {p.get('tags')}")
            print("-" * 40)

except Exception:
    traceback.print_exc()
print("Script end", flush=True)
