#!/usr/bin/env python3
"""
Cleanup New Strains Collection
Removes 'New Strains' tag from:
1. Draft products
2. Products that have been in the collection (based on creation date) for longer than a month.
"""

import shopify_api
import sys
from datetime import datetime, timezone, timedelta

COLLECTION_ID = "421846057172"
TAG_TO_REMOVE = "New Strains"
DAYS_THRESHOLD = 30

def parse_shopify_date(date_str):
    """Parse Shopify ISO 8601 date string"""
    try:
        # Check if python version supports fromisoformat (3.7+)
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (AttributeError, ValueError):
        # Fallback for older python or slightly different formats if needed
        # Simple manual parsing if fromisoformat fails or isn't available
        # Shopify format: 2024-01-01T12:00:00-05:00
        # For simplicity, let's try to just cut off the timezone if strict parsing fails
        # but fromisoformat should work on Mac system python 3.9+
        return datetime.strptime(date_str.split('T')[0], "%Y-%m-%d").replace(tzinfo=timezone.utc)

def cleanup_new_strains():
    print(f"Starting cleanup for collection {COLLECTION_ID}...")
    print(f"Criteria: Remove '{TAG_TO_REMOVE}' tag if Status is 'Draft' OR Age > {DAYS_THRESHOLD} days.")
    
    # Fetch products
    products = shopify_api.get_products_in_collection(COLLECTION_ID)
    if not products:
        print("No products found in collection or error fetching products.")
        return

    print(f"Found {len(products)} products in collection.")
    
    processed_count = 0
    updated_count = 0
    now = datetime.now(timezone.utc)
    
    for product in products:
        product_id = str(product['id'])
        title = product['title']
        status = product['status']
        created_at_str = product.get('created_at')
        tags_string = product.get('tags', '')
        
        # Parse date
        created_at = parse_shopify_date(created_at_str)
        age = now - created_at
        age_days = age.days
        
        # Parse tags into a list
        tags = [t.strip() for t in tags_string.split(',') if t.strip()]
        
        print(f"Checking: {title} (ID: {product_id})")
        print(f"  - Status: {status}")
        print(f"  - Age: {age_days} days (Created: {created_at_str})")
        
        should_remove = False
        reason = ""
        
        if status == 'draft':
            should_remove = True
            reason = "Status is Draft"
        elif age_days > DAYS_THRESHOLD:
            should_remove = True
            reason = f"Age ({age_days} days) > {DAYS_THRESHOLD} days"
        elif "high club" in title.lower():
            should_remove = True
            reason = "Is a High Club product"
        elif "rosin" in title.lower():
            should_remove = True
            reason = "Is a Rosin product"
        elif "hash" in title.lower():
            should_remove = True
            reason = "Is a Hash product"
            
        if should_remove:
            original_tag_count = len(tags)
            new_tags = [t for t in tags if t.lower() != TAG_TO_REMOVE.lower()]
            
            if len(new_tags) < original_tag_count:
                print(f"  - REMOVING TAG. Reason: {reason}")
                if shopify_api.update_product_tags(product_id, new_tags):
                    updated_count += 1
                else:
                    print("  - Failed to update tags.")
            else:
                print(f"  - Tag '{TAG_TO_REMOVE}' not found (already clean?)")
        else:
            print("  - KEEPING. Product is active and new enough.")
            
        processed_count += 1
        print("-" * 40)
        
    print(f"\nCleanup complete.")
    print(f"Processed: {processed_count}")
    print(f"Updated: {updated_count}")

if __name__ == "__main__":
    cleanup_new_strains()
