#!/usr/bin/env python3
"""
Update Chocolope Joint product on Shopify
"""

from shopify_api import update_product_description, update_product_metafields, update_product_tags, get_product

PRODUCT_ID = "9025631912148"

# Data derived from parent Chocolope strain (ID: 8876246728916)
DESCRIPTION = """<p><strong>A Sativa-dominant classic in a convenient 1g joint.</strong></p>
<p>Bursting with rich cocoa, roasted coffee, and sweet haze, the Chocolope Joint is your perfect companion for daytime focus and creative flow. Known for its clear-headed and energetic effects, this nostalgic strain offers a smooth and motivated experience.</p>
<p>Expect an uplifting journey that keeps you productive and inspired.</p>"""

TAGS = [
    "Sativa",
    "Chocolope",
    "Joint",
    "Creative",
    "Euphoric",
    "Happy",
    "Focused",
    "Energetic",
    "Daytime",
    "New Strains"
]

METAFIELDS = {
    "my_fields": {
        "lineage": "Chocolate Thai x Cannalope Haze",
        "profile": "95/5 Sativa-dominant",
        "effects": "Uplifted, Focused, Energetic, Creative, Clear-headed",
        "flavours": "Cocoa, roasted coffee, sweet haze",
        "average_thc_levels": "18–22%",
        "used_for": "Morning motivation, creative flow, productive daytime smoke"
    }
}

def main():
    print(f"🚀 Updating Chocolope Joint (ID: {PRODUCT_ID})...")
    
    # Update description and tags
    if update_product_description(PRODUCT_ID, DESCRIPTION, tags=TAGS):
        print("✅ Description and tags updated.")
    else:
        print("❌ Failed to update description and tags.")
        
    # Update metafields
    if update_product_metafields(PRODUCT_ID, METAFIELDS):
        print("✅ Metafields updated.")
    else:
        print("❌ Failed to update metafields.")
        
    print("\n✨ Chocolope Joint update complete!")

if __name__ == "__main__":
    main()
