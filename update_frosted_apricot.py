#!/usr/bin/env python3
"""
Update Frosted Apricot Joint on Shopify.
Created on Feb 12, 2026.
"""
from shopify_api import update_product_description, create_or_update_metafield, upload_product_image
import os

pid = "9072669163732"
title = "Frosted Apricot Joint"
profile = "70/30 Indica-Dominant Hybrid"
description = "Frosted Apricot is a stunning cross of Irene OG and Apricot Helix. This strain delivers a unique profile of ripe apricot and sweet stone fruit layered over heavy diesel gas. It provides a blissful, euphoric lift followed by a deep physical relaxation—ideal for unwinding in the evening while maintaining a happy, creative headspace."
tags = ["Joint", "Pre-roll", "Indica", "Indica-Dominant", "70/30", "Relaxed", "Euphoric", "Happy", "Apricot", "Fruit", "Diesel", "Irene OG", "Apricot Helix", "New Strains"]

metafields = {
    "lineage": "Irene OG x Apricot Helix",
    "profile": profile,
    "flavours": "Ripe apricot, sweet stone fruit, diesel gas, citrus",
    "effects": "Relaxed • Euphoric • Happy • Creative",
    "used_for": "Evening relaxation, stress relief, mood enhancement",
    "breeder": "Capulator / Farmhouse Genetics"
}

# Standard Normal Joint photo path
PHOTO_PATH = "/Users/norton/.gemini/antigravity/brain/ac48112d-1734-466e-9d19-afb7eb85b105/uploaded_image_1767192210692.jpg"

def main():
    print(f"🚀 Updating {title}...")
    
    # 1. Description & Tags
    full_desc = f"<strong>{profile}</strong><br><br>{description}"
    if update_product_description(pid, full_desc, tags):
        print("   ✅ Description & Tags updated")
    else:
        print("   ❌ Failed to update Description & Tags")

    # 2. Metafields
    mf_count = 0
    for key, val in metafields.items():
        if create_or_update_metafield(pid, "my_fields", key, val):
            mf_count += 1
            print(f"      ✅ Set {key}")
    print(f"   ✅ {mf_count}/6 metafields updated")

    # 3. Photo
    if os.path.exists(PHOTO_PATH):
        # We use a custom call since upload_product_image doesn't set position 1 explicitly 
        # but shopify_api is used for standard consistency.
        # However, for 'standard' we just use the helper.
        if upload_product_image(pid, PHOTO_PATH):
            print("   ✅ Cover photo uploaded")
        else:
            print("   ❌ Failed to upload cover photo")
    else:
        print(f"   ⚠️ Photo not found at {PHOTO_PATH}")

if __name__ == "__main__":
    main()
