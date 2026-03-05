#!/usr/bin/env python3
import shopify_api

print("=== Searching for ALL Recent Rosin Products ===\n")

# Query for "Rosin" and sort by created_at descending
query = """
{
  products(first: 20, query: "title:*Rosin*", sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        id
        title
        status
        createdAt
        bodyHtml
      }
    }
  }
}
"""

result = shopify_api.graphql_query(query)

if result and 'data' in result and result['data']['products']:
    products = result['data']['products']['edges']
    print(f"Found {len(products)} Rosin products (newest first):\n")
    
    for edge in products:
        p = edge['node']
        gid = p['id']
        rest_id = gid.split('/')[-1] if '/' in gid else gid
        title = p['title']
        status = p['status']
        created = p['createdAt']
        desc = p['bodyHtml']
        
        print(f"Title: {title}")
        print(f"  ID: {rest_id}")
        print(f"  Status: {status}")
        print(f"  Created: {created}")
        print(f"  Desc Preview: {desc[:50] if desc else 'None'}")
        print("-" * 30)

else:
    print("No Rosin products found via GraphQL")
