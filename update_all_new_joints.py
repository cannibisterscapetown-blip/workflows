#!/usr/bin/env python3
"""
Update Canni Papa Smurf, Chocolope, Astro Grape, and Ltd Joints.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

PRODUCTS = {
    "9039335981268": { # Papa Smurf
        "title": "Canni Papa Smurf Joint",
        "description": "Papa Smurf is an uplifting hybrid crossing Blue Dream and Cotton Candy. Expect a burst of sweet blueberry and pine flavours with a giggly, happy high that settles into distinct relaxation.",
        "tags": ["Joint", "Pre-roll", "Hybrid", "Sativa Dominant", "Papa Smurf", "Uplifting", "Berry"],
        "metafields": {
            "lineage": "Blue Dream x Cotton Candy",
            "flowering_time": "8–9 weeks", # Estimated standard
            "profile": "Sativa-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±40%",
            "average_thc_levels": "20–24%",
            "flavours": "Blueberry, Berry, Pine, Sweet",
            "effects": "Uplifted • Giggly • Relaxed • Happy",
            "used_for": "Socializing, mood boost, daytime relaxation",
            "breeder": "Atlas Seed"
        }
    },
    "9039335817428": { # Chocolope
        "title": "Canni Chocolope Joint",
        "description": "Chocolope is a legendary sativa classic, blending Chocolate Thai with Cannalope Haze for a nostalgic, cocoa-rich experience. This joint delivers a clear-headed, energetic buzz perfect for creativity.",
        "tags": ["Joint", "Pre-roll", "Sativa", "Chocolope", "Creative", "Energizing", "Cocoa"],
        "metafields": {
            "lineage": "Chocolate Thai x Cannalope Haze",
            "flowering_time": "9–10 weeks",
            "profile": "95/5 Sativa-Dominant Hybrid",
            "height": "Tall",
            "stretch_percentage": "±60%",
            "average_thc_levels": "18–22%",
            "flavours": "Roasted coffee, dark cocoa, sweet haze, earthy spice",
            "effects": "Creative • Energetic • Uplifted • Happy • Focused",
            "used_for": "Daytime productivity, creative focus, morning motivation",
             "breeder": "DNA Genetics"
        }
    },
    "9039335522516": { # Astro Grape
        "title": "Canni Astro Grape Joint",
        "description": "Astro Grape combines Grape Pie and Jet Fuel Gelato for a heavy hitting indica-dominant experience. Bursting with sweet grape candy and pungent gas, this joint offers deep relaxation and a dreamy euphoria.",
        "tags": ["Joint", "Pre-roll", "Indica", "Astro Grape", "Relaxed", "Grape", "Gas"],
        "metafields": {
            "lineage": "Grape Pie x Jet Fuel Gelato",
            "flowering_time": "8–9 weeks",
            "profile": "75/25 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "24–28%",
            "flavours": "Sweet grape candy, pungent gas, creamy berry, tart citrus",
            "effects": "Euphoric • Relaxed • Dreamy • Calm • Heavy body buzz",
            "used_for": "Evening wind-down, anxiety relief, insomnia",
            "breeder": "Unknown" # Sourced from flower data
        }
    },
    "9039335129300": { # Ltd Joint
        "title": "Canni Ltd Joint",
        "description": "A special Limited Edition pre-roll from Cannibisters. This exclusive joint features a curated selection of our finest genetics.",
        "tags": ["Joint", "Pre-roll", "Limited Edition", "Mystery", "Exclusive"],
        "metafields": {
            "lineage": "Top Secret Genetics",
            "flowering_time": "N/A",
            "profile": "Hybrid",
            "height": "N/A",
            "stretch_percentage": "N/A",
            "average_thc_levels": "High",
            "flavours": "Mystery Profile, Exclusive",
            "effects": "Potent • Surprising • Premium",
            "used_for": "Special Occasions, Connoisseurs",
             "breeder": "Cannibisters"
        }
    }
}

def main():
    print("🚀 Updating New Joint Products...")
    print("=" * 60)

    for pid, data in PRODUCTS.items():
        print(f"\n📦 Processing {data['title']} (ID: {pid})...")
        
        # 1. Update Description and Tags
        profile_text = data['metafields'].get('profile', '')
        full_description = f"<strong>{profile_text}</strong><br><br>{data['description']}"
        
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
