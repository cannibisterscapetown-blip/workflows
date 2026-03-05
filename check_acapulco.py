import shopify_api
p = shopify_api.get_product("7859423576276")
print(f"Title: {p['title']}")
print(f"Tags: {p['tags']}")
print(f"Body: {p['body_html']}")
