import shopify_api
pid = "9072669163732"
p = shopify_api.get_product(pid)
if p:
    print(f"TITLE: {p['title']}")
    print(f"DESC: {p.get('body_html', 'No description')}")
    print(f"TAGS: {p.get('tags', '')}")
else:
    print("Product not found")
