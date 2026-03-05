
import requests
import shopify_api

def get_all_products(status='active'):
    all_products = []
    # Use headers from shopify_api
    headers = shopify_api.HEADERS
    base_url = shopify_api.BASE_URL
    
    url = f'{base_url}/products.json'
    # Start with initial params
    params = {'limit': 250, 'status': status}
    
    print(f"Paginated search started for status: {status}...")
    page = 1
    
    while url:
        print(f"  Fetching page {page}...")
        try:
            # For the first request, pass params. For subsequent (next link), params are usually in the URL
            current_params = params if page == 1 else {}
            
            response = requests.get(url, headers=headers, params=current_params)
            response.raise_for_status()
            
            data = response.json()
            batch = data.get('products', [])
            all_products.extend(batch)
            print(f"    Got {len(batch)} products.")
            
            # Pagination handling
            link_header = response.headers.get('Link')
            
            # Reset URL and prepare for next iteration
            next_url = None
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link.split(';')[0].strip('< >')
            
            url = next_url
            page += 1
            
            # Safety break
            if page > 50:
                print("Reached page 50, stopping.")
                break
                
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    print(f"Total products fetched: {len(all_products)}")
    return all_products

def search_collection_items():
    # 1. Fetch active products (likely where the items are)
    active_products = get_all_products(status='active')
    
    # 2. Fetch draft products (just in case)
    draft_products = get_all_products(status='draft')
    
    all_products = active_products + draft_products
    
    matches = []
    keywords = ["Limited Collection", "Canni Ltd", "Canni Limited"]
    
    print(f"\nScanning {len(all_products)} total products for keywords: {keywords}...")
    
    for p in all_products:
        title = p.get('title', '')
        # Check if any keyword is in title (case insensitive)
        if any(k.lower() in title.lower() for k in keywords):
            matches.append(p)
            
    print(f"\nFound {len(matches)} matching products:")
    for m in matches:
        print(f"- {m['title']} (ID: {m['id']}, Status: {m['status']})")

if __name__ == "__main__":
    search_collection_items()
