#!/usr/bin/env python3
"""
Update 4 New Products (Rosin & Joints) on Shopify.
Created on Feb 02, 2026.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

# Product Data Configuration
PRODUCTS = {
    "9059481419988": { # Indoor Flower Rosin - Girl Scout Cookies
        "title": "Indoor Flower Rosin - Girl Scout Cookies",
        "description": "Girl Scout Cookies (GSC) is an award-winning hybrid famous for its sweet, earthy, and minty aroma. This premium rosin captures the essence of the strain, delivering a powerful, long-lasting euphoria that melts into deep relaxation—perfect for stress relief and appetite stimulation.",
        "tags": ["Rosin", "Concentrate", "Hybrid", "50/50", "Relaxed", "Euphoric", "Happy", "Hungry", "Sweet", "Earthy", "Mint", "Chocolate", "Stress Relief", "Appetite", "New Strains"],
        "metafields": {
            "lineage": "OG Kush x Durban Poison",
            "flowering_time": "9-10 weeks",
            "profile": "50/50 Hybrid",
            "height": "Medium",
            "stretch_percentage": "±30%",
            "average_thc_levels": "20–28%", # High for Rosin context, but strain generic
            "flavours": "Sweet, Earthy, Mint, Chocolate",
            "effects": "Euphoric • Relaxed • Happy • Hungry",
            "used_for": "Stress relief, appetite loss, pain management, deep relaxation",
            "breeder": "Cookie Family (classic genetics)"
        }
    },
    "9059463594196": { # Canni Ltd Edition Joint - Supercheese
        "title": "Canni Ltd Edition Joint - Supercheese",
        "description": "Supercheese lives up to its name with a pungent, cheesy aroma and deep skunky undertones. This solid indica offers a steady, feel-good high that relaxes the body while keeping the mind happy—an excellent choice for evening recovery and fighting stress.",
        "tags": ["Joint", "Pre-roll", "Indica", "Indica-Dominant", "75/25", "Relaxed", "Happy", "Euphoric", "Sleepy", "Cheese", "Skunk", "Earthy", "Stress Relief", "Pain Relief", "New Strains"],
        "metafields": {
            "lineage": "Cheese x Cheese (Old School Genetics)",
            "flowering_time": "8-9 weeks",
            "profile": "75/25 Indica",
            "height": "Short-Medium",
            "stretch_percentage": "±25%",
            "average_thc_levels": "18–22%",
            "flavours": "Cheese, Skunk, Earthy, Creamy",
            "effects": "Relaxed • Happy • Euphoric • Sleepy",
            "used_for": "Stress relief, insomnia, pain management, relaxation",
            "breeder": "Unknown (Classic Strain)"
        }
    },
    "9059463004372": { # Canni Ltd Edition Joint - Elvis
        "title": "Canni Ltd Edition Joint - Elvis",
        "description": "Elvis is a high-energy sativa that gets you moving with a burst of creative euphoria. Combining sweet, earthy notes with a skunky kick, this strain is perfect for daytime activities, sparking conversation, or fueling artistic projects.",
        "tags": ["Joint", "Pre-roll", "Sativa", "Sativa-Dominant", "75/25", "Energetic", "Creative", "Uplifted", "Focused", "Sweet", "Earthy", "Skunk", "Diesel", "Daytime", "New Strains"],
        "metafields": {
            "lineage": "AK-47 x Skunk #1",
            "flowering_time": "8-9 weeks",
            "profile": "75/25 Sativa",
            "height": "Tall",
            "stretch_percentage": "±40%",
            "average_thc_levels": "22–26%",
            "flavours": "Sweet, Earthy, Skunk, Diesel",
            "effects": "Energetic • Creative • Uplifted • Focused",
            "used_for": "Daytime energy, creative focus, mood enhancement",
            "breeder": "Seedism Seeds"
        }
    },
    "9059462545620": { # Canni Ltd Edition Joint - Sour Diesel
        "title": "Canni Ltd Edition Joint - Sour Diesel",
        "description": "Sour Diesel is a legendary sativa known for its fast-acting, energizing head high and unmistakable pungent diesel aroma. Perfect for waking and baking or a mid-day boost, it clears the mind and powers you through tasks with focus and elevated mood.",
        "tags": ["Joint", "Pre-roll", "Sativa", "Sativa-Dominant", "70/30", "Energetic", "Focused", "Uplifted", "Happy", "Diesel", "Fuel", "Earthy", "Citrus", "Daytime", "New Strains"],
        "metafields": {
            "lineage": "Chemdawg x Super Skunk",
            "flowering_time": "10-11 weeks",
            "profile": "70/30 Sativa",
            "height": "Tall",
            "stretch_percentage": "±50%",
            "average_thc_levels": "20–25%",
            "flavours": "Diesel, Fuel, Earthy, Pungent Citrus",
            "effects": "Energetic • Focused • Uplifted • Happy",
            "used_for": "Fatigue, stress, depression, lack of focus",
            "breeder": "Unknown (Classic Strain)"
        }
    }
}

def main():
    print("🚀 Updating Martine's New Products (Feb 02)...")
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
        # Construct HTML description with bold profile at the top
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
