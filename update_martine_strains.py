#!/usr/bin/env python3
"""
Update Domestic Disturbance, Blue Caviar, and Obsession.
"""

from shopify_api import update_product_description, create_or_update_metafield
import sys

PRODUCTS = [
    {
        "id": "9049870008532",
        "title": "Domestic Disturbance",
        "description": "Domestic Disturbance is a potent indica-dominant hybrid bred by Humboldt CSI, crossing Family Feud with the Ruthless Runtz cut. This strain delivers a profound, soothing body high that melts away stress and tension, making it ideal for evening relaxation. The flavor profile features sweet, candy-like notes with earthy and spicy undertones.",
        "tags": ["New Strains", "Flower", "Indica Dominant Hybrid", "Domestic Disturbance", "Relaxed", "Sedated", "Candy", "Earthy"],
        "metafields": {
            "lineage": "Family Feud x Ruthless Runtz",
            "flowering_time": "8-9 weeks",
            "profile": "Indica Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±150%",
            "average_thc_levels": "22%",
            "flavours": "Sweet Candy, Earthy, Spicy",
            "effects": "Soothing • Sedated • Calm • Happy",
            "used_for": "Evening relaxation, stress relief, sleep aid",
            "breeder": "Humboldt CSI"
        }
    },
    {
        "id": "9049869353172",
        "title": "Blue Caviar",
        "description": "Blue Caviar is a rich indica-dominant strain known for its deep relaxation and complex flavor profile. With lineage tracing back to Grape Rhino and Lantz/Grape Gas, it offers a luxurious blend of grape, berry, and dark chocolate notes. The effects are calming and euphoric, perfect for melting into the couch and finding relief from stress.",
        "tags": ["New Strains", "Flower", "Indica Dominant", "Blue Caviar", "Fruity", "Relaxed", "Grape", "Berry"],
        "metafields": {
            "lineage": "Lantz x Grape Gas",
            "flowering_time": "8-9 weeks",
            "profile": "Indica Dominant",
            "height": "Medium",
            "stretch_percentage": "±100%",
            "average_thc_levels": "24%",
            "flavours": "Grape, Berry, Dark Chocolate, Earthy",
            "effects": "Relaxed • Euphoric • Sleepy • Stress Relief",
            "used_for": "De-stressing, mood elevation, deep relaxation",
            "breeder": "Unknown" 
        }
    },
    {
        "id": "9049868796116",
        "title": "Obsession",
        "description": "Obsession is a classic indica-dominant hybrid that combines the best of Cinderella 99 and Matanuska Thunder. It features a sweet, fruity aroma with hints of pine and skunk. The high provides a balanced mix of cerebral euphoria and deep physical relaxation, often leading to a peaceful, sleepy state.",
        "tags": ["New Strains", "Flower", "Indica Dominant Hybrid", "Obsession", "Sleepy", "Relaxed", "Sweet"],
        "metafields": {
            "lineage": "Cinderella 99 x Matanuska Thunder",
            "flowering_time": "8-9 weeks",
            "profile": "Indica Dominant Hybrid (60/40)",
            "height": "Medium",
            "stretch_percentage": "±150%",
            "average_thc_levels": "20%",
            "flavours": "Sweet Fruit, Pine, Skunky, Spicy",
            "effects": "Relaxed • Sleepy • Happy • Euphoric",
            "used_for": "Insomnia relief, pain management, unwinding",
            "breeder": "World of Seeds / Various"
        }
    }
]

def main():
    print("🚀 Updating 3 New Strains...")
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
