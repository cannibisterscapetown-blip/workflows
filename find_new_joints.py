#!/usr/bin/env python3
import shopify_api
import re

def find_new_joints():
    print("🔍 Fetching latest products (Active & Draft)...")
    products = shopify_api.list_products(limit=15, status='active')
    drafts = shopify_api.list_products(limit=15, status='draft')
    
    all_products = products + drafts
    # Sort by created_at descending
    all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    print(f"\nFound {len(all_products)} recent products. Filtering for 'Joint'...")
    
    count = 0
    for p in all_products:
        if 'joint' in p['title'].lower():
            count += 1
            print(f"\n[{count}] ID: {p['id']}")
            print(f"Title: {p['title']}")
            print(f"Status: {p['status']}")
            print(f"Created: {p['created_at']}")
            print(f"Description (HTML): {p.get('body_html', '')[:200]}...") # Print first 200 chars
            print(f"Tags: {p.get('tags')}")
            print("-" * 40)
            
            if count >= 5: break

if __name__ == "__main__":
    find_new_joints()
