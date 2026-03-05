#!/usr/bin/env python3
"""
Update a Cannibisters product on Shopify with metafields, description, and tags
"""

import argparse
import json
import sys
from shopify_api import (
    get_product, 
    search_products,
    update_product_description, 
    update_product_metafields,
    get_product_metafields
)


def format_metafields_for_api(metafields_dict: dict) -> dict:
    """
    Convert metafields from user-friendly format to API format
    
    Expected input format:
    {
        "lineage": "Ice Cream Cake x Whipped Cream",
        "flowering_time": "8-9 weeks",
        ...
    }
    
    Output format:
    {
        "my_fields": {
            "lineage": "Ice Cream Cake x Whipped Cream",
            "flowering_time": "8-9 weeks"
        }
    }
    """
    # Default to 'my_fields' namespace for all metafields (Cannibisters custom namespace)
    return {"my_fields": metafields_dict}


def display_product_info(product: dict):
    """Display current product information"""
    print(f"\n📦 Product: {product['title']}")
    print(f"   ID: {product['id']}")
    print(f"   Status: {product['status']}")
    print(f"   Type: {product.get('product_type', 'N/A')}")
    
    if product.get('body_html'):
        print(f"\n📝 Current Description:")
        print(f"   {product['body_html'][:200]}...")
    
    if product.get('tags'):
        print(f"\n🏷️  Current Tags: {product['tags']}")
    
    # Get and display metafields
    metafields = get_product_metafields(str(product['id']))
    if metafields:
        print(f"\n🗂️  Current Metafields:")
        for namespace, fields in metafields.items():
            print(f"   [{namespace}]")
            for key, value in fields.items():
                print(f"      {key}: {value}")


def main():
    parser = argparse.ArgumentParser(description='Update Cannibisters product on Shopify')
    parser.add_argument('--product-id', type=str, help='Product ID')
    parser.add_argument('--product-name', type=str, help='Product name (will search)')
    parser.add_argument('--description', type=str, help='Product description (HTML)')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--metafields', type=str, help='Path to JSON file with metafields')
    parser.add_argument('--show-current', action='store_true', help='Show current product info')
    parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    # Get product ID
    product_id = args.product_id
    
    if not product_id and args.product_name:
        print(f"🔍 Searching for product: {args.product_name}")
        products = search_products(args.product_name)
        
        if not products:
            print(f"❌ No products found matching: {args.product_name}")
            sys.exit(1)
        
        if len(products) > 1:
            print(f"\n⚠️  Multiple products found:")
            for i, p in enumerate(products, 1):
                print(f"   {i}. {p['title']} (ID: {p['id']})")
            
            choice = input("\nEnter number to select product (or 'q' to quit): ")
            if choice.lower() == 'q':
                sys.exit(0)
            
            try:
                product_id = str(products[int(choice) - 1]['id'])
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                sys.exit(1)
        else:
            product_id = str(products[0]['id'])
            print(f"✅ Found product: {products[0]['title']} (ID: {product_id})")
    
    if not product_id:
        print("❌ Error: Must provide --product-id or --product-name")
        parser.print_help()
        sys.exit(1)
    
    # Get current product info
    product = get_product(product_id)
    if not product:
        print(f"❌ Product {product_id} not found")
        sys.exit(1)
    
    # Show current info if requested
    if args.show_current:
        display_product_info(product)
        sys.exit(0)
    
    # Check if we have updates to make
    if not any([args.description, args.tags, args.metafields]):
        print("ℹ️  No updates specified. Use --show-current to view product info.")
        parser.print_help()
        sys.exit(0)
    
    # Display current info
    display_product_info(product)
    
    # Show what will be updated
    print("\n" + "="*80)
    print("📝 PROPOSED UPDATES:")
    print("="*80)
    
    if args.description:
        print(f"\n✏️  New Description:")
        print(f"   {args.description[:200]}...")
    
    if args.tags:
        tags_list = [tag.strip() for tag in args.tags.split(',')]
        print(f"\n🏷️  New Tags: {', '.join(tags_list)}")
    
    if args.metafields:
        try:
            with open(args.metafields, 'r') as f:
                metafields_data = json.load(f)
            
            print(f"\n🗂️  New Metafields:")
            for key, value in metafields_data.items():
                print(f"      {key}: {value}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Error reading metafields file: {e}")
            sys.exit(1)
    
    # Confirm
    if not args.yes:
        confirm = input("\n❓ Proceed with these updates? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("❌ Update cancelled")
            sys.exit(0)
    
    # Perform updates
    print("\n🚀 Updating product...")
    
    success = True
    
    # Update description and tags
    if args.description or args.tags:
        tags_list = [tag.strip() for tag in args.tags.split(',')] if args.tags else None
        if update_product_description(product_id, args.description or product['body_html'], tags_list):
            print("✅ Description and tags updated")
        else:
            print("❌ Failed to update description/tags")
            success = False
    
    # Update metafields
    if args.metafields:
        formatted_metafields = format_metafields_for_api(metafields_data)
        if update_product_metafields(product_id, formatted_metafields):
            print("✅ Metafields updated")
        else:
            print("❌ Failed to update metafields")
            success = False
    
    if success:
        print("\n🎉 Product updated successfully!")
        print(f"   View in Shopify: https://admin.shopify.com/store/cannibisters/products/{product_id}")
    else:
        print("\n⚠️  Some updates failed. Please check the errors above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
