#!/usr/bin/env python3
"""
Update Black Patronus metafields directly
"""

from shopify_api import create_or_update_metafield

# Product ID for Black Patronus
product_id = "9008376185044"

# Metafields to update (using 'custom' namespace)
metafields = {
    "lineage": "Rainbow Sherbet #11 (RS-11) x Falcon 9 (Exotic Genetix creation)",
    "flowering_time": "8–9 weeks",
    "profile": "60/40 Indica-Dominant Hybrid",
    "height": "Medium",
    "stretch_percentage": "±35%",
    "average_thc_levels": "24–28%",
    "flavours": "Spicy black coffee, fruity anise, sweet berries, peppery diesel, chocolate",
    "effects": "Relaxed • Euphoric • Focused • Uplifted • Creative",
    "breeder": "Exotic Genetix (Washington-based breeder)",
    "used_for": "Evening relaxation, stress relief, creative focus, pain management",
    "plant_characteristics": "Dense frosty buds • Spicy coffee-berry aroma • Indica-leaning structure",
    "plant_class": "Indica-dominant Flowering Plant",
    "plant_name": "Black Patronus",
    "suitable_space": "Indoor or Greenhouse"
}

print("🚀 Updating Black Patronus metafields...")
print(f"   Product ID: {product_id}\n")

success_count = 0
fail_count = 0

for key, value in metafields.items():
    print(f"   Updating {key}...", end=" ")
    if create_or_update_metafield(product_id, "custom", key, value):
        print("✅")
        success_count += 1
    else:
        print("❌")
        fail_count += 1

print(f"\n📊 Results:")
print(f"   ✅ Successful: {success_count}")
print(f"   ❌ Failed: {fail_count}")

if fail_count == 0:
    print(f"\n🎉 All metafields updated successfully!")
    print(f"   View product: https://admin.shopify.com/store/cannibisters/products/{product_id}")
else:
    print(f"\n⚠️  Some metafields failed to update.")
