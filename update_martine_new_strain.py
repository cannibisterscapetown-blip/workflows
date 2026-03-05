#!/usr/bin/env python3
"""
Update Chocolope (Martine New Strain)
Created on Feb 09, 2026.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product

# Product Data Configuration
PRODUCTS = {
    "9068135481556": { # Chocolope - Cannibisters Limited Collection
        "title": "Chocolope - Cannibisters Limited Collection",
        "description": "Indulge in the rich, nostalgic flavors of Chocolope. <br><br><strong>50/50 Hybrid</strong><br><br>This balanced strain delivers a delightful fusion of earthy coffee and sweet melon, underpinned by deep chocolate notes. Known for its dreamy, cerebral high, Chocolope offers a smooth lift that sparks creativity and happy euphoria without heavy sedation.<br><br>Perfect for a morning pick-me-up or an afternoon creative session.",
        "tags": ["Chocolope", "Hybrid", "50/50", "Coffee", "Chocolate", "Sweet", "Melon", "Earthy", "Euphoric", "Happy", "Creative", "Limited Collection", "New Strains", "Cannibisters Limited Collection"],
        "metafields": {
            "lineage": "Chocolate Thai x Cannalope Haze",
            "flowering_time": "9-10 Weeks",
            "profile": "50/50 Hybrid",
            "height": "Tall",
            "stretch_percentage": "High (200%)",
            "average_thc_levels": "18-22%",
            "flavours": "Coffee, Dark Chocolate, Earthy, Sweet Melon",
            "effects": "Euphoric • Happy • Creative • Energetic",
            "used_for": "Depression, stress, fatigue, lack of appetite",
            "breeder": "DNA Genetics (Lineage)"
        }
    }
}

def main():
    print("🚀 Updating Chocolope (Feb 09)...")
    print("=" * 60)

    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing {data['title']} (ID: {pid})...")
        
        # Verify product exists
        product = get_product(pid)
        if not product:
            print(f"   ❌ Product not found! Skipping...")
            continue
            
        # 1. Update Description and Tags
        # Prepend profile to description if not already there (it is in my string)
        full_description = data['description']
        
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
