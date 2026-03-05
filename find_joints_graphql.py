#!/usr/bin/env python3
import shopify_api

# Try using GraphQL to search for products
query = """
{
  products(first: 50, query: "title:*Sherbet* OR title:*Patronus*") {
    edges {
      node {
        id
        title
        status
        createdAt
      }
    }
  }
}
"""

print("=== GraphQL Query for Orange Sherbet and Black Patronus ===\n")
result = shopify_api.graphql_query(query)

if result and 'data' in result:
    products = result['data']['products']['edges']
    print(f"Found {len(products)} products\n")
    for edge in products:
        product = edge['node']
        # Convert GraphQL ID to REST API ID
        gid = product['id']
        rest_id = gid.split('/')[-1] if '/' in gid else gid
        print(f"Title: {product['title']}")
        print(f"GraphQL ID: {gid}")
        print(f"REST ID: {rest_id}")
        print(f"Status: {product['status']}")
        print(f"Created: {product['createdAt']}")
        print()
else:
    print("Error or no results")
    print(result)
