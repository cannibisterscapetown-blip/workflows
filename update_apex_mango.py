#!/usr/bin/env python3
"""
Update Apex and Mango Tango strains.
"""

from shopify_api import update_product_description, create_or_update_metafield
import sys

PRODUCTS = [
    {
        "id": "9047076569300",
        "title": "Apex",
        "description": "Apex is a balanced hybrid strain (50/50) bred by Ethos Genetics, crossing Mandarin Cookies with Lilac Diesel BX3. It delivers a powerful, tingly high that starts with euphoria and settles into deep relaxation. The flavor profile is complex, mixing sweet and sour citrusy candy notes with spicy earth and diesel undertones.",
        "tags": ["New Strains", "Flower", "Hybrid", "Apex", "Relaxed", "Tingly", "Citrus", "Diesel"],
        "metafields": {
            "lineage": "Mandarin Cookies x Lilac Diesel BX3",
            "flowering_time": "9 weeks",
            "profile": "Balanced Hybrid (50/50)",
            "height": "Medium",
            "stretch_percentage": "±150%",
            "average_thc_levels": "24%",
            "flavours": "Sweet Citrus, Berry, Spicy Earth, Diesel",
            "effects": "Relaxed • Tingly • Happy • Euphoric • Hungry",
            "used_for": "Stress relief, appetite stimulation, relaxation",
            "breeder": "Ethos Genetics"
        }
    },
    {
        "id": "9047076438228",
        "title": "Mango Tango",
        "description": "Mango Tango is an indica-dominant hybrid (70/30) known for its delicious tropical flavor. A cross between True OG and Tangie, this strain offers a pungent aroma of ripe mango and pine. The effects are uplifting and euphoric, gradually giving way to a calming body high that can be sleepy in higher doses.",
        "tags": ["New Strains", "Flower", "Indica Dominant Hybrid", "Mango Tango", "Fruity", "Relaxed", "Sleepy"],
        "metafields": {
            "lineage": "True OG x Tangie",
            "flowering_time": "8-9 weeks",
            "profile": "Indica Dominant Hybrid (70/30)",
            "height": "Medium",
            "stretch_percentage": "±150%",
            "average_thc_levels": "22%",
            "flavours": "Ripe Mango, Citrus, Pine, Sweet Fruit",
            "effects": "Relaxed • Euphoric • Happy • Uplifted • Sleepy",
            "used_for": "Evening relaxation, mood elevation, sleep aid",
            "breeder": "Elemental Seeds"
        }
    }
]

def main():
    print("🚀 Updating Apex and Mango Tango...")
    print("=" * 60)
    
    for p in PRODUCTS:
        print(f"📦 Processing {p['title']} (ID: {p['id']})...")
        
        # 1. Update Description and Tags
        # Prepend Profile text directly in bold
        profile_text = p['metafields']['profile']
        full_description = f"<strong>{profile_text}</strong><br><br>{p['description']}"
        
        print(f"   Updating Description & Tags...")
        if update_product_description(p['id'], full_description, p['tags']):
            print(f"   ✅ Description & Tags updated")
        else:
            print(f"   ❌ Failed to update Description & Tags")

        # 2. Update Metafields
        print(f"   Updating metafields...")
        mf_success_count = 0
        for key, value in p['metafields'].items():
            if create_or_update_metafield(p['id'], "my_fields", key, value):
                mf_success_count += 1
                print(f"      ✅ Set {key}")
            else:
                print(f"      ❌ Failed on {key}")
                
        print(f"   ✅ {mf_success_count}/{len(p['metafields'])} metafields updated")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("🎉 Finished!")

if __name__ == "__main__":
    main()
