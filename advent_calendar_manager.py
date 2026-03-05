#!/usr/bin/env python3
"""
Advent Calendar Manager
Handles the daily rotation of products for the Advent Calendar collection.
"""

import json
import datetime
import os
import sys
import argparse
from typing import Dict, Optional, List
import shopify_api

SCHEDULE_FILE = 'advent_calendar_schedule.json'
COLLECTION_TITLE = 'Advent calendar'

def load_schedule() -> list:
    """Load the advent calendar schedule"""
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {SCHEDULE_FILE} not found.")
        sys.exit(1)

def get_todays_drop(schedule: list, day_override: Optional[int] = None) -> Optional[Dict]:
    """Get the product scheduled for today"""
    today = datetime.datetime.now().day
    if day_override:
        today = day_override
        print(f"ℹ️ Overriding date to Day {today}")
            
    for item in schedule:
        if item['day'] == today:
            return item
    return None

def restore_product_price(product: Dict) -> bool:
    """Restore a product's price to its original value"""
    product_id = product['id']
    # We need to fetch the full product details to get variants
    full_product = shopify_api.get_product(product_id)
    if not full_product:
        return False
        
    success = True
    for variant in full_product['variants']:
        compare_at = variant.get('compare_at_price')
        if compare_at:
            # Restore original price
            print(f"  Restoring price for variant {variant['id']} to {compare_at}")
            if not shopify_api.update_product_price(product_id, float(compare_at), None):
                success = False
    return success

def apply_discount(product: Dict, discount_percent: int) -> bool:
    """Apply discount to a product"""
    product_id = product['id']
    full_product = shopify_api.get_product(product_id)
    if not full_product:
        return False
        
    success = True
    for variant in full_product['variants']:
        original_price = float(variant['price'])
        # If already on sale, use the compare_at_price as original
        if variant.get('compare_at_price'):
            original_price = float(variant['compare_at_price'])
            
        discount_multiplier = (100 - discount_percent) / 100
        new_price = round(original_price * discount_multiplier, 2)
        
        print(f"  Applying {discount_percent}% off to variant {variant['id']}")
        print(f"  Original: {original_price}, New: {new_price}")
        
        if not shopify_api.update_product_price(product_id, new_price, original_price):
            success = False
    return success

def main():
    parser = argparse.ArgumentParser(description='Advent Calendar Update Manager')
    parser.add_argument('day', type=int, nargs='?', help='Day number to run (optional)')
    parser.add_argument('--product', help='Override product name for testing')
    parser.add_argument('--discount', type=int, help='Override discount percent for testing')
    parser.add_argument('--keep', action='append', help='Product title to keep in collection (can be used multiple times)')
    parser.add_argument('--draft', action='store_true', help='Set product status to draft (for testing)')
    args = parser.parse_args()

    print("🎄 Starting Advent Calendar Update...")
    
    # 1. Find the collection
    collection = shopify_api.get_collection_by_title(COLLECTION_TITLE)
    if not collection:
        print(f"❌ Error: Collection '{COLLECTION_TITLE}' not found.")
        sys.exit(1)
    
    collection_id = collection['id']
    print(f"✅ Found collection: {COLLECTION_TITLE} ({collection_id})")
    
    # 2. Cleanup: Remove existing products and restore prices
    print("\n🧹 Cleaning up previous products...")
    current_products = shopify_api.get_products_in_collection(collection_id)
    
    products_to_keep = args.keep if args.keep else []
    
    for product in current_products:
        if product['title'] in products_to_keep:
            print(f"  Skipping removal of kept product: {product['title']}")
            continue
            
        print(f"  Removing {product['title']}...")
        if shopify_api.remove_product_from_collection(collection_id, product['id']):
            restore_product_price(product)
            
    # 3. Setup: Add today's product
    print("\n🎁 Setting up today's drop...")
    
    product_name = args.product
    discount_percent = args.discount
    
    if not product_name:
        schedule = load_schedule()
        todays_drop = get_todays_drop(schedule, args.day)
        
        if not todays_drop:
            print("ℹ️ No drop scheduled for today.")
            return
        product_name = todays_drop['product']
        discount_percent = todays_drop['discount_percent']

    print(f"  Today's Drop: {product_name} ({discount_percent}% off)")
    
    # Find the product
    products = shopify_api.search_products(product_name)
    if not products:
        print(f"❌ Error: Product '{product_name}' not found in Shopify.")
        return
        
    # Use the first match, but warn if multiple
    target_product = products[0]
    if len(products) > 1:
        print(f"⚠️ Warning: Multiple products found for '{product_name}'. Using the first one: {target_product['title']}")
    
    # Set status if requested
    if args.draft:
        print(f"  Setting status to DRAFT for testing...")
        shopify_api.update_product_status(target_product['id'], 'draft')

    # Apply discount
    if apply_discount(target_product, discount_percent):
        # Add to collection
        if shopify_api.add_product_to_collection(collection_id, target_product['id']):
            print("\n✨ Advent Calendar successfully updated! ✨")
        else:
            print("\n❌ Failed to add product to collection.")
    else:
        print("\n❌ Failed to update product price.")

if __name__ == '__main__':
    main()
