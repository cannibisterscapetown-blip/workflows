#!/usr/bin/env python3
"""
Update Cannibisters Full Spectrum CBD Cream Metafields.
"""

from shopify_api import create_or_update_metafield, get_product
import sys

PRODUCT_ID = "9039396798676"

# Metafields for specialized CBD Cream
METAFIELDS = {
    "lineage": "Full Spectrum Rosin x Aloe Vera",
    "flowering_time": "N/A",
    "profile": "CBD Topical Cream",
    "height": "N/A",
    "stretch_percentage": "N/A",
    "average_thc_levels": "Full Spectrum", # Denotes presence of cannabinoids
    "flavours": "Natural, Aloe, Earthy", # Scent/aroma profile
    "effects": "Soothing • Hydrating • Relief • Repair",
    "used_for": "Dry skin, inflammation, localized relief, daily skincare",
    "breeder": "Cannibisters"
}

def main():
    print(f"🚀 Updating CBD Cream (ID: {PRODUCT_ID})...")
    print("=" * 60)

    # Verify product exists first
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"❌ Product with ID {PRODUCT_ID} not found!")
        sys.exit(1)
        
    print(f"   Found Product: {product.get('title')}")

    # Update Metafields ONLY (Description left as is)
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
