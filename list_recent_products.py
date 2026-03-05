
from shopify_api import list_products

print("Listing recent products...")
# listing 10 products, default is status='active' but I should check 'draft' too if possible?
# The list_products function takes status arg.

print("\n--- Active Products ---")
products = list_products(limit=10, status='active')
for p in products:
    print(f"ID: {p['id']} - Title: {p['title']}")

print("\n--- Draft Products ---")
products = list_products(limit=10, status='draft')
for p in products:
    print(f"ID: {p['id']} - Title: {p['title']}")
