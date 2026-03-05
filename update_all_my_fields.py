#!/usr/bin/env python3
"""
Update all three products with my_fields namespace metafields
"""

from shopify_api import create_or_update_metafield

# Products to update
products = {
    "Gelato Drops": {
        "id": "9008376086740",
        "metafields": {
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
        }
    },
    "Peachy Jam": {
        "id": "9008376774868",
        "metafields": {
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
        }
    },
    "Black Patronus": {
        "id": "9008376185044",
        "metafields": {
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
        }
    }
}

print("🚀 Updating all products with my_fields namespace metafields...")
print("="*80)

for product_name, data in products.items():
    product_id = data["id"]
    metafields = data["metafields"]
    
    print(f"\n📦 {product_name} (ID: {product_id})")
    print("-"*80)
    
    success_count = 0
    fail_count = 0
    
    for key, value in metafields.items():
        print(f"   {key}...", end=" ")
        if create_or_update_metafield(product_id, "my_fields", key, value):
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1
    
    print(f"\n   ✅ Successful: {success_count} | ❌ Failed: {fail_count}")

print(f"\n{'='*80}")
print("🎉 All products updated!")
print(f"{'='*80}")
