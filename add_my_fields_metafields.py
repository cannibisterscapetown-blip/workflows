#!/usr/bin/env python3
"""
Add metafields to my_fields namespace for both products
"""

from shopify_api import create_or_update_metafield

# Products to update
products = {
    "Gelato Drops": {
        "id": "9008376086740",
        "metafields": {
            "lineage": "Sunset Sherbet x Thin Mint Girl Scout Cookies (legendary dessert hybrid from Cookie Fam)",
            "flowering_time": "8–9 weeks",
            "effects": "Euphoric • Relaxed • Creative • Happy • Balanced body-mind buzz",
            "breeder": "Cookie Fam Genetics x Sherbinskis (San Francisco origins)",
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
    }
}

for product_name, data in products.items():
    product_id = data["id"]
    metafields = data["metafields"]
    
    print(f"\n{'='*80}")
    print(f"🚀 Updating {product_name} (my_fields namespace)")
    print(f"   Product ID: {product_id}")
    print(f"{'='*80}\n")
    
    success_count = 0
    fail_count = 0
    
    for key, value in metafields.items():
        print(f"   Updating {key}...", end=" ")
        if create_or_update_metafield(product_id, "my_fields", key, value):
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1
    
    print(f"\n   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {fail_count}")

print(f"\n{'='*80}")
print("🎉 All updates complete!")
print(f"{'='*80}")
