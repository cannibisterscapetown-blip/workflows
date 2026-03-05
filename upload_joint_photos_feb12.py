#!/usr/bin/env python3
import os
import requests
import base64
from shopify_api import HEADERS, BASE_URL

# Standard image paths from previous configurations
IMAGE_PATHS = {
    "Normal Joint": "/Users/norton/.gemini/antigravity/brain/ac48112d-1734-466e-9d19-afb7eb85b105/uploaded_image_1767192210692.jpg",
    "Moonstick": "/Users/norton/.gemini/antigravity/brain/ac48112d-1734-466e-9d19-afb7eb85b105/uploaded_image_1767192229900.jpg"
}

PRODUCTS = {
    "9072664772820": "Normal Joint",  # Animal Tsunami Joint
    "8944913187028": "Moonstick",     # Animal Tsunami - Rosin Moonstick
    "8822549676244": "Moonstick",     # Astro Grape - Rosin Moonstick
    "8829780754644": "Moonstick"      # Afghan Kush Moonstick
}

def upload_photo(product_id, category):
    image_path = IMAGE_PATHS.get(category)
    if not image_path or not os.path.exists(image_path):
        print(f"❌ Image path for {category} not found: {image_path}")
        return False

    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')

    data = {
        "image": {
            "attachment": encoded_string,
            "filename": os.path.basename(image_path),
            "position": 1
        }
    }

    url = f"{BASE_URL}/products/{product_id}/images.json"
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        print(f"✅ Successfully uploaded {category} photo to {product_id}")
        return True
    else:
        print(f"❌ Failed to upload to {product_id}: {response.text}")
        return False

if __name__ == "__main__":
    for pid, cat in PRODUCTS.items():
        upload_photo(pid, cat)
