import shopify_api
p = shopify_api.get_product("9072669163732")
if p:
    print(f"TITLE: {p['title']}")
    print(f"DESC: {p.get('body_html')}")
    print(f"TAGS: {p.get('tags')}")
    print(f"IMAGES: {len(p.get('images', []))}")
else:
    print("Product not found")
