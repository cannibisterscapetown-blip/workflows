#!/usr/bin/env python3
"""
Upload images for Karamel Cut Throat and Mango Tango.
"""

from shopify_api import upload_product_image
import os

UPDATES = [
    {
        "id": "8658724651220",
        "name": "Karamel Cut Throat",
        "image": "karamel_cut_throat.png"
    },
    {
        "id": "9047076438228",
        "name": "Mango Tango",
        "image": "mango_tango.png"
    },
    {
        "id": "9047076569300",
        "name": "Apex",
        "image": "apex.png"
    }
]

def main():
    print("🚀 Uploading images...")
    print("=" * 60)

    for item in UPDATES:
        print(f"📸 Uploading for {item['name']} (ID: {item['id']})...")
        if not os.path.exists(item['image']):
            print(f"   ❌ Image file not found: {item['image']}")
            continue
            
        if upload_product_image(item['id'], item['image']):
             print(f"   ✅ Success")
        else:
             print(f"   ❌ Failed")

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
