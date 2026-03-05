#!/usr/bin/env python3
"""
Update Apple & Banana Gelato on Shopify.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

PRODUCT_ID = "7889558110420"

# Description
DESCRIPTION = """Apple & Banana Gelato is a delicious hybrid from Lit Farms, crossing the fruity powerhouse Apples and Bananas with the creamy legend Gelato #41. This strain offers a perfectly balanced high, combining euphoria and creativity with a soothing, relaxed finish. The flavour profile is a dessert-lover's dream, featuring notes of sweet apple, ripe banana, and earthy spice wrapped in a smooth, creamy finish."""

TAGS = ["New Strains", "Flower", "Hybrid", "Apple & Banana Gelato", "Creative", "Fruity", "Relaxed"]

# Metafields
METAFIELDS = {
    "lineage": "Apples and Bananas x Gelato #41",
    "flowering_time": "9 weeks",
    "profile": "50/50 Balanced Hybrid",
    "height": "Medium",
    "stretch_percentage": "±40%",
    "average_thc_levels": "24–28%",
    "flavours": "Baked Apple, Banana, Sweet Cream, Earthy Spice",
    "effects": "Uplifted • Creative • Euphoric • Relaxed • Happy",
    "used_for": "Creative work, social gatherings, stress relief, mood boost",
    "breeder": "Lit Farms"
}

def main():
    print(f"🚀 Updating Apple & Banana Gelato (ID: {PRODUCT_ID})...")
    print("=" * 60)

    # Verify product exists first
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"❌ Product with ID {PRODUCT_ID} not found!")
        sys.exit(1)
        
    print(f"   Found Product: {product.get('title')}")

    # 1. Update Description and Tags
    # Prepend Profile text directly in bold
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
