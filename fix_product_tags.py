#!/usr/bin/env python3
"""
Fix tags for all four products - remove ratios and time-of-day, keep New Strains
"""

from shopify_api import update_product_description, get_product

products = {
    "Gelato Drops": {
        "id": "9008376086740",
        "tags": ["Hybrid", "Balanced", "Euphoric", "Creative", "Relaxed", "Happy", "Social", "Berry", "Sweet", "Creamy", "Citrus", "Stress Relief", "Cookie Fam", "Gelato", "New Strains"]
    },
    "Peachy Jam": {
        "id": "9008376774868",
        "tags": ["Hybrid", "Balanced", "Euphoric", "Uplifted", "Relaxed", "Happy", "Social", "Creative", "Peach", "Sweet", "Citrus", "Fruity", "Tropical", "Mood Elevation", "New Strains"]
    },
    "Black Patronus": {
        "id": "9008376185044",
        "tags": ["Indica", "Indica-Dominant", "Relaxed", "Euphoric", "Focused", "Uplifted", "Creative", "Coffee", "Berry", "Spicy", "Diesel", "Exotic Genetix", "Stress Relief", "Pain Relief", "New Strains"]
    },
    "Orange Sherbet": {
        "id": "9008378970324",
        "tags": ["Indica", "Indica-Dominant", "Relaxed", "Euphoric", "Happy", "Calm", "Orange", "Citrus", "Sweet", "Creamy", "Stress Relief", "Pain Relief", "Barney's Farm", "New Strains"]
    }
}

print("🏷️  Fixing tags for all products...")
print("   Removing: ratios (80/20, 60/40, 50/50) and time-of-day (Evening, Daytime)")
print("   Keeping: New Strains tag\n")
print("="*80)

for product_name, data in products.items():
    product_id = data["id"]
    tags = data["tags"]
    
    # Get current product to preserve description
    product = get_product(product_id)
    if not product:
        print(f"❌ {product_name}: Could not fetch product")
        continue
    
    print(f"\n📦 {product_name}")
    print(f"   New tags: {', '.join(tags)}")
    
    # Update with current description and new tags
    if update_product_description(product_id, product['body_html'], tags):
        print(f"   ✅ Tags updated")
    else:
        print(f"   ❌ Failed to update tags")

print(f"\n{'='*80}")
print("🎉 Tag updates complete!")
