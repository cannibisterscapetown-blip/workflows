#!/usr/bin/env python3
"""
Update Blue Muffin Joint on Shopify.
Created on Mar 5, 2026.
"""
from shopify_api import update_product_description, create_or_update_metafield

pid = "9094388547796"
title = "Blue Muffin Joints"
profile = "70/30 Indica-Dominant Hybrid"
description = (
    "Blue Muffin is a luscious indica-dominant hybrid with rich blueberry and warm vanilla muffin "
    "flavours layered over sweet berries and light earth. It delivers a deeply relaxing, euphoric "
    "body high that melts tension, lifts the mood, and sparks the appetite—perfect for unwinding "
    "in the evening."
)
tags = [
    "Joint", "Pre-roll", "Indica", "Indica-Dominant", "70/30",
    "Relaxed", "Euphoric", "Happy", "Hungry", "Sleepy",
    "Blueberry", "Berry", "Sweet", "Muffin",
    "New Strains"
]

metafields = {
    "lineage": "Blueberry x Blueberry Muffin (berry-dessert indica cross)",
    "profile": profile,
    "flavours": "Fresh blueberry, warm vanilla muffin, sweet berries, light earth",
    "effects": "Relaxed • Euphoric • Happy • Hungry • Sleepy",
    "used_for": "Evening relaxation, stress relief, appetite stimulation, sleep aid",
    "breeder": "Multiple breeders (widely cultivated indica phenotype)",
}


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
        else:
            print(f"      ❌ Failed to set {key}")
    print(f"   ✅ {mf_count}/{len(metafields)} metafields updated")


if __name__ == "__main__":
    main()
