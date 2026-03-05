#!/usr/bin/env python3
"""
List all products from Cannibisters Shopify store
"""

import argparse
import json
from shopify_api import list_products, search_products


def main():
    parser = argparse.ArgumentParser(description='List Cannibisters products from Shopify')
    parser.add_argument('--search', type=str, help='Search for products by name')
    parser.add_argument('--limit', type=int, default=250, help='Maximum number of products to return')
    parser.add_argument('--status', type=str, default='active', 
                       choices=['active', 'draft', 'archived', 'any'],
                       help='Product status filter')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Get products
    if args.search:
        print(f"🔍 Searching for products matching: {args.search}")
        products = search_products(args.search)
    else:
        print(f"📦 Fetching products (status: {args.status}, limit: {args.limit})...")
        products = list_products(limit=args.limit, status=args.status)
    
    if not products:
        print("No products found.")
        return
    
    # Output results
    if args.json:
        print(json.dumps(products, indent=2))
    else:
        print(f"\n✅ Found {len(products)} product(s):\n")
        print(f"{'ID':<15} {'Title':<50} {'Status':<10} {'Type':<20}")
        print("-" * 95)
        
        for product in products:
            product_id = str(product['id'])
            title = product['title'][:47] + '...' if len(product['title']) > 50 else product['title']
            status = product['status']
            product_type = product.get('product_type', 'N/A')[:17] + '...' if len(product.get('product_type', '')) > 20 else product.get('product_type', 'N/A')
            
            print(f"{product_id:<15} {title:<50} {status:<10} {product_type:<20}")
        
        print(f"\n📊 Total: {len(products)} products")


if __name__ == '__main__':
    main()
