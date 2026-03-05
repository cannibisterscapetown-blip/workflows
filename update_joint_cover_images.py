#!/usr/bin/env python3
"""
Update cover images for joint products based on their category.
Sets the new image to position: 1.
"""

import os
import base64
import requests
import json
from shopify_api import HEADERS, BASE_URL

# Paths to the uploaded feature images
IMAGE_PATHS = {
    "Normal Joints": "/Users/norton/.gemini/antigravity/brain/ac48112d-1734-466e-9d19-afb7eb85b105/uploaded_image_1767192210692.jpg",
    "Moonsticks": "/Users/norton/.gemini/antigravity/brain/ac48112d-1734-466e-9d19-afb7eb85b105/uploaded_image_1767192229900.jpg",
    "Super Joints": "/Users/norton/.gemini/antigravity/brain/ac48112d-1734-466e-9d19-afb7eb85b105/uploaded_image_1767191356385.jpg"
}

def upload_cover_image(product_id: str, image_path: str) -> bool:
    """Upload an image and set it as position 1 (cover)"""
    try:
        if not os.path.exists(image_path):
            print(f"   ❌ Image not found: {image_path}")
            return False
            
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
        filename = os.path.basename(image_path)
        
        data = {
            "image": {
                "attachment": encoded_string,
                "filename": filename,
                "position": 1
            }
        }
        
        response = requests.post(
            f'{BASE_URL}/products/{product_id}/images.json',
            headers=HEADERS,
            json=data
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"   ❌ Error updating {product_id}: {e}")
        return False

def main():
    print("🖼️ Starting update of joint cover images...")
    print("=" * 60)
    
    # Load categories
    try:
        with open('joint_categories.json', 'r') as f:
            categories = json.load(f)
    except Exception as e:
        print(f"❌ Error loading joint_categories.json: {e}")
        return

    for category, products in categories.items():
        image_path = IMAGE_PATHS.get(category)
        if not image_path:
            print(f"⚠️ No image defined for category: {category}")
            continue
            
        print(f"\n📂 Category: {category} ({len(products)} products)")
        print(f"🖼️ Cover Image: {os.path.basename(image_path)}")
        
        for p in products:
            pid = p['id']
            name = p['title']
            print(f"   ⬆️ Setting cover for {name} ({pid})...", end="", flush=True)
            if upload_cover_image(pid, image_path):
                print(" ✅ Success")
            else:
                print(" ❌ Failed")

    print("\n" + "=" * 60)
    print("🎉 All cover image updates complete!")

if __name__ == "__main__":
    main()
