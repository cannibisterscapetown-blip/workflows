#!/usr/bin/env python3
import shopify_api

print("=== Searching for target products via GraphQL ===\n")

# Query multiple variations to ensure we catch them
# Note: GraphQL 'query' argument format for products search
search_query = 'title:*Girl* OR title:*Cookies* OR title:*Supercheese* OR title:*Elvis* OR title:*Sour Diesel* OR title:*Rosin* OR title:*Joint*'

query = f"""
{{
  products(first: 50, query: "{search_query}", sortKey: CREATED_AT, reverse: true) {{
    edges {{
      node {{
        id
        title
        status
        createdAt
      }}
    }}
  }}
}}
"""

result = shopify_api.graphql_query(query)

found_ids = {}

if result and 'data' in result and result['data']['products']:
    products = result['data']['products']['edges']
    print(f"Found {len(products)} potential matches\n")
    
    targets = [
        'Indoor Flower Rosin - Girl Scout Cookies',
        'Canni Ltd Edition Joint - Supercheese',
        'Canni Ltd Edition Joint - Elvis',
        'Canni Ltd Edition Joint - Sour Diesel'
    ]
    
    for edge in products:
        p = edge['node']
        gid = p['id']
        rest_id = gid.split('/')[-1] if '/' in gid else gid
        title = p['title']
        status = p['status']
        created = p['createdAt']
        
        # Check against targets
        is_match = False
        for t in targets:
            if t.lower() in title.lower() or title.lower() in t.lower(): # Loose matching
                print(f"MATCH FOUND: {title}")
                print(f"  ID: {rest_id}")
                print(f"  Status: {status}")
                print(f"  Created: {created}")
                print("-" * 20)
                found_ids[title] = rest_id
                is_match = True
                break
        
        if not is_match:
             # Print recent drafts as they are likely the new ones
             if status == 'DRAFT':
                 print(f"POTENTIAL DRAFT MATCH: {title}")
                 print(f"  ID: {rest_id}")
                 print("-" * 20)

else:
    print("No results from GraphQL query")
    if result and 'errors' in result:
        print(f"Errors: {result['errors']}")

print("\n=== Summary of IDs ===")
for t, i in found_ids.items():
    print(f"{t}: {i}")
