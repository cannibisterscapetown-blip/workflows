#!/usr/bin/env python3
"""
Update Persian Pie on Shopify.
"""

from shopify_api import update_product_description, create_or_update_metafield, get_product
import sys

PRODUCT_ID = "8002266857684"

# Description
DESCRIPTION = """Persian Pie is a powerful hybrid from Green House Seeds, combining the zesty citrus profile of Lemon Tree with the sweet, creamy depth of Banana Krumble. This vigorous strain delivers an explosion of fruity flavours, starting with fresh lemon and ending with earthy, caramelized banana notes. The effects are balanced yet potent, offering a heavy body relaxation coupled with a creative, cerebral buzz."""

TAGS = ["New Strains", "Flower", "Hybrid", "Persian Pie", "Relaxed", "Creative", "Fruity"]

# Metafields
METAFIELDS = {
    "lineage": "Lemon Tree x Banana Krumble",
    "flowering_time": "8–9 weeks",
    "profile": "60/40 Indica-Dominant Hybrid",
    "height": "Medium-Tall",
    "stretch_percentage": "±40%",
    "average_thc_levels": "25–27%",
    "flavours": "Lemon, Banana, Earthy, Sweet Cream, Gas",
    "effects": "Relaxed • Euphoric • Creative • Happy • Calm",
    "used_for": "Stress relief, creative sessions, evening relaxation",
    "breeder": "Green House Seeds"
}

def main():
    print(f"🚀 Updating Persian Pie (ID: {PRODUCT_ID})...")
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
