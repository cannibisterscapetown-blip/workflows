
import shopify_api
product = shopify_api.get_product('8949573976276')
if product:
    print(f"TITLE: '{product['title']}'")
