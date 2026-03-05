#!/usr/bin/env python3
"""
Verify image uploads for all updated products
"""

from shopify_api import get_product

products = {
    "9008376185044": "Black Patronus",
    "8876246728916": "Chocolope",
    "9008376774868": "Peach Jam",
    "8733300719828": "Superberry Crush",
    "9008378970324": "Orange Sherbet",
    "8598292037844": "Gelato Jealousy",
    "8899422945492": "Frosted Peaks",
    "7973895733460": "Blunicorn"
}

print("🚀 Verifying final image counts...")
print("="*80)

for pid, name in products.items():
    product = get_product(pid)
    if product:
        images = product.get('images', [])
        count = len(images)
        status = "✅" if count >= 1 else "❌"
        # Since we deleted old ones, we expect count usually to be 1, or just >0
        print(f"{status} {name} (ID: {pid}): {count} images")
        if count > 0:
            print(f"   Image: {images[0]['src']}")
    else:
        print(f"❌ {name}: Product not found!")

print("\n" + "="*80)
print("🏁 Verification complete!")
