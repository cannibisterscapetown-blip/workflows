import shopify_api

pids = ["9072664772820", "8944913187028", "8822549676244", "8829780754644"]

for pid in pids:
    p = shopify_api.get_product(pid)
    if not p:
        print(f"❌ {pid} NOT FOUND")
        continue
    print(f"\n--- {p['title']} ({p['id']}) ---")
    print(f"Tags: {p['tags']}")
    print(f"Profile: {p['body_html'][:50]}...")
    print(f"Images: {len(p.get('images', []))}")
    if p.get('images'):
        print(f"First Image: {p['images'][0]['src']}")
