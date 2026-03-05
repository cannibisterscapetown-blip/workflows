
import shopify_api

def find_collection_items():
    print("Fetching ALL products to filter locally...")
    # Fetch a large number of products with status='any' to cover drafts too
    all_products = shopify_api.list_products(limit=250, status='any')
    
    limited_collection = []
    canni_ltd = []
    
    for p in all_products:
        title = p['title']
        if "Limited Collection" in title:
            limited_collection.append(title)
        if "Canni Ltd" in title or "Cannibisters Limited" in title:
            canni_ltd.append(title)
            
    print(f"\nFound {len(limited_collection)} 'Limited Collection' items:")
    for t in limited_collection:
        print(f" - {t}")
        
    print(f"\nFound {len(canni_ltd)} 'Canni Ltd' items:")
    for t in canni_ltd:
        print(f" - {t}")

if __name__ == "__main__":
    find_collection_items()
