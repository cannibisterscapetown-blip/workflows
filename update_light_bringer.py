#!/usr/bin/env python3
"""
Update Light Bringer Joint on Shopify.
Created on Feb 12, 2026.
"""
from shopify_api import update_product_description, create_or_update_metafield, upload_product_image
import os

pid = "9072666804436"
title = "Light Bringer Joint"
profile = "70/30 Sativa-Dominant Hybrid"
description = "Light Bringer is a potent sativa-dominant hybrid known for its illuminating mental clarity and energetic lift. This strain delivers a crisp profile of sharp citrus, sweet pine, and subtle earthy undertones. It's the perfect companion for daytime productivity, creative projects, or social gatherings, providing a focused euphoria that clears the mental fog."
tags = ["Joint", "Pre-roll", "Sativa", "Sativa-Dominant", "70/30", "Focused", "Energetic", "Creative", "Citrus", "Pine", "Euphoric", "Daytime", "New Strains"]

metafields = {
    "lineage": "Icarus x Hellfire OG (Exotic Genetix selection)",
    "profile": profile,
    "flavours": "Sharp citrus, sweet pine, earthy gas, lemon",
    "effects": "Focused • Energetic • Creative • Euphoric",
    "used_for": "Daytime productivity, social energy, creative focus",
    "breeder": "Exotic Genetix"
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
        if upload_product_image(pid, PHOTO_PATH):
            print("   ✅ Cover photo uploaded")
        else:
            print("   ❌ Failed to upload cover photo")
    else:
        print(f"   ⚠️ Photo not found at {PHOTO_PATH}")

if __name__ == "__main__":
    main()
