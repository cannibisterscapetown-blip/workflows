
from shopify_api import get_product

product_ids = [
    "9016555864276",
    "901655995348",
    "9016556454100"
]

print("Checking products...")
for pid in product_ids:
    product = get_product(pid)
    if product:
        print(f"\nID: {pid}")
        print(f"Title: {product.get('title')}")
        print(f"Status: {product.get('status')}")
        print(f"Tags: {product.get('tags')}")
    else:
        print(f"\nID: {pid} - Not Found")
