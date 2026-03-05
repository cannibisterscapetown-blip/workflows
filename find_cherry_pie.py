import json
import os

def check_file(filename):
    if not os.path.exists(filename):
        print(f"{filename} not found.")
        return

    with open(filename, 'r') as f:
        try:
            data = json.load(f)
            # Handle list of products directly or {'products': [...]}
            products = data.get('products', []) if isinstance(data, dict) else data
            
            for p in products:
                title = p.get('title', '')
                if 'Cherry Pie' in title:
                    print(f"File: {filename}")
                    print(f"ID: {p.get('id')}")
                    print(f"Title: {title}")
                    # Print metafields if present (some dumps might have them)
                    # Note: standard product list endpoint might not include metafields unless explicitly requested usually,
                    # but let's see what's in the file.
                    if 'metafields' in p:
                         print(f"Metafields: {p['metafields']}")
                    else:
                         print("No metafields in this dump.")
                    print("-" * 20)
        except json.JSONDecodeError:
            print(f"Error decoding {filename}")

check_file('all_products.json')
check_file('draft_products.json')
