#!/usr/bin/env python3
import shopify_api
from collections import OrderedDict

print("=== searching for recent products ===\n")

# Use a workaround to get recent products since we can't sort by created_at in search easily without specific fields
# We'll just list all products (or a large number) and sort locally, OR search for * and sort?
# The `list_products` standard function might be better if it supports limits.
# Let's try searching for "Vape" first, as that is likely in the title or type.

print("--- Searching for 'Vape' ---")
vapes = shopify_api.search_products("Vape", status='any')
if vapes:
    # Sort by created_at desc
    vapes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    for p in vapes[:5]:
        print(f"Title: {p['title']}")
        print(f"ID: {p['id']}")
        print(f"Created: {p.get('created_at')}")
        print(f"Status: {p['status']}")
        print("-" * 20)
else:
    print("No Vapes found.")

print("\n--- Listing 5 most recent products generally ---")
# If we have a list_products tool that takes limits, good. 
# Looking at shopify_api.py (which I haven't read fully but I can guess)
# I'll rely on the fact that I can iterate.
# Actually, I'll just check `list_products.py` to see how it works.
# But for now, I'll just search for "Joint" as a proxy for "recent stuff" if Vapes fail, 
# OR just run a broad search if possible.
# Wait, I'll just look at `shopify_api.py` to see if there is a `get_products` with sort.

# Assuming get_all_products or similar exists or I can just use a broad search term.
# Let's try searching for "The" which is common.
products = shopify_api.search_products("The", status='any')
if products:
    products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    for p in products[:10]:
        print(f"Title: {p['title']}")
        print(f"ID: {p['id']}")
        print(f"Created: {p.get('created_at')}")
        print(f"Status: {p['status']}")
        print("-" * 20)

