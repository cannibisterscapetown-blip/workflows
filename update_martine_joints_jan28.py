#!/usr/bin/env python3
"""
Update Orange Sherbet Joint and Black Patronus Joint on Shopify.
Created on Jan 28, 2026.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

PRODUCTS = {
    "9055138283732": { # Orange Sherbet Joint
        "title": "Orange Sherbet Joint",
        "description": "Orange Sherbet delivers a sweet burst of orange candy and fresh citrus with creamy tangerine notes. This Barney's Farm creation offers deeply relaxing euphoria perfect for unwinding—ideal for evening stress relief and peaceful calm.",
        "tags": ["Joint", "Pre-roll", "Indica", "Indica-Dominant", "80/20", "Relaxed", "Euphoric", "Happy", "Calm", "Evening", "Orange", "Citrus", "Sweet", "Creamy", "Stress Relief", "Pain Relief", "Barney's Farm", "New Strains"],
        "metafields": {
            "lineage": "Orange Cream x Purple Urkle x Cherry Pie (sweet citrus indica blend)",
            "flowering_time": "9–10 weeks",
            "profile": "80/20 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±30%",
            "average_thc_levels": "22–24%",
            "flavours": "Sweet orange candy, fresh citrus, creamy tangerine, earthy pine",
            "effects": "Relaxed • Euphoric • Happy • Calm • Uplifted",
            "used_for": "Evening relaxation, stress relief, pain management, anxiety relief",
            "breeder": "Barney's Farm (premium genetics)"
        }
    },
    "9055138545876": { # Black Patronus Joint
        "title": "Black Patronus Joint",
        "description": "Black Patronus blends spicy black coffee, fruity anise, and sweet berries with peppery diesel notes. This Exotic Genetix creation delivers a harmonious balance of deep relaxation and focused euphoria—perfect for evening unwinding with creative clarity.",
        "tags": ["Joint", "Pre-roll", "Indica", "Indica-Dominant", "60/40", "Relaxed", "Euphoric", "Focused", "Uplifted", "Creative", "Evening", "Coffee", "Berry", "Spicy", "Diesel", "Exotic Genetix", "Stress Relief", "Pain Relief", "New Strains"],
        "metafields": {
            "lineage": "Rainbow Sherbet #11 (RS-11) x Falcon 9 (Exotic Genetix creation)",
            "flowering_time": "8–9 weeks",
            "profile": "60/40 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "24–28%",
            "flavours": "Spicy black coffee, fruity anise, sweet berries, peppery diesel, chocolate",
            "effects": "Relaxed • Euphoric • Focused • Uplifted • Creative",
            "used_for": "Evening relaxation, stress relief, creative focus, pain management",
            "breeder": "Exotic Genetix (Washington-based breeder)"
        }
    }
}

def main():
    print("🚀 Updating Martine's New Joints...")
    print("=" * 60)

    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing {data['title']} (ID: {pid})...")
        
        # Verify product exists
        product = get_product(pid)
        if not product:
            print(f"   ❌ Product not found! Skipping...")
            continue
            
        # 1. Update Description and Tags
        profile_text = data['metafields'].get('profile', '')
        full_description = f"<strong>{profile_text}</strong><br><br>{data['description'].strip()}"
        
        print(f"   Updating Description & Tags...")
        if update_product_description(pid, full_description, data['tags']):
             print(f"   ✅ Description & Tags updated")
        else:
             print(f"   ❌ Failed to update Description & Tags")
             
        # 2. Update Metafields
        print(f"   Updating metafields...")
        mf_success_count = 0
        for key, value in data['metafields'].items():
            if create_or_update_metafield(pid, "my_fields", key, value):
                mf_success_count += 1
                print(f"      ✅ Set {key}")
            else:
                print(f"      ❌ Failed on {key}")
        print(f"   ✅ {mf_success_count}/{len(data['metafields'])} metafields updated")

    print("\n" + "=" * 60)
    print("🎉 All updates finished!")

if __name__ == "__main__":
    main()
