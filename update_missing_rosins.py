#!/usr/bin/env python3
"""
Update 3 Missing Rosin Products on Shopify.
Created on Feb 02, 2026.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

# Product Data Configuration
PRODUCTS = {
    "9059476242644": { # Indoor Flower Rosin - Elvis
        "title": "Indoor Flower Rosin - Elvis",
        "description": "Elvis Rosin concentrates the high-energy spirit of its namesake into a potent, golden extraction. With sweet, earthy notes and a skunky kick, this sativa-dominant concentrate delivers a burst of creative euphoria perfect for daytime focus and artistic inspiration.",
        "tags": ["Rosin", "Concentrate", "Sativa", "Sativa-Dominant", "75/25", "Energetic", "Creative", "Uplifted", "Focused", "Sweet", "Earthy", "Skunk", "Daytime", "New Strains"],
        "metafields": {
            "lineage": "AK-47 x Skunk #1",
            "flowering_time": "8-9 weeks",
            "profile": "75/25 Sativa",
            "height": "Tall",
            "stretch_percentage": "±40%",
            "average_thc_levels": "22–28%", # Potent for Rosin
            "flavours": "Sweet, Earthy, Skunk, Diesel",
            "effects": "Energetic • Creative • Uplifted • Focused",
            "used_for": "Daytime energy, creative focus, mood enhancement",
            "breeder": "Seedism Seeds"
        }
    },
    "9059471425748": { # Indoor Flower Rosin - Super Cheese
        "title": "Indoor Flower Rosin - Super Cheese",
        "description": "Super Cheese Rosin captures the essence of the classic strain in a pure, solventless form. Expect a pungent, cheesy aroma with deep skunky undertones. This indica-heavy concentrate offers steady, feel-good relaxation that soothes the body while keeping the mind happy.",
        "tags": ["Rosin", "Concentrate", "Indica", "Indica-Dominant", "75/25", "Relaxed", "Happy", "Euphoric", "Sleepy", "Cheese", "Skunk", "Earthy", "Stress Relief", "Pain Relief", "New Strains"],
        "metafields": {
            "lineage": "Cheese x Cheese (Old School Genetics)",
            "flowering_time": "8-9 weeks",
            "profile": "75/25 Indica",
            "height": "Short-Medium",
            "stretch_percentage": "±25%",
            "average_thc_levels": "20–25%",
            "flavours": "Cheese, Skunk, Earthy, Creamy",
            "effects": "Relaxed • Happy • Euphoric • Sleepy",
            "used_for": "Stress relief, insomnia, pain management, relaxation",
            "breeder": "Unknown (Classic Strain)"
        }
    },
    "9059468574932": { # Indoor Flower Rosin - Blue Cheese
        "title": "Indoor Flower Rosin - Blue Cheese",
        "description": "Blue Cheese Rosin is a gourmet concentrate blending sweet berry notes with a savory, creamy finish. This indica-dominant extract is renowned for its deeply relaxing effects, melting away stress and tension while delivering a euphoric, peaceful state of mind.",
        "tags": ["Rosin", "Concentrate", "Indica", "Indica-Dominant", "75/25", "Relaxed", "Sleepy", "Euphoric", "Happy", "Blue Cheese", "Berry", "Earthy", "Creamy", "Stress Relief", "Insomnia", "New Strains"],
        "metafields": {
            "lineage": "Blueberry x UK Cheese",
            "flowering_time": "8-9 weeks",
            "profile": "75/25 Indica",
            "height": "Short-Medium",
            "stretch_percentage": "±25%",
            "average_thc_levels": "20–25%",
            "flavours": "Blue Cheese, Sweet Berry, Earthy, Creamy",
            "effects": "Relaxed • Sleepy • Euphoric • Happy",
            "used_for": "Insomnia, stress, pain, muscle spasms",
            "breeder": "Big Buddha Seeds / Barney's Farm"
        }
    }
}

def main():
    print("🚀 Updating Missing Rosin Products (Elvis, Super Cheese, Blue Cheese)...")
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
