#!/usr/bin/env python3
"""
Update Gelato Drops metafields directly
"""

from shopify_api import create_or_update_metafield

# Product ID for Gelato Drops
product_id = "9008376086740"

# Metafields to update (using 'custom' namespace as seen in atomic_jelly)
metafields = {
    "lineage": "Sunset Sherbet x Thin Mint Girl Scout Cookies (legendary dessert hybrid from Cookie Fam)",
    "flowering_time": "8–9 weeks",
    "profile": "50/50 Balanced Hybrid",
    "height": "Medium",
    "stretch_percentage": "±30%",
    "average_thc_levels": "20–25%",
    "flavours": "Sweet berries, creamy vanilla, citrus sherbet, earthy mint",
    "effects": "Euphoric • Relaxed • Creative • Happy • Balanced body-mind buzz",
    "breeder": "Cookie Fam Genetics x Sherbinskis (San Francisco origins)",
    "used_for": "Creative sessions, social gatherings, balanced daytime-evening use, stress relief",
    "plant_characteristics": "Frosty purple-tinged buds • Sweet fruity aroma • Balanced hybrid structure",
    "plant_class": "Balanced Hybrid Flowering Plant",
    "plant_name": "Gelato Drops",
    "suitable_space": "Indoor or Greenhouse"
}

print("🚀 Updating Gelato Drops metafields...")
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
