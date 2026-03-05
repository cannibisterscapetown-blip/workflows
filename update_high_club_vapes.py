#!/usr/bin/env python3
"""
Update 2 New "The High Club" Vapes on Shopify.
Created on Feb 05, 2026.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

# Product Data Configuration
PRODUCTS = {
    "9062481985748": { # The High Club: Skittlez / Lemon Berry Fire
        "title": "The High Club: Skittlez / Lemon Berry Fire",
        "description": "Experience the best of both worlds with this dual-strain disposable vape from The High Club. <br><br><strong>Skittlez (Indica)</strong> brings the calm with its award-winning sweetness, offering a burst of fruity, grape-like flavor and a deeply relaxing body high.<br><br><strong>Lemon Berry Fire (Sativa-Hybrid)</strong> ignites the senses with a zesty lemon-berry fusion, delivering an uplifted, energetic buzz perfect for sparking creativity or social vibes.<br><br>Toggle between the two or mix them for a custom experience.",
        "tags": ["Vape", "Disposable", "The High Club", "Skittlez", "Lemon Berry Fire", "Indica", "Sativa", "Hybrid", "Sweet", "Fruity", "Citrus", "Berry", "Relaxed", "Happy", "Euphoric", "Creative", "New Strains"],
        "metafields": {
            "lineage": "Zkittlez x (Lemonberry x Fire OG)",
            "flowering_time": "N/A (Derived Product)",
            "profile": "Dual Strain (Indica / Sativa-Hybrid)",
            "height": "N/A",
            "stretch_percentage": "N/A",
            "average_thc_levels": "High Potency Distillate/Resin",
            "flavours": "Sweet Candy, Grape, Lemon Zest, Berry, Gas",
            "effects": "Relaxed • Euphoric • Happy • Creative",
            "used_for": "Stress relief, mood enhancement, creativity, relaxation",
            "breeder": "The High Club"
        }
    },
    "9062480642260": { # The High Club: Permanent Marker / Sun of Peach
        "title": "The High Club: Permanent Marker / Sun of Peach",
        "description": "A potent pairing for the connoisseur. <br><br><strong>Permanent Marker (Indica-Dominant)</strong> delivers a heavy-hitting high with unique notes of floral soap, candy, and gas, melting away stress and tension.<br><br><strong>Sun of Peach (Indica-Dominant)</strong> offers a sweeter escape, blending juicy peach flavors with a diesel kick for a soothing, happy relaxation.<br><br>Ideally suited for evening use or unwinding after a long day.",
        "tags": ["Vape", "Disposable", "The High Club", "Permanent Marker", "Sun of Peach", "Indica", "Indica-Dominant", "Floral", "Soap", "Peach", "Diesel", "Gas", "Relaxed", "Sleepy", "Happy", "Tingly", "New Strains"],
        "metafields": {
            "lineage": "(Biscotti x Jealousy x Sherb) x (Gorilla Piss x Permanent Marker)",
            "flowering_time": "N/A (Derived Product)",
            "profile": "Dual Strain (Indica Dominant)",
            "height": "N/A",
            "stretch_percentage": "N/A",
            "average_thc_levels": "High Potency Distillate/Resin",
            "flavours": "Floral Soap, Sweet Candy, Peach, Diesel, Gas",
            "effects": "Relaxed • Sleepy • Happy • Tingly",
            "used_for": "Insomnia, pain relief, stress, deep relaxation",
            "breeder": "The High Club"
        }
    }
}

def main():
    print("🚀 Updating The High Club Vapes (Feb 05)...")
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
        # Construct HTML description with bold profile at the top if needed, 
        # but the description key already has HTML, so likely just use it directly 
        # or prepend profile if consistent with other products.
        # Current pattern seems to be: <strong>Profile</strong><br><br>Description
        
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
