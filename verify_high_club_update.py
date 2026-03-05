#!/usr/bin/env python3
import shopify_api

ids = [9062481985748, 9062480642260]

print("=== Verifying The High Club Vapes Updates (with Images) ===\n")

for pid in ids:
    product = shopify_api.get_product(str(pid))
    if product:
        print(f"ID: {pid}")
        print(f"Title: {product['title']}")
        images = product.get('images', [])
        print(f"Images count: {len(images)}")
        for img in images:
            print(f"  - Image ID: {img['id']}")
            print(f"    SRC: {img['src']}")
            
        if len(images) >= 3:
            print("✅ Images uploaded successfully.")
        else:
            print("⚠️  Warning: Less than 3 images found.")
            
        print("-" * 30)
    else:
        print(f"ID: {pid} NOT FOUND")
