
from shopify_api import list_products

print("Searching for 'New Strains'...")
# Get 250 drafts (should cover recent ones)
products = list_products(limit=250, status='draft')

found_count = 0
for p in products:
    tags = p.get('tags', '')
    if 'New Strains' in tags:
        print(f"DTO: {p['title']} (ID: {p['id']})")
        found_count += 1

if found_count == 0:
    print("No 'New Strains' found in drafts. Checking active...")
    products = list_products(limit=250, status='active')
    for p in products:
        tags = p.get('tags', '')
        if 'New Strains' in tags:
            print(f"ACTIVE: {p['title']} (ID: {p['id']})")
            found_count += 1
