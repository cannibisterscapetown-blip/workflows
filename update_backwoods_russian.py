#!/usr/bin/env python3
"""
Update Backwoods Rolling tobacco leaf - Russian Creme on Shopify.
"""

from shopify_api import create_or_update_metafield, get_product
import sys

PRODUCT_ID = "9032980431060"

# Metafields suitable for Backwoods Russian Creme
METAFIELDS = {
    "lineage": "N/A",
    "flowering_time": "N/A",
    "profile": "Tobacco Leaf",
    "height": "N/A",
    "stretch_percentage": "N/A",
    "average_thc_levels": "N/A",
    "flavours": "Russian Creme, Cream, Coffee, Vodka",
    "effects": "Relaxed • Buzz",
    "used_for": "Rolling, Relaxation, Socializing",
    "breeder": "Backwoods"
}

def main():
    print(f"🚀 Updating Backwoods Russian Creme (ID: {PRODUCT_ID})...")
    print("=" * 60)

    # Verify product exists first
    product = get_product(PRODUCT_ID)
    if not product:
        print(f"❌ Product with ID {PRODUCT_ID} not found!")
        sys.exit(1)
        
    print(f"   Found Product: {product.get('title')}")

    # Update Metafields
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
