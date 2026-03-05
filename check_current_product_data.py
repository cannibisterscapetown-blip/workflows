#!/usr/bin/env python3
import shopify_api

ids = {
    "Indoor Flower Rosin - Girl Scout Cookies": 9059481419988,
    "Canni Ltd Edition Joint - Supercheese": 9059463594196,
    "Canni Ltd Edition Joint - Elvis": 9059463004372,
    "Canni Ltd Edition Joint - Sour Diesel": 9059462545620
}

print("=== Inspecting Current Product Data ===\n")

for name, pid in ids.items():
    print(f"--- {name} ({pid}) ---")
    product = shopify_api.get_product(pid)
    
    if product:
        desc = product.get('body_html', '')
        print(f"Title: {product['title']}")
        print(f"Status: {product['status']}")
        print(f"Description Length: {len(desc) if desc else 0}")
        print(f"Description Preview: {desc[:200] if desc else 'None'}")
        
        # Check for ratios in description
        if desc and ('/' in desc or '%' in desc):
            print("POTENTIAL RATIO FOUND in description")
            # Simple content dump to see what's there
            print(f"Full Description:\n{desc}\n")
            
        print("Metafields:")
        if 'metafields' in product and product['metafields']:
            for mf in product['metafields']:
                print(f"  {mf['namespace']}.{mf['key']}: {mf['value']}")
        else:
            print("  None")
    else:
        print("  Product not found")
    print()
