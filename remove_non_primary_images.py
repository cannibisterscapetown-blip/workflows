#!/usr/bin/env python3
"""
Remove all non-primary images (position > 1) from joint products.
Targets categories: Normal Joints and Moonsticks.
"""

import requests
import json
from shopify_api import HEADERS, BASE_URL

def delete_secondary_images(product_id: str):
    """Fetch all images for a product and delete those with position > 1"""
    try:
        # Get all images for the product
        response = requests.get(f'{BASE_URL}/products/{product_id}/images.json', headers=HEADERS)
        response.raise_for_status()
        images = response.json().get('images', [])
        
        if not images:
            print(f"   ℹ️ No images found for {product_id}")
            return
            
        # Filter for images where position > 1
        to_delete = [img for img in images if img['position'] > 1]
        
        if not to_delete:
            print(f"   ✅ No secondary images to delete for {product_id}")
            return
            
        print(f"   🗑️ Deleting {len(to_delete)} secondary images for {product_id}...")
        for img in to_delete:
            img_id = img['id']
            try:
                del_resp = requests.delete(
                    f'{BASE_URL}/products/{product_id}/images/{img_id}.json',
                    headers=HEADERS
                )
                del_resp.raise_for_status()
                print(f"      ✅ Deleted image {img_id}")
            except Exception as e:
                print(f"      ❌ Failed to delete image {img_id}: {e}")
                
    except Exception as e:
        print(f"   ❌ Error processing product {product_id}: {e}")

def main():
    print("🧹 Starting cleanup of non-primary images...")
    print("=" * 60)
    
    # Load categories
    try:
        with open('joint_categories.json', 'r') as f:
            categories = json.load(f)
    except Exception as e:
        print(f"❌ Error loading joint_categories.json: {e}")
        return

    # Targeting Normal Joints and Moonsticks
    target_cats = ["Normal Joints", "Moonsticks"]
    
    for cat in target_cats:
        products = categories.get(cat, [])
        print(f"\n📂 Processing Category: {cat} ({len(products)} products)")
        
        for p in products:
            pid = p['id']
            title = p['title']
            print(f"   🔍 Product: {title} ({pid})")
            delete_secondary_images(pid)

    print("\n" + "=" * 60)
    print("🎉 Cleanup complete!")

if __name__ == "__main__":
    main()
