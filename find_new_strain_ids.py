import json
from shopify_api import list_products

target_strains = [
    "Blue Cheese",
    "Sour Diesel D",
    "Sour Diesel MS1",
    "Astro Grape",
    "White Widow",
    "Mad Ghost",
    "Girl Scout Cookies",
    "Christmas Cracker",
    "SUPERCHEESE",
    "ELVIS",
    "Grandpa's Endgame",
    "Purple Panda"
]

def find_strains():
    found = {}
    
    # Check Active
    print("Checking active products...")
    active_products = list_products(limit=250, status='active')
    # If there are more than 250, we might need paging, but usually new ones are in the first 250
    # Actually, let's just search for the strings
    for p in active_products:
        p_title = p['title'].lower()
        for target in target_strains:
            if target.lower() in p_title:
                found[target] = p['id']
    
    # Check Draft
    print("Checking draft products...")
    draft_products = list_products(limit=250, status='draft')
    for p in draft_products:
        p_title = p['title'].lower()
        for target in target_strains:
            if target.lower() in p_title and target not in found:
                found[target] = p['id']
                
    return found

if __name__ == "__main__":
    results = find_strains()
    print("\n--- Results ---")
    for strain in target_strains:
        status = results.get(strain, "NOT FOUND")
        print(f"{strain}: {status}")
    
    with open('found_strains.json', 'w') as f:
        json.dump(results, f, indent=2)
