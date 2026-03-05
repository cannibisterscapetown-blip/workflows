#!/usr/bin/env python3
"""
Update Montagu Snacks Metafields.
"""

from shopify_api import create_or_update_metafield
import sys

# Common "N/A" fields for snacks
COMMON_FIELDS = {
    "lineage": "N/A",
    "flowering_time": "N/A",
    "height": "N/A",
    "stretch_percentage": "N/A",
    "average_thc_levels": "N/A",
    "breeder": "Montagu"
}

PRODUCTS = {
    "9045387477204": { # Mango Fruit Flakes
        "name": "Mango Fruit Flakes",
        "fields": {
            "profile": "Dried Fruit Snack",
            "flavours": "Sweet Mango",
            "effects": "Natural Energy",
            "used_for": "Heathy snacking, Lunchboxes"
        }
    },
    "9045387542740": { # Raspberry & Beetroot
        "name": "Raspberry & Beetroot Fruit Cubes",
        "fields": {
            "profile": "Fruit & Veg Snack",
            "flavours": "Tangy Raspberry, Earthy Beetroot",
            "effects": "Natural Energy",
            "used_for": "Heathy snacking, On-the-go"
        }
    },
    "9045387575508": { # Mixed Tree Nuts
        "name": "Mixed Tree Nuts",
        "fields": {
            "profile": "Mixed Nuts",
            "flavours": "Natural Nutty, Roasted",
            "effects": "Satiety, Energy",
            "used_for": "Protein boost, Snacking"
        }
    }
}

def main():
    print("🚀 Updating Montagu Snacks Metafields...")
    print("=" * 60)
    
    for pid, data in PRODUCTS.items():
        print(f"📦 Processing {data['name']} (ID: {pid})...")
        
        # Merge common fields with specific fields
        metafields = {**COMMON_FIELDS, **data['fields']}
        
        success_count = 0
        for key, value in metafields.items():
            if create_or_update_metafield(pid, "my_fields", key, value):
                print(f"      ✅ Set {key}: {value}")
                success_count += 1
            else:
                print(f"      ❌ Failed to set {key}")
                
        print(f"   ✅ {success_count}/{len(metafields)} metafields updated")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
