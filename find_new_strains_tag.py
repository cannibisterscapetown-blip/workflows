import shopify_api

def find_by_tag():
    print("🔍 Searching for products with 'New Strains' tag...")
    products = shopify_api.list_products(limit=50, status='any')
    
    new_strains = [p for p in products if p.get('tags') and 'New Strains' in p['tags']]
    
    print(f"\nFound {len(new_strains)} products with 'New Strains' tag:")
    for p in new_strains:
        print(f"\nID: {p['id']}")
        print(f"Title: {p['title']}")
        print(f"Status: {p['status']}")
        print(f"Tags: {p.get('tags')}")
        print(f"Description: {p.get('body_html', '')[:100]}...")

if __name__ == "__main__":
    find_by_tag()
