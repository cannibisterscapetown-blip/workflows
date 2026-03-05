from shopify_api import get_all_products

def find_product():
    print("Searching for 'Persian Pie Joint'...")
    products = get_all_products()
    for p in products:
        if "Persian Pie" in p['title'] and "Joint" in p['title']:
            print(f"FOUND: {p['title']} | ID: {p['id']}")
            return
    print("Not found.")

if __name__ == "__main__":
    find_product()
