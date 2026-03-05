#!/usr/bin/env python3
"""
Update Orange Marmalade Joint (ID: 9043939164372) on Shopify.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

# Correct Product ID for the Joint
PRODUCT_ID = "9043939164372"

# Description - Keeping the same premium description
DESCRIPTION = """Orange Marmalade is a zesty sativa-dominant hybrid that lives up to its name with a deliciously sweet and citrusy flavour profile. A cross between Exodus Cheese and Orange Diesels, this strain delivers a honey-sweet aroma with sharp notes of fresh orange and herbal spice. The effects are vibrant and energetic, offering a creative, uplifting high that melts into a relaxing warmth, making it perfect for daytime use or social gatherings."""

TAGS = ["New Strains", "Joint", "Sativa Dominant Hybrid", "Orange Marmalade", "Energetic", "Citrus", "Creative"]

# Metafields
METAFIELDS = {
    "lineage": "Exodus Cheese x Orange Diesels",
    "flowering_time": "8-9 weeks",
    "profile": "70/30 Sativa-Dominant Hybrid",
    "height": "Medium",
    "stretch_percentage": "±150%",
    "average_thc_levels": "24%",
    "flavours": "Sweet Orange, Citrus Zest, Honey, Herbal",
    "effects": "Uplifted • Euphoric • Energetic • Creative • Happy",
    "used_for": "Daytime energy, creative projects, mood elevation, social events",
    "breeder": "Unknown"
}

def main():
    print(f"🚀 Updating Orange Marmalade Joint (ID: {PRODUCT_ID})...")
    print("=" * 60)

    # Verify product exists first
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"❌ Product with ID {PRODUCT_ID} not found!")
        sys.exit(1)
        
    print(f"   Found Product: {product.get('title')}")

    # 1. Update Description and Tags
    profile_text = METAFIELDS['profile']
    full_description = f"<strong>{profile_text}</strong><br><br>{DESCRIPTION}"
    
    print(f"   Updating Description & Tags...")
    if update_product_description(PRODUCT_ID, full_description, TAGS):
        print(f"   ✅ Description & Tags updated")
    else:
        print(f"   ❌ Failed to update Description & Tags")

    # 2. Update Metafields
    print(f"   Updating metafields...")
    mf_success_count = 0
    for key, value in METAFIELDS.items():
        if create_or_update_metafield(PRODUCT_ID, "my_fields", key, value):
            mf_success_count += 1
            print(f"      ✅ Set {key} to '{value}'")
        else:
            print(f"      ❌ Failed on {key}")
            
    print(f"   ✅ {mf_success_count}/{len(METAFIELDS)} metafields updated")

    print("\n" + "=" * 60)
    print("🎉 Update process finished!")

if __name__ == "__main__":
    main()
