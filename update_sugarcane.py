#!/usr/bin/env python3
"""
Update Sugarcane Hash Rosin product on Shopify.
"""

from shopify_api import update_product_description, create_or_update_metafield
import os

PRODUCT_ID = "9031060848852"

# Premium description
DESCRIPTION = """Sugar Cane is a rare and exotic hybrid strain by In House Genetics, created by crossing Platinum with Slurricane. Known for its frosty appearance and sweet, sugary flavor profile, this premium Hash Rosin concentrate captures the essence of the plant. It offers an energetic and focused high that settles into a relaxing body buzz. Perfect for those seeking creativity and mood elevation."""

TAGS = ["New Strains", "Limited Collection", "Concentrate", "Rosin", "Hash Rosin", "Sugar Cane", "Hybrid", "High Potency"]

METAFIELDS = {
    "lineage": "Platinum x Slurricane (In House Genetics)",
    "profile": "Sativa-Dominant Hybrid",
    "average_thc_levels": "70–80% (High Potency)",
    "flavours": "Sweet, sugary, grape, floral, earthy",
    "effects": "Energetic • Focused • Uplifted • Happy • Relaxed",
    "used_for": "Creativity, mood elevation, stress relief"
}

def main():
    print(f"🚀 Updating Sugarcane Hash Rosin (ID: {PRODUCT_ID})...")
    print("=" * 60)
    
    # 1. Update Description and Tags
    # Prepend Profile text directly in bold to match Martine's style
    profile_text = METAFIELDS['profile']
    full_description = f"<strong>{profile_text}</strong><br><br>{DESCRIPTION}"
    
    desc_success = update_product_description(PRODUCT_ID, full_description, TAGS)
    if desc_success:
        print(f"   ✅ Description & Tags updated")
    else:
        print(f"   ❌ Failed to update Description & Tags")
        
    # 2. Update Metafields
    print(f"   Updating metafields...")
    mf_success_count = 0
    for key, value in METAFIELDS.items():
        if create_or_update_metafield(PRODUCT_ID, "my_fields", key, value):
            mf_success_count += 1
        else:
            print(f"      ❌ Failed on {key}")
            
    print(f"   ✅ {mf_success_count}/{len(METAFIELDS)} metafields updated")

    print("\n" + "=" * 60)
    print("🎉 Update process finished!")

if __name__ == "__main__":
    main()
