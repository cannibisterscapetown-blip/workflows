
import shopify_api
import json

product_id = "9071245623508"
try:
    product = shopify_api.get_product(product_id)
    if product:
        print(f"Product Title: {product.get('title')}")
        print(f"Product Type: {product.get('product_type')}")
        print(f"JSON Dump: {json.dumps(product, indent=2)}")
    else:
        print(f"Product {product_id} not found.")
except Exception as e:
    print(f"Error: {e}")
