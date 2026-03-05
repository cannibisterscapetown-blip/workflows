#!/usr/bin/env python3
"""
Update Peachy Jam metafields directly
"""

from shopify_api import create_or_update_metafield

# Product ID for Peachy Jam
product_id = "9008376774868"

# Metafields to update (using 'custom' namespace)
metafields = {
    "lineage": "Traffic Jam x Peach Crescendo (peachy-sweet hybrid; balanced genetics)",
    "flowering_time": "8–9 weeks",
    "profile": "50/50 Balanced Hybrid",
    "height": "Medium",
    "stretch_percentage": "±35%",
    "average_thc_levels": "20–24%",
    "flavours": "Ripe peaches, sweet citrus, tropical fruit, earthy undertones",
    "effects": "Euphoric • Relaxed • Uplifted • Happy • Balanced mind-body harmony",
    "breeder": "Genetic Avenue (Traffic Jam x Peach Crescendo cross)",
    "used_for": "Social gatherings, creative sessions, mood elevation, balanced relaxation",
    "plant_characteristics": "Dense resinous buds • Sweet peachy aroma • Balanced hybrid structure",
    "plant_class": "Balanced Hybrid Flowering Plant",
    "plant_name": "Peachy Jam",
    "suitable_space": "Indoor or Greenhouse"
}

print("🚀 Updating Peachy Jam metafields...")
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
